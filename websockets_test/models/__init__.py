"""
Abstração
"""
from mongoengine import connect
from pymongo import MongoClient

from websockets_test.settings import CONFIG

config = CONFIG["MONGODB"]["default"]
connect(
    config['base'],  # DB Name
    host=config['host'], username=config['username'], password=config['password'], port=config['port']
)


class Mongo(object):
    """
    Mongo
    """

    model = str
    connected = False

    def __init__(self):
        self.model = self.__class__

    @classmethod
    def switch_connection(cls, connection="default"):
        """
        Alterna as conexões do MongoDB
        """
        conf = CONFIG["MONGODB"][connection]
        client = MongoClient('mongodb://%s:%s@%s:%d/%s' % (
            conf['username'], conf['password'], conf['host'], conf['port'], conf['base'])
        )

        return client
