from agents import Agent, handoff


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
        handoffs=[
            handoff(
                billing_agent,
                tool_name_override="transfer_to_billing_agent",
                tool_description_override="Hand off billing, payment, and refund questions.",
            ),
            handoff(
                tech_agent,
                tool_name_override="transfer_to_tech_support_agent",
                tool_description_override="Hand off product bug, login, and API questions.",
            ),
        ],
    )
