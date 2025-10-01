from typing import List
from pydantic import BaseModel, Field

class Source(BaseModel):
    """Schema for a source used by the agent."""

    url: str = Field(description="The URL of the source.")

class AgentResponse(BaseModel):
    """Schema for the agent's response."""

    answer: str = Field(description="The agent's answer to the query.")
    playersName: List[str] = Field(default_factory=list, description="List of players' names used to generate the answer.")