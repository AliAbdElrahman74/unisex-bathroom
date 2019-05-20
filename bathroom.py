#!/usr/bin/env python
import logging, threading, time


class Bathroom(object):
    def __init__(self, num_of_stalls):
        self.exit_key = threading.Lock()
        self.entering_key = threading.Lock()
        self.women_waiting_queue = threading.Semaphore()
        self.men_waiting_queue = threading.Semaphore()
        self.women_waiting_count = 0
        self.men_waiting_count = 0
        self.women_using_count = 0
        self.men_using_count = 0
        self.free_spaces = num_of_stalls

    def woman_enter(self):
        self.entering_key.acquire()
        if self.can_woman_enter_bathroom:
            self.entering_woman()
        else:
            self.woman_wait_in_queue()
        self.entering_key.release()
        time.sleep(1)
        self.woman_exit()

    def can_woman_enter_bathroom(self):
        self.free_spaces > 0 and self.men_using_count == 0 and self.men_waiting_count == 0

    def entering_woman(self):
        logging.debug("woman enter")
        self.women_using_count += 1
        self.free_spaces -= 1

    def woman_wait_in_queue(self):
        logging.debug("woman wait")
        self.women_waiting_count += 1
        self.women_waiting_queue.acquire()

    def man_enter(self):
        self.entering_key.acquire()
        if self.can_man_enter_bathroom():
            self.entering_man()
        else:
            self.man_wait_in_queue()
        self.entering_key.release()
        time.sleep(1)
        self.man_exit()

    def can_man_enter_bathroom(self):
        self.free_spaces > 0  and self.women_using_count == 0 and self.women_waiting_count == 0

    def entering_man(self):
        logging.debug("man enter")
        self.men_using_count += 1
        self.free_spaces -= 1

    def man_wait_in_queue(self):
        logging.debug("man wait")
        self.men_waiting_count += 1
        self.men_waiting_queue.acquire()

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
        self.exiting_woman()
        self.handle_exiting_for_woman()

    def handle_exiting_for_woman(self):
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

    def exiting_woman(self):
        self.exit_key.acquire()
        logging.debug("woman exit")
        self.women_using_count -= 1
        self.free_spaces += 1
        self.exit_key.release()
