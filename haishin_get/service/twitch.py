from urllib.request import urlopen
import json

from .common import BaseSVC

class TwitchSVC(BaseSVC):
    identified_by = ("twitch", "t")
    api = "https://api.twitch.tv/kraken/"

    def get_info(self, streamer_name):
        return self.get_stream_info(streamer_name)

    def get_channel_info(self, streamer_name):
        reqstr = self.request(self.api, "channels", streamer_name)
        obj = json.loads(reqstr)

        display_name = obj["display_name"]
        url = obj["url"]

        return self.report(display_name, False, url)

    def get_stream_info(self, streamer_name):
        reqstr = self.request(self.api, "streams", streamer_name)
        obj = json.loads(reqstr)

        if obj["stream"] is None:
            return self.get_channel_info(streamer_name)

        stream = obj["stream"]
        channel = stream["channel"]

        display_name = channel["display_name"]
        game = channel["game"]
        url = channel["url"]

        return self.report(display_name, True, url, game)