from agents import Agent

from app.agents.prompts import AGENT_INSTRUCTIONS
from app.agents.tools import (
    crawl_web,
    execute_command,
    extract_web,
    search_web,
    write_file,
)


def get_agent():
    return Agent(
        name="Assistant",
        instructions=AGENT_INSTRUCTIONS,
        model="gpt-5.4-mini",
        tools=[search_web, extract_web, crawl_web, write_file, execute_command],
    )
