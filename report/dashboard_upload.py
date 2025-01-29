from util.actor import Actor


class DashboardUpload(Actor):
    def __init__(self, actor_id, dashboard, sensor, interval=2, verbose=False):
        super().__init__(actor_id, interval=interval, verbose=verbose)
        self._dashboard = dashboard
        self._sensor = sensor
        self._current_value = None

    async def work(self):
        new_value = self._sensor.value()
        if new_value != self._current_value:
            self._current_value = new_value
            self.upload_data()
        if self._verbose:
            self.log("Uploading dashboard data for sensor %s" % self._sensor)

    def upload_data(self):
        pass
