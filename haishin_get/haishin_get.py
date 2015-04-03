import urllib.request
import sys
import inspect
import shutil
import os

from .service import gen_services


class Streamer(object):
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
            msg = "Stream not found: {} {}".format(self.name, self.svcstr)
        return msg

class ConfigHandler(object):
    dir_ = os.path.expanduser('~/.config/haishin-get/')
    file = 'streams.conf'

    def exists(self):
        if not os.path.exists(self.dir_):
            os.makedirs(self.dir_)
        if not os.path.isfile(os.path.join(self.dir_, self.file)):
            return False
        return True

    def create(self):
        sample_dir = os.path.abspath(__package__)
        sample_conf = os.path.join(sample_dir, self.file)

        shutil.copyfile(sample_conf, os.path.join(self.dir_, self.file))    

    def read(self):
        streamers = []        
        try:
            confile = open(os.path.join(self.dir_ , 'streams.conf'), 'r')
        except:
            raise SystemExit("Could not open find streams.conf in {}".format(localdir))
        for line in confile:
            if line.startswith("#"):
                continue

            splitln = line.split()
            if len(splitln) == 2:
                streamers.append(Streamer(splitln[0], splitln[1]))

        return streamers


def parse_args():
    streamers = []
    streamers.append(Streamer(sys.argv[1], sys.argv[2]))
    return streamers


def main():
    if len(sys.argv) == 3:
        streamers = parse_args()
    else:
        ch = ConfigHandler()
        if not ch.exists():
            ch.create()
        streamers = ch.read()

    for s in streamers:
        print(s.get_info())