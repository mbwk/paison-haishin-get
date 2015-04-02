from .twitch import TwitchSVC
from .hitbox import HitboxSVC

_CLASSES = [klass for name, klass in globals().items() if name.endswith('SVC')]

def gen_services():
	return [klass() for klass in _CLASSES]