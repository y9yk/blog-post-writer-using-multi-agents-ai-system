import tiktoken

from config import settings


# Cost estimation is via OpenAI libraries and models. May vary for other models
def estimate_llm_cost(input_content: str, output_content: str) -> float:
    encoding = tiktoken.get_encoding(settings.ENCODING_MODEL)
    input_tokens = encoding.encode(input_content)
    output_tokens = encoding.encode(output_content)
    input_costs = len(input_tokens) * settings.INPUT_COST_PER_TOKEN
    output_costs = len(output_tokens) * settings.OUTPUT_COST_PER_TOKEN
    return input_costs + output_costs


def estimate_embedding_cost(model, docs):
    encoding = tiktoken.encoding_for_model(model)
    total_tokens = sum(len(encoding.encode(str(doc))) for doc in docs)
    return total_tokens * settings.EMBEDDING_COST
