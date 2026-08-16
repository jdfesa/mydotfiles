select(
  (.UNIT // "") == $unit
  and (.JOB_TYPE // "") == "start"
  and has("JOB_RESULT")
  and (._PID // "") == "1"
  and (._COMM // "") == "systemd"
  and ((.__REALTIME_TIMESTAMP // "0" | tonumber) >= $minimum_us)
)
