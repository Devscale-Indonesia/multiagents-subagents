from agents import Agent


def get_agent():
    booking_agent = Agent(
        name="Booking Agent",
        instructions="Answer only booking questions: dates, rooms, changes, and cancellations.",
        model="gpt-5.4-mini",
    )

    refund_agent = Agent(
        name="Refund Agent",
        instructions="Answer only refund questions: eligibility, timing, and next steps.",
        model="gpt-5.4-mini",
    )

    return Agent(
        name="Customer Manager",
        instructions=(
            "You are the manager agent. Keep control of the conversation and give "
            "the final answer to the user. Use a specialist tool only when the "
            "question is clearly about booking or refunds."
        ),
        model="gpt-5.4-mini",
        tools=[
            booking_agent.as_tool(
                tool_name="booking_expert",
                tool_description="Use for booking, rescheduling, or cancellation questions.",
            ),
            refund_agent.as_tool(
                tool_name="refund_expert",
                tool_description="Use for refund policy or refund status questions.",
            ),
        ],
    )
