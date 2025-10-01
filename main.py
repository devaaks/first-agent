import os
import json
from dotenv import load_dotenv

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS

load_dotenv()

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_tavily import TavilySearch
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda

from langchain_anthropic import ChatAnthropic

from schema import AgentResponse

tools = [TavilySearch()]

llm = ChatAnthropic(
    model="claude-3-5-sonnet-latest",
    temperature=0,
    max_tokens=512
)

react_prompt = hub.pull("hwchase17/react")
output_parser = PydanticOutputParser(pydantic_object=AgentResponse)
react_prompt_with_format_instructions = PromptTemplate(
    input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
    template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
    partial_variables={
        "format_instructions": output_parser.get_format_instructions()
    },
).partial(format_instructions=output_parser.get_format_instructions())


agent = create_react_agent(llm, tools, prompt=react_prompt_with_format_instructions)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=False)
extract_output = RunnableLambda(lambda x: x['output'])
output_output = RunnableLambda(lambda x: output_parser.parse(x))
chain = agent_executor | extract_output | output_output

def main():
    result = chain.invoke(
        input={
            "input": "Search for top 3 indian players in ICC ODI batting rankings",
        }
    )

    print('------------------- Player Names -------------------')
    print(result.playersName)


if __name__ == "__main__":
    main()
