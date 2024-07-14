import os

from fastapi import WebSocket
from langchain_openai import ChatOpenAI

from blog_poster.config import settings
from blog_poster.llm.providers import BaseLLMProvider
from blog_poster.utils import logger


class OpenAIProvider(BaseLLMProvider):
    def __init__(self, model, temperature, max_tokens):
        super().__init__()
        self.model = model if model else settings.OPENAI_MODEL_NAME
        self.temperature = temperature if temperature else 0
        self.max_tokens = max_tokens if max_tokens else 4096
        self.api_key = self.get_api_key()
        self.base_url = self.get_base_url()
        self.llm = self.get_llm_model()

    def get_api_key(self):
        """
        Gets the OpenAI API key
        Returns:

        """
        try:
            api_key = settings.OPENAI_API_KEY
        except KeyError:
            raise Exception("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        return api_key

    def get_base_url(self):
        """
        Gets the OpenAI Base URL from the environment variable if defined otherwise use the default one
        Returns:

        """
        base_url = os.environ.get("OPENAI_BASE_URL", None)
        return base_url

    def get_llm_model(self):
        # Initializing the chat model
        llm = ChatOpenAI(
            model=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            api_key=self.api_key,
        )
        if self.base_url:
            llm.openai_api_base = self.base_url

        return llm

    async def get_chat_response(
        self,
        messages,
        stream,
        websocket: WebSocket = None,
    ):
        if not stream:
            # Getting output from the model chain using ainvoke for asynchronous invoking
            output = await self.llm.ainvoke(messages)

            return output.content

        else:
            return await self.stream_response(messages, websocket)

    async def stream_response(self, messages, websocket: WebSocket = None):
        paragraph = ""
        response = ""

        # Streaming the response using the chain astream method from langchain
        async for chunk in self.llm.astream(messages):
            content = chunk.content
            if content is not None:
                response += content
                paragraph += content
                if "\n" in paragraph:
                    if websocket is not None:
                        await websocket.send_json({"type": "report", "output": paragraph})
                    else:
                        logger.debug(f"{paragraph}")
                    paragraph = ""

        return response
