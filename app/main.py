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


def format_tool_output(output):
    text = str(output).strip()
    if len(text) > 180:
        text = f"{text[:177]}..."
    return f"Tool output: {text}"


def format_handoff_call(raw):
    name = getattr(raw, "name", "unknown")
    return f"Handoff requested: {name}"


async def run_agent():
    active_agent = get_agent()
    session = SQLAlchemySession.from_url(
        "default",
        url=DATABASE_URL,
        create_tables=True,
    )

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in {"exit", "quit"}:
            break

        runner = Runner.run_streamed(active_agent, input=user_input, session=session)

        current_agent_name = active_agent.name
        print(f"{active_agent.name}: ", end="", flush=True)
        async for event in runner.stream_events():
            if event.type == "raw_response_event" and isinstance(
                event.data, ResponseTextDeltaEvent
            ):
                print(event.data.delta, end="", flush=True)
            elif event.type == "agent_updated_stream_event":
                if event.new_agent.name != current_agent_name:
                    current_agent_name = event.new_agent.name
                    print(
                        f"\nActive agent: {current_agent_name}",
                        end="\n\n",
                        flush=True,
                    )
            elif event.type == "run_item_stream_event":
                if event.item.type == "handoff_call_item":
                    raw = event.item.raw_item
                    print(
                        f"\n{format_handoff_call(raw)}",
                        end="\n\n",
                        flush=True,
                    )
                elif event.item.type == "handoff_output_item":
                    print(
                        f"\nHandoff: {event.item.source_agent.name} "
                        f"-> {event.item.target_agent.name}",
                        end="\n\n",
                        flush=True,
                    )
                elif event.item.type == "tool_call_item":
                    raw = event.item.raw_item
                    if getattr(raw, "name", "").startswith("transfer_to_"):
                        continue
                    print(
                        f"\n{format_tool_call(raw)}",
                        end="\n\n",
                        flush=True,
                    )
                elif event.item.type == "tool_call_output_item":
                    print(
                        f"\n{format_tool_output(event.item.output)}",
                        end="\n\n",
                        flush=True,
                    )
        active_agent = runner.last_agent
        print()


if __name__ == "__main__":
    run(run_agent())
