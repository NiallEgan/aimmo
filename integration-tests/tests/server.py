import socket
import re
import sys

from time import sleep
from subprocess import call


################################################################################

# Register custom mockery...

# import sys
# # Add the ptdraft folder path to the sys.path list
# sys.path.append('../../')
#
# import importlib
# mockery = importlib.import_module("aimmo-game-creator.tests.test_worker_manager")


################################################################################

import signal
import sys
import json

################################################################################

# register a specific signal handler if necessary at the termination of the program
# def signal_handler(signal, frame):
    # close the socket here
    # sys.exit(0)
# signal.signal(signal.SIGINT, signal_handler)

################################################################################

class Runner():
    def __init__(self, binder):
        self.binder = binder
    def apply(self, received):
        return received

################################################################################

# Class that receives a mock(as in unit tests) and creates a lightweight server
# at localhost
class MockServer():
    def __register_connection(self, host, port):
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # allows reuse of the socket once the process gets stopped
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #bind the connection
        self.sock.bind((host, port))

        #listen to one client
        self.sock.listen(1)

        print "Server starting on port " + str(port)

    def __init__(self, host="localhost", port=8000):
        self.__register_connection(host, port)
        self.runners = []

    def register_runner(self, runner):
        self.runners.append(runner)

    def clear_runners(self):
        self.runners = []

    # for the moment supports only gets
    def receive(self):
        def receive_lines(csock):
            raw_request = csock.recv(1024)
            lines = raw_request.split('\n')
            return raw_request, lines[0]

        raw_request, get_request = receive_lines(self.csock)
        resource_identifier = get_request.split(' ')[1]

        return raw_request, resource_identifier

    def serve(self):
        received, received_formatted = self.receive()
        print "Received request " + received_formatted

        ans = received_formatted
        for runner in self.runners:
            ans = runner.apply(ans)
        return ans

    def run(self, times=1000):
        #listen for connection
        while times > 0:
            self.csock, self.caddr = self.sock.accept()
            print "Connection from:" + `self.caddr`

            # serve the connection
            str_ans = self.serve()
            self.csock.send("HTTP/1.0 200 OK\nContent-Type: text/plain\n\n" + str_ans)

            times -= 1
            self.csock.close()

if __name__ == "__main__":
    server = MockServer()
    server.run()
