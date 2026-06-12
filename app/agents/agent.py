from agents import Agent, handoff


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
            "You are only a router. If the user asks to talk to the SQL, Python, "
            "or Git specialist, handoff immediately. For SQL, Python, or Git "
            "questions, always handoff to the matching predefined specialist "
            "instead of answering yourself. Ask a short clarifying question if "
            "the topic is unclear."
        ),
        model="gpt-5.4-mini",
        handoffs=[
            handoff(
                sql_agent,
                tool_name_override="transfer_to_sql_agent",
                tool_description_override="Hand off database and SQL questions.",
            ),
            handoff(
                python_agent,
                tool_name_override="transfer_to_python_agent",
                tool_description_override="Hand off Python programming questions.",
            ),
            handoff(
                git_agent,
                tool_name_override="transfer_to_git_agent",
                tool_description_override="Hand off Git workflow questions.",
            ),
        ],
    )
