from agents import Agent


def get_agent():
    billing_agent = Agent(
        name="Billing Agent",
        instructions="You handle invoices, payments, subscription changes, and refunds.",
        model="gpt-5.4-mini",
    )

    tech_agent = Agent(
        name="Tech Support Agent",
        instructions="You handle product bugs, login problems, and API issues.",
        model="gpt-5.4-mini",
    )

    return Agent(
        name="Triage Agent",
        instructions=(
            "Decide who should own the conversation. Handoff billing questions to "
            "Billing Agent and technical questions to Tech Support Agent. If the "
            "request is unclear, ask one short clarifying question."
        ),
        model="gpt-5.4-mini",
        handoffs=[billing_agent, tech_agent],
    )
