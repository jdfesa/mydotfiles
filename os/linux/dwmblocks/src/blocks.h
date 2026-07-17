static const Block blocks[] = {
    /* Icon   Command                                   Interval  Signal */
    { "",     "status-sensors",                        30,       1 },
    { "",     "date '+%b %d (%a) %I:%M%p'",             30,       0 },
};

static char delim[] = " | ";
static unsigned int delimLen = 5;
