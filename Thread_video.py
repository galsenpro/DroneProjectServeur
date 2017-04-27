from threading import Thread,Event


class ThreadVideo(Thread):
    def __init__(self,drone = None,refresh = 1.0):
        super(ThreadVideo, self).__init__()
        self.drone = drone
        self._stopevent = Event()
        self.refresh = refresh

    def run(self):
        id_inter = self.drone.id_intervention
        while not self._stopevent.isSet():
            self.drone.prendre_video()
            self._stopevent.wait(self.refresh)
        print('fin du thread')

    def stop(self):
        self._stopevent.set()
