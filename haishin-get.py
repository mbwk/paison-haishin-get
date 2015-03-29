#!/usr/bin/env python3
#

import urllib.request
import sys
import inspect
import os

from streams import *

# Stream services to use
services = [Twitch, Hitbox]


class Streamer:

    def __init__(self, name, svcstr):
        self.name = name
        self.svcstr = svcstr.lower()
        self.service = self.detectStreamSvc()

    def getName(self):
        return self.name

    def getService(self):
        return self.service

    def detectStreamSvc(self):
        for service in services:
            if self.svcstr in service.identified_by:
                return service()

    def getInfo(self):
        msg = ""
        try:
            msg = self.service.get_info(self.name)
        except:
            msg = "Service not found: {} {}".format(self.name, self.svcstr)
        return msg


def makeStreamer(name, svcstr):
    streamer = Streamer(name, svcstr)
    return streamer


def readConf():
    streamers = []
    localdir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe())))
    confile = open(localdir + "/streams.conf", "r")
    for line in confile:
        if line.startswith("#"):
            continue

        splitln = line.split()
        if len(splitln) == 2:
            streamers.append(makeStreamer(splitln[0], splitln[1]))

    return streamers


def parseArgs():
    streamers = []
    streamers.append(makeStreamer(sys.argv[1], sys.argv[2]))
    return streamers


def main():
    if len(sys.argv) == 3:
        streamers = parseArgs()
    else:
        streamers = readConf()

    for s in streamers:
        print(s.getInfo())


if __name__ == "__main__":
    main()
