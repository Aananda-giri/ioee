# ioee/dbrouters.py
from api.models import IoeNoti

class MyDBRouter(object):

    def db_for_read(self, model, **hints):
        """ reading IoeNoti from fuse_attend """
        if model == IoeNoti:
            return 'fuse_attend'
        return None

    def db_for_write(self, model, **hints):
        """ writing IoeNoti to fuse_attend """
        if model == IoeNoti:
            return 'fuse_attend'
        return None
