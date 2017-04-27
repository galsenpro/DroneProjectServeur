from threading import Thread,Event


class Thread_position(Thread):
    def __init__(self,drone = None,refresh = 1.0):
        super(Thread_position, self).__init__()
        self.drone = drone
        self._stopevent = Event()
        self.refresh = refresh

    def run(self):
        id_inter = self.drone.id_intervention
        while not self._stopevent.isSet():
            self.drone.prend_video()
            self._stopevent.wait(self.refresh)
        print('fin du thread')

    def stop(self):
        self._stopevent.set()

"""def main():
    drone = Drone()
    drone.set_intervention('58ddf84c212566155e8e98ec')
    print('drone OK, debut lecture commandes')
    tetat = Thread_position(drone)
    print('script start')
    tetat.start()
    time.sleep(10)
    print('script stop')
    tetat.stop()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)"""