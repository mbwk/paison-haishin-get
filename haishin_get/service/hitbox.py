from urllib.request import urlopen
import json

from .common import BaseSVC

class HitboxSVC(BaseSVC):
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
