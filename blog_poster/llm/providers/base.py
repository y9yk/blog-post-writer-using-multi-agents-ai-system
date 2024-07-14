import abc

from blog_poster.exceptions import NotImplementedException


class BaseLLMProvider(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    async def get_chat_response(self):
        raise NotImplementedException()
