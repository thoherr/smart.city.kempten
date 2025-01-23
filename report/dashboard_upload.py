from util.actor import Actor


class DashboardUpload(Actor):
    def __init__(self, actor_id, dashboard, sensor, interval=2, verbose=False):
        super().__init__(actor_id, interval=interval, verbose=verbose)
        self._dashboard = dashboard
        self._sensor = sensor

    async def work(self):
        if self._verbose:
            self.log("Uploading dashboard data for sensor %s" % self._sensor)
