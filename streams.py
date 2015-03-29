from urllib.request import urlopen
import json


class Base(object):

    def get_name(self):
        return self.__name__

    def request(self, api, path, value):
        requestString = "{}{}/{}".format(api, path, value)
        request = urlopen(requestString).read().decode("utf-8")

        return request

    def report(self, name, isstrm, url, game=""):
        if isstrm:
            msg = "{name} ({url}) is STREAMING {game}".format(
                name=name,
                url=url,
                game=game)
        else:
            msg = "{name} ({url}) is OFFLINE".format(
                name=name,
                url=url)
        return msg


class Twitch(Base):
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


class Hitbox(Base):
    identified_by = ("hitbox", "h")
    api = "https://api.hitbox.tv/"

    def get_info(self, streamer_name):
        reqstr = self.request(self.api, "media/live", streamer_name)
        obj = json.loads(reqstr)

        livestreamobj = obj["livestream"][0]

        display_name = livestreamobj["media_display_name"]

        if livestreamobj["media_is_live"] == "1":
            isstrm = True
        else:
            isstrm = False

        url = livestreamobj["channel"]["channel_link"]
        game = livestreamobj["category_name"]

        return self.report(display_name, isstrm, url, game)
