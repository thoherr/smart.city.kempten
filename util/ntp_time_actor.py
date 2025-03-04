from time import gmtime
import ntptime

import setup_values
from util.actor import Actor

ntptime.timeout = setup_values.NTP_TIMEOUT


class NtpTimeActor(Actor):
    def __init__(self, actor_id="NtpTimeActor", interval=setup_values.NTP_QUERY_INTERVAL, verbose=False):
        super().__init__(actor_id, interval=interval, verbose=verbose, debug=verbose)

    def set_time(self):
        try:
            if self._verbose:
                self.log("Getting NTP time...")
            t = ntptime.time()
            tm = gmtime(t)
            if self._verbose:
                self.log(f"Got NTP time {tm}...")
            # It seems like the "fix" of the YR 2036 bug (see micropython/net/ntptime/ntptime.py)
            # sometimes leads to a time warp to 2036.
            # I assume that the NTP request might lead to 0 some times, so the time is in fact invalid.
            # However, in this case, ntptime.time() adds 0x100000000 to the time, because it thinks there was an
            # overflow, since 0 < MIN_NTP_TIMESTAMP = 3913056000 (which is 2024-01-01 00:00:00)
            # Therefore we only copy values greater than 2024 and less than 2036.
            # As a consequence, this code will not work after 2035...
            if 2024 < tm[0] < 2036:
                import machine
                machine.RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
        except OSError:
            if self._verbose:
                self.log("ERROR: Failed to get NTP time")

    async def work(self):
        self.set_time()
