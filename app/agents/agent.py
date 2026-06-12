from agents import Agent


def get_agent():
    sql_agent = Agent(
        name="SQL Agent",
        instructions="Help students with database design, queries, joins, and indexes.",
        model="gpt-5.4-mini",
    )

    python_agent = Agent(
        name="Python Agent",
        instructions="Help students with Python syntax, debugging, and small scripts.",
        model="gpt-5.4-mini",
    )

    git_agent = Agent(
        name="Git Agent",
        instructions="Help students with commits, branches, merges, and pull requests.",
        model="gpt-5.4-mini",
    )

    return Agent(
        name="Bootcamp Assistant",
        instructions=(
            "Route each student question to the predefined specialist that best "
            "matches the topic. Ask a short clarifying question if the topic is unclear."
        ),
        model="gpt-5.4-mini",
        handoffs=[sql_agent, python_agent, git_agent],
    )
