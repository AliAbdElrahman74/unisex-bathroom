#!/usr/bin/env python
import importlib, logging, threading, random

importlib.import_module("bathroom")
from bathroom import Bathroom

class Main:
    @staticmethod
    def run():
        logging.basicConfig(format='%(threadName)s, %(asctime)s, %(message)s', datefmt='%M:%S', level=logging.DEBUG)
        num_of_stalls = int(input("Enter number of stalls "))
        num_of_users = int(input("Enter number of users "))
        bathroom = Bathroom(num_of_stalls)
        Main.enter_users_to_bathroom(num_of_users, bathroom)

    @staticmethod
    def enter_users_to_bathroom(num_of_users, bathroom):
        for i in range(num_of_users):
            if random.randint(0, 1) == 0:
                Main.start_thread(bathroom.man_enter)
            else:
                Main.start_thread(bathroom.woman_enter)
    @staticmethod
    def start_thread(target_fun):
        t = threading.Thread(target=target_fun, args=())
        t.start()

Main.run()
