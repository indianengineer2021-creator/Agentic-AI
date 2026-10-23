"""Streamlit UI for the AI Travel Planning Multi-Agent System."""

from __future__ import annotations

import streamlit as st

from graph.workflow import run_workflow


st.set_page_config(page_title="AI Travel Planner", page_icon="✈️", layout="wide")


def render_plan(result: dict) -> None:
    """Render the final structured plan in the Streamlit UI."""
    st.title("AI Travel Planner")
    final_plan = result.get("final_plan") or {}
    if not final_plan:
        st.warning("No final plan is available yet. Check the workflow output or API configuration.")
        return

    st.subheader("✈️ Flights")
    flight = final_plan.get("flight_recommendation") or {}
    if flight:
        st.write(f"Airline: {flight.get('airline', 'N/A')}")
        st.write(f"Estimated cost: ₹{flight.get('estimated_cost', 0):,.0f}")
        st.write(f"Notes: {flight.get('notes', '')}")

    st.subheader("🏨 Hotels")
    hotel = final_plan.get("hotel_recommendation") or {}
    if hotel:
        st.write(f"Category: {hotel.get('category', 'N/A')}")
        st.write(f"Estimated nightly rate: ₹{hotel.get('estimated_cost_per_night', 0):,.0f}")
        st.write(f"Notes: {hotel.get('notes', '')}")

    st.subheader("🎯 Activities")
    for activity in final_plan.get("activities", []):
        st.write(f"- {activity}")

    st.subheader("💰 Budget")
    budget = final_plan.get("budget") or {}
    st.write(f"Total estimated cost: ₹{budget.get('total_estimated_cost', 0):,.0f}")
    st.write(f"Remaining budget: ₹{budget.get('remaining_budget', 0):,.0f}")
    st.write(f"Budget utilization: {budget.get('utilization_percent', 0):.1f}%")

    st.subheader("🗓️ Itinerary")
    for item in final_plan.get("itinerary", []):
        st.write(f"### {item.get('title', 'Day')}")
        for activity in item.get("activities", []):
            st.write(f"- {activity}")

    st.subheader("📚 Travel Information")
    for info in final_plan.get("travel_tips", []):
        st.write(f"- {info}")

    st.subheader("⚠️ Risks")
    for risk in final_plan.get("risks", []):
        st.write(f"- {risk}")

    st.subheader("🔍 AI Review")
    st.write(final_plan.get("review_summary", "Review not available."))
    review = result.get("review") or {}
    if review.get("provider") == "groq":
        st.caption(f"Reviewed by Groq ({review.get('model', 'configured model')}).")
    else:
        st.caption("Reviewed with rule-based checks. Set GROQ_API_KEY to enable Groq analysis.")
    for issue in review.get("issues", []):
        st.warning(issue)
    for warning in review.get("warnings", []):
        st.info(warning)
    for suggestion in review.get("suggestions", []):
        st.write(f"Suggestion: {suggestion}")

    st.subheader("🤖 Agent Execution Summary")
    st.write(result.get("workflow_status", "complete"))


def main() -> None:
    """Render the travel planner interface."""
    st.sidebar.title("Trip Details")
    origin = st.sidebar.text_input("Origin", value="Chennai")
    destination = st.sidebar.text_input("Destination", value="Singapore")
    travel_dates = st.sidebar.text_input("Travel dates", value="Flexible dates")
    duration = st.sidebar.number_input("Duration (days)", min_value=1, max_value=30, value=4)
    travelers = st.sidebar.number_input("Travelers", min_value=1, max_value=10, value=2)
    budget = st.sidebar.number_input("Budget", min_value=1000, step=1000, value=100000)
    currency = st.sidebar.selectbox("Currency", ["INR", "USD", "SGD", "EUR"])
    interests = st.sidebar.text_input("Interests", value="sightseeing, food, shopping")
    hotel_preference = st.sidebar.selectbox("Hotel preference", ["budget", "mid-range", "premium", "luxury"], index=1)
    activity_preference = st.sidebar.text_input("Activity preference", value="Sightseeing")

    st.title("AI Travel Planner")
    st.write("Plan a realistic travel itinerary using a multi-agent workflow and mock travel data.")

    if st.button("Plan My Trip"):
        user_request = (
            f"I want to travel from {origin} to {destination} for {duration} days for {travelers} people "
            f"with a budget of {currency} {budget}. I like {interests}. I prefer a {hotel_preference} hotel."
        )
        with st.spinner("Running the supervisor and agent workflow..."):
            result = run_workflow(user_request)
        render_plan(result)


if __name__ == "__main__":
    main()
