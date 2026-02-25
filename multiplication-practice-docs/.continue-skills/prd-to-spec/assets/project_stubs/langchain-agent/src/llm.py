from typing import Sequence, Callable, Any, List

from langchain.agents import create_agent
from langchain_core.language_models import BaseChatModel
from langchain_core.tools import BaseTool
from langchain_litellm import ChatLiteLLM
from litellm import embedding
from pydantic import BaseModel


def get_langchain_llm() -> BaseChatModel:
    return ChatLiteLLM(model="sap/gpt-4o")


def embed(text: list[str]) -> List[float]:
    return embedding(model="sap/text-embedding-3-small", input=text).data[0][
        "embedding"
    ]


def create_langchain_agent(
    tools: Sequence[BaseTool | Callable[..., Any] | dict[str, Any]], system_prompt: str
):
    return create_agent(
        model=get_langchain_llm(),
        system_prompt=system_prompt,
        tools=tools,
    )


class ResponseModel(BaseModel):
    response: str
    traces: List[str] = []


class RequestBody(BaseModel):
    prompt: str


if __name__ == "__main__":
    llm = get_langchain_llm()
    response = llm.invoke("Hello, how are you?")
    # response = embed(["Hello, world!"])
    print(response)
