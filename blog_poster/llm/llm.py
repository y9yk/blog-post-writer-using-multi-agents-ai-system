from typing import Any, Dict, Optional

from fastapi import WebSocket

from blog_poster.exceptions import NotImplementedException
from blog_poster.llm.providers import BaseLLMProvider
from blog_poster.utils import estimate_llm_cost, logger


def get_llm(llm_provider, **kwargs):
    match llm_provider:
        case "openai":
            from blog_poster.llm.providers import OpenAIProvider as LLMProvider
        case _:
            raise NotImplementedException()

    llm_provider = LLMProvider
    return llm_provider(**kwargs)


async def create_chat_completion(
    messages: list,  # type: ignore
    model: Optional[str] = None,
    temperature: float = 1.0,
    max_tokens: Optional[int] = 4096,
    llm_provider: Optional[str] = None,
    stream: Optional[bool] = False,
    websocket: WebSocket | None = None,
    llm_kwargs: Dict[str, Any] | None = None,
    cost_callback: callable = None,
) -> str:
    """Create a chat completion using the OpenAI API
    Args:
        messages (list[dict[str, str]]): The messages to send to the chat completion
        model (str, optional): The model to use. Defaults to None.
        temperature (float, optional): The temperature to use. Defaults to 0.9.
        max_tokens (int, optional): The max tokens to use. Defaults to None.
        stream (bool, optional): Whether to stream the response. Defaults to False.
        llm_provider (str, optional): The LLM Provider to use.
        webocket (WebSocket): The websocket used in the currect request,
        cost_callback: Callback function for updating cost
    Returns:
        str: The response from the chat completion
    """

    # validate input
    if model is None:
        raise ValueError("Model cannot be None")
    if max_tokens is not None and max_tokens > 8001:
        raise ValueError(f"Max tokens cannot be more than 8001, but got {max_tokens}")

    # Get the provider from supported providers
    provider: BaseLLMProvider = get_llm(
        llm_provider,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        **llm_kwargs,
    )

    response = ""
    # create response
    for _ in range(10):  # maximum of 10 attempts
        response = await provider.get_chat_response(messages, stream, websocket)

        if cost_callback:
            llm_costs = estimate_llm_cost(str(messages), response)
            cost_callback(llm_costs)

        return response

    logger.error(f"Failed to get response from {llm_provider} API")
    raise RuntimeError(f"Failed to get response from {llm_provider} API")
