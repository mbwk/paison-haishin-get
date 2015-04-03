import urllib.request
import sys
import inspect
import os

from .service import gen_services


class Streamer:

    def __init__(self, name, svcstr):
        self.name = name
        self.svcstr = svcstr.lower()
        self.service = self.detect_stream()

    def get_name(self):
        return self.name

    def get_service(self):
        return self.service

    def detect_stream(self):
        for service in gen_services():
            if self.svcstr in service.identified_by:
                return service

    def get_info(self):
        msg = ""
        try:
            msg = self.service.get_info(self.name)
        except:
            msg = "Service not found: {} {}".format(self.name, self.svcstr)
            raise
        return msg


def make_streamer(name, svcstr):
    streamer = Streamer(name, svcstr)
    return streamer


def read_config():
    streamers = []
    localdir = os.path.dirname(
        os.path.abspath(inspect.getfile(inspect.currentframe()))[-1])
    try:
        confile = open(os.path.join(localdir , 'streams.conf'), 'r')
    except:
        raise SystemExit("Could not open find streams.conf in {}".format(localdir))
    for line in confile:
        if line.startswith("#"):
            continue

        splitln = line.split()
        if len(splitln) == 2:
            streamers.append(make_streamer(splitln[0], splitln[1]))

    return streamers


def parse_args():
    streamers = []
    streamers.append(make_streamer(sys.argv[1], sys.argv[2]))
    return streamers


def main():
    if len(sys.argv) == 3:
        streamers = parse_args()
    else:
        streamers = read_config()

    for s in streamers:
        print(s.get_info())