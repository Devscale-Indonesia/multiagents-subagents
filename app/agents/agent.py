from agents import Agent, Runner, function_tool


def make_specialist(topic: str) -> Agent:
    return Agent(
        name=f"{topic} Specialist",
        instructions=(
            f"You are a specialist in {topic}. Stay inside that topic, "
            "answer concisely, and say when the task needs a different expert."
        ),
        model="gpt-5.4-mini",
    )


@function_tool
async def ask_dynamic_specialist(topic: str, task: str) -> str:
    """Create a temporary specialist for one narrow topic and ask it one task."""
    specialist = make_specialist(topic)
    result = await Runner.run(specialist, task)
    return result.final_output


def get_agent():
    return Agent(
        name="Dynamic Specialist Manager",
        instructions=(
            "Help the user directly for simple requests. For requests that need "
            "a specific expert, call ask_dynamic_specialist with a narrow topic."
        ),
        model="gpt-5.4-mini",
        tools=[ask_dynamic_specialist],
    )
