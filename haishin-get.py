#!/usr/bin/env python3
#

import urllib.request
import json, sys, inspect, os
from enum import Enum

TWITCHAPI = "https://api.twitch.tv/kraken/"
HITBOXAPI = "https://api.hitbox.tv/"

class Report():
    def __init__(self, name, isstrm, url, game = "(n/a)"):
        self.name = name
        self.isstrm = isstrm
        self.url = url
        self.game = game

    def getMsg(self):
        if self.isstrm:
            return "{name} ({url}) is STREAMING {game}".format(name=self.name, url=self.url, game=self.game)
        elif not self.isstrm:
            return "{name} ({url}) is OFFLINE".format(name=self.name, url=self.url)


class StreamSvc(Enum):
    none = 0
    twitch = 1
    hitbox = 2

    def getSvc(instr):
        if type(instr) != str:
            return None

        instr = instr.lower

        if instr == "twitch" or instr == "ttv" or instr == "t":
            return StreamSvc.twitch
        elif instr == "hitbox" or instr == "hb" or instr == "h":
            return StreamSvc.hitbox
        else:
            return None
        
def streamApiRequest(api, path, value):
    requestString = "{}{}/{}".format(api, path, value)
    return urllib.request.urlopen(requestString).read().decode("utf-8")


def getChannelInfoTwitch(streamer_name):
    reqstr = streamApiRequest(TWITCHAPI, "channels", streamer_name)
    obj = json.loads(reqstr)

    if obj["status"] == 404:
        return None

    display_name = obj["display_name"]
    url = obj["url"]

    return Report(display_name, False, url)


def getStreamInfoTwitch(streamer_name):
    reqstr = streamApiRequest(TWITCHAPI, "streams", streamer_name)
    obj = json.loads(reqstr)

    if obj["stream"] is None:
        return getChannelInfoTwitch(streamer_name)

    stream = obj["stream"]
    channel = stream["channel"]

    display_name = channel["display_name"]
    game = channel["game"]
    url = channel["url"]

    return Report(display_name, True, url, game)


def getMediaInfoHitbox(streamer_name):
    reqstr = streamApiRequest(HITBOXAPI, "media/live", streamer_name)
    obj = json.loads(reqstr)

    livestreamobj = obj["livestream"][0]

    display_name = livestreamobj["media_display_name"]
    
    if livestreamobj["media_is_live"] == "1":
        isstrm = True
    else:
        isstrm = False

    url = livestreamobj["channel"]["channel_link"]
    game = livestreamobj["category_name"]

    return Report(display_name, isstrm, url, game)


def getStatus(streamer):
    if streamer.service == StreamSvc.twitch:
        return getStreamInfoTwitch(streamer.name)
    elif streamer.service == StreamSvc.hitbox:
        return getMediaInfoHitbox(streamer.name)
    else:
        return "invalid service specified"


class Streamer:
    def __init__(self, name, service):
        self.name = name
        self.service = service

    def getName(self):
        return self.name

    def getService(self):
        return self.service


def makeStreamer(name, svcstr):
    svcstr = svcstr.lower()

    if "twitch" == svcstr or svcstr.startswith("t"):
        svcenum = StreamSvc.twitch
    elif "hitbox" == svcstr or svcstr.startswith("h"):
        svcenum = StreamSvc.hitbox
    else:
        svcenum = StreamSvc.none

    return Streamer(name, svcenum)


def readConf():
    streams = []
    localdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    confile = open(localdir + "/streams.conf", "r")
    for line in confile:
        if line.startswith("#"):
            continue

        splitln = line.split()
        if len(splitln) == 2:
            streams.append(makeStreamer(splitln[0], splitln[1]))

    return streams


def parseArgs():
    streams = []
    streams.append(makeStreamer(sys.argv[1], sys.argv[2]))
    return streams


def main():
    if len(sys.argv) == 3:
        streams = parseArgs()
    else:
        streams = readConf()

    for s in streams:
        r = getStatus(s)

        if type(r) is not Report:
            print("NULL: " + s.getName())
            continue

        print(r.getMsg())
        

if __name__ == "__main__":
    main()


