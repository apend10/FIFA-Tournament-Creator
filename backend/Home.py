import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="FIFA Tournament Simulator", layout="centered")

# Landing page content
st.title("🏆 FIFA Tournament Simulator")

st.subheader("Welcome to the FIFA Tournament Simulator!")
st.write("Simulate your FIFA tournament with ease. Get started by specifying the number of players.")

# Input for the number of players
num_players = st.number_input(
    "How many players will participate?", 
    min_value=3, 
    max_value=8, 
    value=4, 
    step=1, 
    help="Enter the number of players participating in the tournament (3 to 8)."
)

# Input for the player names
st.write("### Enter Player Names")
player_names = []
for i in range(num_players):
    player_name = st.text_input(f"Player {i + 1} Name:", key=f"player_{i}")
    player_names.append(player_name)

# Proceed button
if st.button("Enter"):
    if all(player_names):
        # Store the data in session state
        st.session_state["num_players"] = num_players
        st.session_state["player_names"] = player_names

        st.success("To proceed, to the next step, please go to the simulate page!")
    else:
        st.error("Please fill in all player names before proceeding.")

# Footer or additional info
st.markdown("---")
st.caption("Powered by Streamlit | © 2024 FIFA Tournament Simulator")