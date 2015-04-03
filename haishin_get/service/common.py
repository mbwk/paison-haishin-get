from urllib.request import urlopen

class BaseSVC(object):

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