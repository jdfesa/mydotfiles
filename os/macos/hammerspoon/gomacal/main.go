package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/exec"
	"path/filepath"
	"runtime"
	"strings"
	"time"

	"golang.org/x/oauth2"
	"golang.org/x/oauth2/google"
	"google.golang.org/api/calendar/v3"
	"google.golang.org/api/option"
)

const separator = " § "

func main() {
	next := flag.String("next", "", "show events within the specified duration, such as 5m or 2h")
	calendarID := flag.String("calendar", "primary", "Google Calendar ID")
	credentialsPath := flag.String("credentials", defaultCredentialsPath(), "OAuth credentials JSON path")
	tokenPath := flag.String("token", defaultTokenPath(), "OAuth token cache path")
	port := flag.Int("port", 8080, "localhost OAuth callback port")
	noAuth := flag.Bool("no-auth", false, "do not start browser authentication when token is missing")
	quietEmpty := flag.Bool("quiet-empty", false, "print nothing when no events are found")
	flag.Parse()

	if err := run(*next, *calendarID, *credentialsPath, *tokenPath, *port, *noAuth, *quietEmpty); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func run(next, calendarID, credentialsPath, tokenPath string, port int, noAuth, quietEmpty bool) error {
	credentials, err := os.ReadFile(expandPath(credentialsPath))
	if err != nil {
		return fmt.Errorf("unable to read credentials file: %w", err)
	}

	config, err := google.ConfigFromJSON(credentials, calendar.CalendarReadonlyScope)
	if err != nil {
		return fmt.Errorf("unable to parse credentials: %w", err)
	}
	config.RedirectURL = fmt.Sprintf("http://localhost:%d/", port)

	client, err := getClient(context.Background(), config, expandPath(tokenPath), port, noAuth)
	if err != nil {
		return err
	}

	service, err := calendar.NewService(context.Background(), option.WithHTTPClient(client))
	if err != nil {
		return fmt.Errorf("unable to create calendar service: %w", err)
	}

	duration := 24 * time.Hour
	if next != "" {
		duration, err = time.ParseDuration(next)
		if err != nil {
			return fmt.Errorf("invalid duration format: %w", err)
		}
	}

	now := time.Now()
	events, err := service.Events.List(calendarID).
		TimeMin(now.Add(-duration).Format(time.RFC3339)).
		TimeMax(now.Add(duration).Format(time.RFC3339)).
		SingleEvents(true).
		OrderBy("startTime").
		Do()
	if err != nil {
		return fmt.Errorf("unable to retrieve events: %w", err)
	}

	var matches []string
	for _, event := range events.Items {
		start, ok := eventStartTime(event)
		if !ok {
			continue
		}

		timeUntilStart := start.Sub(now)
		timeSinceStart := now.Sub(start)
		if (timeUntilStart >= 0 && timeUntilStart <= duration) || (timeSinceStart >= 0 && timeSinceStart <= duration) {
			matches = append(matches, formatEvent(event, start, now))
		}
	}

	if len(matches) == 0 {
		if quietEmpty {
			return nil
		}
		if next != "" {
			fmt.Printf("No events found within %s of current time\n", next)
		} else {
			fmt.Println("No events found today")
		}
		return nil
	}

	for _, line := range matches {
		fmt.Println(line)
	}

	return nil
}

func eventStartTime(event *calendar.Event) (time.Time, bool) {
	if event.Start == nil || event.Start.DateTime == "" {
		return time.Time{}, false
	}

	start, err := time.Parse(time.RFC3339, event.Start.DateTime)
	return start, err == nil
}

func formatEvent(event *calendar.Event, start, now time.Time) string {
	timeInfo := ""
	if until := start.Sub(now); until > 0 {
		timeInfo = fmt.Sprintf("starts in %v", until.Round(time.Minute))
	} else {
		timeInfo = fmt.Sprintf("started %v ago", now.Sub(start).Round(time.Minute))
	}

	return strings.Join([]string{
		cleanField(event.Summary),
		timeInfo,
		extractMeetingLink(event),
		event.Id,
	}, separator)
}

func extractMeetingLink(event *calendar.Event) string {
	if event.ConferenceData != nil {
		for _, entry := range event.ConferenceData.EntryPoints {
			if entry.EntryPointType == "video" && entry.Uri != "" {
				return entry.Uri
			}
		}
	}

	if isURL(event.Location) {
		return cleanURL(event.Location)
	}

	for _, line := range strings.Split(event.Description, "\n") {
		lower := strings.ToLower(line)
		if strings.Contains(lower, "zoom.") ||
			strings.Contains(lower, "teams.") ||
			strings.Contains(lower, "meet.google.") ||
			strings.Contains(lower, "webex.") {
			for _, word := range strings.Fields(line) {
				if isURL(word) {
					return cleanURL(word)
				}
			}
		}
	}

	return ""
}

func isURL(value string) bool {
	value = strings.TrimSpace(value)
	return strings.HasPrefix(value, "http://") || strings.HasPrefix(value, "https://")
}

func cleanURL(value string) string {
	return strings.Trim(strings.TrimSpace(value), "<>()[]{}.,;\"'")
}

func cleanField(value string) string {
	value = strings.ReplaceAll(value, separator, " - ")
	value = strings.ReplaceAll(value, "\n", " ")
	return strings.TrimSpace(value)
}

func getClient(ctx context.Context, config *oauth2.Config, tokenPath string, port int, noAuth bool) (*http.Client, error) {
	token, err := tokenFromFile(tokenPath)
	if err != nil {
		if noAuth {
			return nil, fmt.Errorf("OAuth token not found; run gomacal once manually to authenticate")
		}
		token, err = tokenFromWeb(ctx, config, port)
		if err != nil {
			return nil, err
		}
		if err := saveToken(tokenPath, token); err != nil {
			return nil, err
		}
	}

	return config.Client(ctx, token), nil
}

func tokenFromFile(path string) (*oauth2.Token, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	token := &oauth2.Token{}
	if err := json.NewDecoder(file).Decode(token); err != nil {
		return nil, err
	}
	return token, nil
}

func saveToken(path string, token *oauth2.Token) error {
	if err := os.MkdirAll(filepath.Dir(path), 0700); err != nil {
		return err
	}

	file, err := os.OpenFile(path, os.O_RDWR|os.O_CREATE|os.O_TRUNC, 0600)
	if err != nil {
		return fmt.Errorf("unable to cache OAuth token: %w", err)
	}
	defer file.Close()

	return json.NewEncoder(file).Encode(token)
}

func tokenFromWeb(ctx context.Context, config *oauth2.Config, port int) (*oauth2.Token, error) {
	codeChan := make(chan string, 1)
	server := &http.Server{Addr: fmt.Sprintf(":%d", port)}

	mux := http.NewServeMux()
	mux.HandleFunc("/", func(w http.ResponseWriter, request *http.Request) {
		code := request.URL.Query().Get("code")
		if code == "" {
			http.Error(w, "missing code", http.StatusBadRequest)
			return
		}

		fmt.Fprintln(w, "Authorization successful. You can close this window.")
		codeChan <- code
		go func() {
			time.Sleep(time.Second)
			_ = server.Shutdown(ctx)
		}()
	})
	server.Handler = mux

	errChan := make(chan error, 1)
	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			errChan <- err
		}
	}()

	authURL := config.AuthCodeURL("state-token", oauth2.AccessTypeOffline)
	fmt.Println("Opening browser for Google Calendar authorization...")
	if err := openBrowser(authURL); err != nil {
		fmt.Printf("Could not open browser automatically. Visit:\n%s\n", authURL)
	}

	select {
	case code := <-codeChan:
		token, err := config.Exchange(ctx, code)
		if err != nil {
			return nil, fmt.Errorf("unable to retrieve token: %w", err)
		}
		return token, nil
	case err := <-errChan:
		return nil, fmt.Errorf("OAuth callback server failed: %w", err)
	case <-time.After(5 * time.Minute):
		_ = server.Shutdown(ctx)
		return nil, fmt.Errorf("OAuth authorization timed out")
	}
}

func openBrowser(url string) error {
	switch runtime.GOOS {
	case "darwin":
		return exec.Command("open", url).Start()
	case "linux":
		return exec.Command("xdg-open", url).Start()
	case "windows":
		return exec.Command("rundll32", "url.dll,FileProtocolHandler", url).Start()
	default:
		return fmt.Errorf("unsupported platform")
	}
}

func defaultCredentialsPath() string {
	return filepath.Join(configHome(), "gomacal", "credentials.json")
}

func defaultTokenPath() string {
	return filepath.Join(stateHome(), "gomacal", "token.json")
}

func configHome() string {
	if value := os.Getenv("XDG_CONFIG_HOME"); value != "" {
		return value
	}
	return filepath.Join(homeDir(), ".config")
}

func stateHome() string {
	if value := os.Getenv("XDG_STATE_HOME"); value != "" {
		return value
	}
	return filepath.Join(homeDir(), ".local", "state")
}

func homeDir() string {
	home, err := os.UserHomeDir()
	if err != nil {
		log.Fatal(err)
	}
	return home
}

func expandPath(path string) string {
	if strings.HasPrefix(path, "~/") {
		return filepath.Join(homeDir(), strings.TrimPrefix(path, "~/"))
	}
	return path
}
