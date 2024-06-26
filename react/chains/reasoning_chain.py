from dotenv import load_dotenv

load_dotenv()

from langchain import hub
from langchain.agents import create_react_agent
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_openai.chat_models import ChatOpenAI

react_prompt: PromptTemplate = hub.pull("hwchase17/react")


@tool
def fahrenheit_to_celsius(num: float) -> float:
    """
    :param num: a number to convert from Fahrenheit to Celsius
    :return: the number converted to  Celsius
    """
    num = float(num)
    celsius = (num - 32) * 5 / 9
    return celsius


@tool
def triple(num: float) -> float:
    """
    :param num: a number to triple
    :return: the number multiplied by 3 (tripled(
    """

    return num * 3


tools = [TavilySearchResults(max_results=3), fahrenheit_to_celsius, triple]

llm = ChatOpenAI(model="gpt-4o")

react_reasoning_runnable = create_react_agent(llm, tools, react_prompt)
