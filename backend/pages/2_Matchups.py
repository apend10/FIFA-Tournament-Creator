import streamlit as st
import random
from itertools import combinations
import pandas as pd

st.title("🤺 Matchups")
st.header("League Phase")
st.write("All players will first play each other once. The top players will then compete against each other in a tournament-style bracket.")

#-------------------------------------------------------------------------------------------------------------------------------------
# Generate Matchups
#-------------------------------------------------------------------------------------------------------------------------------------
player_names = st.session_state.get("player_names", None)
num_players = st.session_state.get("num_players", None)

def generate_matchups():
    matchups = list(combinations(player_names, 2)) 
    random.shuffle(matchups)
    team1, team2 = zip(*matchups)
    return [team1, team2]

# Initialize matchups and matchup_df in session state if not already done
if "matchups" not in st.session_state:
    st.session_state["matchups"] = generate_matchups()

# Store matchup DataFrame in session state
if "matchup_df" not in st.session_state:
    matchups = st.session_state["matchups"]
    st.session_state["matchup_df"] = pd.DataFrame({
        "Home Team": matchups[0],
        "Away Team": matchups[1],
        "Score (Home)": [""] * len(matchups[0]),  
        "Score (Away)": [""] * len(matchups[1])
    })

matchup_df = st.session_state["matchup_df"]

# Show all matchups in a table
st.write("### All Matchups")
st.table(matchup_df)

# Show current game being played
if "current_game" not in st.session_state:
    st.session_state["current_game"] = 0

current_game = st.session_state["current_game"]

# Display current game and score input
if current_game < (num_players * (num_players - 1)) / 2:
    st.write(f"### Enter score for Game {current_game + 1} - {matchup_df.loc[current_game, 'Home Team']} vs. {matchup_df.loc[current_game, 'Away Team']}")

    # Layout for score input
    cols = st.columns([3, 3])

    home_score = cols[0].number_input(
        f"Score for {matchup_df.loc[current_game, 'Home Team']} (Home)", 
        min_value=0, 
        value=0, 
        step=1, 
        key=f"home_score_{current_game}"
    )

    away_score = cols[1].number_input(
        f"Score for {matchup_df.loc[current_game, 'Away Team']} (Away)", 
        min_value=0, 
        value=0, 
        step=1, 
        key=f"away_score_{current_game}"
    )

    # Button to record the game
    if st.button(f"Record Game {current_game + 1} Score"):
        if home_score >= 0 and away_score >= 0:
            st.success("The game has been recorded.")
            # Update the scores in session state
            st.session_state["matchup_df"].loc[current_game, 'Score (Home)'] = home_score
            st.session_state["matchup_df"].loc[current_game, 'Score (Away)'] = away_score
            
            # Move to the next game
            st.session_state["current_game"] += 1
        else:
            st.error("Please enter valid scores for both teams.")
else:
    st.write("### All games have been recorded!")

st.divider()
st.write("### League Table")
st.session_state["league_table"] = pd.DataFrame({
        "Teams" : player_names,
        "Points": [0] * num_players,  
        "Goal Difference": [0] * num_players
    })

for i in range(len(matchup_df)):
    home_index = st.session_state["league_table"]["Teams"].to_list().index(matchup_df['Home Team'][i])
    away_index = st.session_state["league_table"]["Teams"].to_list().index(matchup_df['Away Team'][i])
    
    #Tie
    if matchup_df['Score (Home)'][i] == matchup_df['Score (Away)'][i]:
        st.session_state["league_table"].loc[home_index, "Points"] += 1
        st.session_state["league_table"].loc[away_index, "Points"] += 1

    else:
        difference = int(matchup_df['Score (Home)'][i] - matchup_df['Score (Away)'][i])
        #home team won
        if difference > 0:
            st.session_state["league_table"].loc[home_index, "Points"] += 3
            st.session_state["league_table"].loc[home_index, "Goal Difference"] += difference

            st.session_state["league_table"].loc[away_index, "Goal Difference"] -= difference
        #away team won
        else:
            st.session_state["league_table"].loc[away_index, "Points"] += 3
            st.session_state["league_table"].loc[away_index, "Goal Difference"] -= difference

            st.session_state["league_table"].loc[home_index, "Goal Difference"] += difference

st.session_state['league_table'].sort_values(by=['Points', 'Goal Difference'], ascending=False, inplace=True)
st.session_state['league_table'] = st.session_state['league_table'].set_index("Teams")
st.table(st.session_state.get("league_table", None))
