# ioee/dbrouters.py
from api.models import IoeNoti
from code_share.models import Code, Branch
class MyDBRouter(object):
    def __init__(self):
        self.fuse_attend_models = [IoeNoti, Code, Branch]
        
    def db_for_read(self, model, **hints):
        """ reading IoeNoti from fuse_attend """
        if model in self.fuse_attend_models:
            return 'ioee' # 'fuse_attend' cause both are same
        return None

    def db_for_write(self, model, **hints):
        """ writing IoeNoti to fuse_attend """
        if model in self.fuse_attend_models:
            return 'ioee' # 'fuse_attend' cause both are same
        return None
