import logging, threading, random, time


class Bathroom(object):
    def __init__(self):
        # self.men_entering_queue = threading.Semaphore(3)
        self.exit_key = threading.Lock()
        self.entering_queue = threading.Lock()
        self.women_waiting_queue = threading.Semaphore()
        self.men_waiting_queue = threading.Semaphore()
        self.women_waiting_count = 0
        self.men_waiting_count = 0
        self.women_using_count = 0
        self.men_using_count = 0
        self.free_spaces = 2

    def woman_enter(self):
        self.entering_queue.acquire()
        if self.free_spaces > 0 and self.men_using_count == 0 and self.men_waiting_count == 0:
            logging.debug("woman enter")
            self.women_using_count += 1
            self.free_spaces -= 1
        else:
            logging.debug("woman wait")
            self.women_waiting_count += 1
            self.women_waiting_queue.acquire()
        self.entering_queue.release()
        time.sleep(1)
        self.woman_exit()

    def man_enter(self):
        self.entering_queue.acquire()
        if self.free_spaces > 0  and self.women_using_count == 0 and self.women_waiting_count == 0:
            logging.debug("man enter")
            self.men_using_count += 1
            self.free_spaces -= 1
        else:
            logging.debug("man wait")
            self.men_waiting_count += 1
            self.men_waiting_queue.acquire()
        self.entering_queue.release()
        time.sleep(1)
        self.man_exit()

    def man_exit(self):
        self.exit_key.acquire()
        logging.debug("man exit")
        self.men_using_count -= 1
        self.free_spaces += 1
        self.exit_key.release()
        if self.women_waiting_count > 0:
            while self.men_using_count > 0:
                logging.debug("waiting men to finish")
                pass
            self.women_waiting_count -= 1
            self.free_spaces -=1
            logging.debug("let woman enter")
            self.women_waiting_queue.release()
        elif self.men_waiting_count > 0:
            self.men_waiting_queue.release()

    def woman_exit(self):
        self.exit_key.acquire()
        logging.debug("woman exit")
        self.women_using_count -= 1
        self.free_spaces += 1
        self.exit_key.release()
        if self.men_waiting_count > 0:
            while self.women_using_count  > 0:
                logging.debug("waiting women to finish")
                pass
            self.men_waiting_count -= 1
            self.free_spaces -= 1
            logging.debug("let man enter")
            self.men_waiting_queue.release()
        elif self.women_waiting_count > 0:
            self.women_waiting_queue.release()

def Main():
    logging.basicConfig(format='%(threadName)s, %(asctime)s, %(message)s', datefmt='%M:%S', level=logging.DEBUG)
    bathroom = Bathroom()
    for i in range(5):
        if random.randint(0, 1) == 0:
            t = threading.Thread(target=bathroom.man_enter, args=())
            t.start()
        else:
            t = threading.Thread(target=bathroom.woman_enter, args=())
            t.start()
if __name__ == '__main__':
    Main()
