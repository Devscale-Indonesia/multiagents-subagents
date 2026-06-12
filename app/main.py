import json
from asyncio import run

from agents import Runner
from agents.extensions.memory import SQLAlchemySession
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent

from app.agents.agent import get_agent
from app.core.settings import DATABASE_URL

load_dotenv()


def format_tool_call(raw):
    name = getattr(raw, "name", "unknown")
    arguments = getattr(raw, "arguments", "{}")

    try:
        arguments = json.loads(arguments)
    except json.JSONDecodeError:
        pass

    if name == "write_file" and isinstance(arguments, dict):
        arguments = {"path": arguments.get("path")}

    return f"Tool call: {name}({arguments})"


async def run_agent():
    agent = get_agent()
    session = SQLAlchemySession.from_url(
        "default",
        url=DATABASE_URL,
        create_tables=True,
    )

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        runner = Runner.run_streamed(agent, input=user_input, session=session)

        print("Assistant: ", end="", flush=True)
        async for event in runner.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                print(event.data.delta, end="", flush=True)
            elif event.type == "run_item_stream_event":
                if event.item.type == "tool_call_item":
                    raw = event.item.raw_item
                    print(
                        f"\n{format_tool_call(raw)}",
                        end="\n\n",
                        flush=True,
                    )
        print()


if __name__ == "__main__":
    run(run_agent())
