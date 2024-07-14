import abc

from blog_poster.exceptions import NotImplementedException


class BaseRetriever(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def search(self, query: str):
        raise NotImplementedException()
