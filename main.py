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
chain = agent_executor

def main():
    result = chain.invoke(
        input={
            "input": "Search for top 3 indian players in ICC ODI batting rankings",
        }
    )

    try:
        output_data = json.loads(result['output'])
        players_name = output_data.get('playersName', [])
        
        print('------------------- Players Info -------------------')
        print("Players Name:", players_name)
        print("Number of players:", len(players_name))
        
        # Print each player individually
        for i, player in enumerate(players_name, 1):
            print(f"{i}. {player}")
            
    except json.JSONDecodeError:
        print("Error: Could not parse the output as JSON")
    except KeyError as e:
        print(f"Error: Key {e} not found in the result")


if __name__ == "__main__":
    main()
