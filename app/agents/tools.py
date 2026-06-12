import os
import subprocess
from pathlib import Path

from agents import function_tool
from tavily import TavilyClient

SANDBOX_DIR = Path(".sandbox").resolve()
tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def _sandbox_path(path: str) -> Path:
    target = (SANDBOX_DIR / path).resolve()
    if not target.is_relative_to(SANDBOX_DIR):
        raise ValueError("Path must stay inside .sandbox")
    return target


@function_tool
def search_web(query: str):
    """Search the web using Tavily."""
    return tavily_client.search(query=query, max_results=5, include_answer=True)


@function_tool
def extract_web(url: str):
    """Extract content from a web page using Tavily."""
    return tavily_client.extract(urls=url)


@function_tool
def crawl_web(url: str, instructions: str):
    """Crawl a website using Tavily."""
    return tavily_client.crawl(url=url, instructions=instructions, limit=10)


@function_tool
def write_file(path: str, content: str):
    """Write a file inside .sandbox."""
    target = _sandbox_path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content)
    return f"Wrote {target}"


@function_tool
def execute_command(command: str):
    """Run a shell command from .sandbox."""
    result = subprocess.run(
        command,
        shell=True,
        cwd=SANDBOX_DIR,
        capture_output=True,
        text=True,
        timeout=30,
    )
    return {
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
