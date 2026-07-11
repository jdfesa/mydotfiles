-- Local Hammerspoon feature switches.

return {
  google_calendar = {
    enabled = false,
    command = os.getenv("HOME") .. "/.local/bin/gomacal",
    lookahead = "5m",
    interval_seconds = 60,
  },
}
