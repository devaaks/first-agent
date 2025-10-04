"""
First Agent - A modular implementation of an AI agent for searching player information.

This module provides a clean, modular implementation of a ReAct agent that can search
for information using various tools and return structured responses.
"""

import json
import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

from langchain import hub
from langchain.agents import AgentExecutor
from langchain.agents.react.agent import create_react_agent
from langchain_anthropic import ChatAnthropic
from langchain_core.output_parsers.pydantic import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_tavily import TavilySearch

from prompt import REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS
from schema import AgentResponse


class SearchAgentConfig:
    """Configuration class for the First Agent."""
    
    def __init__(
        self,
        model_name: str = "claude-3-5-sonnet-latest",
        temperature: float = 0.0,
        max_tokens: int = 512,
        verbose: bool = False
    ):
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.verbose = verbose


class SearchAgent:
    """
    A ReAct agent for searching information with structured output.
    
    This agent can search the internet using various tools and return responses
    in a structured format defined by the AgentResponse schema.
    """
    
    def __init__(self, config: SearchAgentConfig):
        """
        Initialize the First Agent.
        
        Args:
            config: Configuration object containing agent settings
        """
        self.config = config
        self._load_environment()
        self._setup_components()
    
    def _load_environment(self) -> None:
        """Load environment variables from .env file."""
        load_dotenv()
    
    def _setup_components(self) -> None:
        """Set up all agent components: LLM, tools, prompts, and agent."""
        self.tools = self._create_tools()
        self.llm = self._create_llm()
        self.structured_llm = self._create_structured_llm()
        self.prompt = self._create_prompt()
        self.agent_executor = self._create_agent_executor()
        self.chain = self._create_chain()
    
    def _create_tools(self) -> List[Any]:
        """Create and return the list of tools available to the agent."""
        return [TavilySearch()]
    
    def _create_llm(self) -> ChatAnthropic:
        """Create and configure the language model."""
        return ChatAnthropic(
            model=self.config.model_name,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
    
    def _create_structured_llm(self) -> Any:
        """Create a structured LLM that returns validated Pydantic objects."""
        return self.llm.with_structured_output(AgentResponse)
    
    def _create_prompt(self) -> PromptTemplate:
        """Create the prompt template with format instructions."""
        # Pull the base ReAct prompt from LangChain hub
        # react_prompt = hub.pull("hwchase17/react")
        
        # Create custom prompt with format instructions
        return PromptTemplate(
            input_variables=["tools", "tool_names", "input", "agent_scratchpad"],
            template=REACT_PROMPT_WITH_FORMAT_INSTRUCTIONS,
        ).partial(format_instructions='')
    
    def _create_agent_executor(self) -> AgentExecutor:
        """Create the agent and its executor."""
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=self.prompt
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=self.config.verbose
        )
    
    def _create_chain(self) -> Any:
        """Create the complete chain with structured output."""
        extract_output = RunnableLambda(lambda x: x['output'])
        return self.agent_executor | extract_output | self.structured_llm
    
    def search(self, query: str) -> AgentResponse:
        """
        Execute a search query using the agent.
        
        Args:
            query: The search query to execute
            
        Returns:
            AgentResponse object with structured output
        """
        try:
            result = self.chain.invoke({"input": query})
            return result
        except Exception as e:
            # Return a default AgentResponse on error
            return AgentResponse(
                answer=f"Error occurred during search: {str(e)}",
                playersName=[]
            )


class ResultProcessor:
    """Utility class for processing and displaying agent results."""
    
    @staticmethod
    def display_result(result: AgentResponse) -> None:
        """
        Display the complete result in a formatted way.
        
        Args:
            result: The AgentResponse object to display
        """
        print("=" * 60)
        print("AGENT SEARCH RESULTS")
        print("=" * 60)
        
        # Display answer if available
        if result.answer:
            print(f"\nAnswer: {result.answer}")
        
        # Display players if available
        if result.playersName:
            print(f"\n{'─' * 40}")
            print(f"Players Found: {len(result.playersName)}")
            print(f"{'─' * 40}")
            for i, player in enumerate(result.playersName, 1):
                print(f"  {i}. {player}")
        
        print("\n" + "=" * 60)


def create_default_agent() -> SearchAgent:
    """
    Create a First Agent with default configuration.
    
    Returns:
        Configured SearchAgent instance
    """
    config = SearchAgentConfig(
        model_name="claude-3-5-sonnet-latest",
        temperature=0.0,
        max_tokens=512,
        verbose=False
    )
    return SearchAgent(config)


def main() -> None:
    """Main function to demonstrate the First Agent."""
    # Create agent with default configuration
    agent = create_default_agent()
    
    # Define the search query
    query = "Search for top 3 indian players in ICC ODI batting rankings"
    
    # Execute the search
    print("🔍 Starting search...")
    result = agent.search(query)
    
    # Display results
    ResultProcessor.display_result(result)
    
    # Additional processing example
    if result.playersName:
        print(f"📊 Summary: Found {len(result.playersName)} players")
        for player in result.playersName:
            print(f"   • {player}")


if __name__ == "__main__":
    main()