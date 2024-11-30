import streamlit as st
import copy
import random
import requests
import json
import pandas as pd

API_LINK = "https://drop-api.ea.com/rating/fc-24"

#gender
male = "gender=0"
female = "gender=1"

# Retrieve data from session state
num_players = st.session_state.get("num_players", None)
player_names = st.session_state.get("player_names", None)

#simulation logic
def create_player_picks(tiers:list, people:list, positions:list):
    # adjust tiers
    # explanation: tiers is made default for 4 players. If there are more, then the top 3 tiers stay the same
    # and there are more 4th tiers created
    for _ in range(len(people) - 4):
        tiers.append(tiers[-1])

    picks = [[] for _ in range(12)]
    for i in range(len(positions)):
        temp_people = copy.deepcopy(people)

        for j in range(len(people)):
            index = random.randint(0, len(temp_people) - 1)
            rating = tiers[j][random.randint(0, len(tiers[j]) - 1)]

            output = f"#{j + 1}. {temp_people[index]}: pick a player with a rating <= {rating}" if positions[i] != "TEAM" else (temp_people[index])
            
            if i == 0:
                picks[0].append(temp_people[index])
            else:
                picks[i].append([temp_people[index], rating])

            temp_people.pop(index)
    return picks

def filter(selected_positions:list):
    position_abbreviation_full_form_conversion = {
        "GK" : "0",
        "LB" : "7",
        "RB" : "3",
        "CB" : "5",
        "CDM" : "10",
        "CM" : "14",
        "CAM" : "18",
        "LM" : "16",
        "RM" : "12",
        "LW" : "27",
        "RW" : "23",
        "ST" : "25"
    }

    selected_positions_str = ""
    for i in range(len(selected_positions)):
        selected_positions_str += position_abbreviation_full_form_conversion[selected_positions[i]]
        if i != len(selected_positions) - 1:
           selected_positions_str += ","

    response = requests.get(f"{API_LINK}?position={selected_positions_str}&{male}")
    print(f"{API_LINK}?position={selected_positions_str}&{male}")
    jsonresponse = json.loads(response.text)
    
    overallRating = []
    name = []
    pac = []
    sho = []
    dri = []
    defend = []
    phy = []
    pas = []
    pic = []

    for i in range(len(jsonresponse["items"])):
      overallRating.append(jsonresponse["items"][i]["overallRating"])
      name.append(jsonresponse["items"][i]["firstName"] + " " + jsonresponse["items"][i]["lastName"])
      pac.append(jsonresponse["items"][i]["stats"]["pac"]["value"])
      sho.append(jsonresponse["items"][i]["stats"]["sho"]["value"])
      dri.append(jsonresponse["items"][i]["stats"]["dri"]["value"])
      defend.append(jsonresponse["items"][i]["stats"]["def"]["value"])
      phy.append(jsonresponse["items"][i]["stats"]["phy"]["value"])
      pas.append(jsonresponse["items"][i]["stats"]["pas"]["value"])
      pic.append(jsonresponse["items"][i]["shieldUrl"])
    
    result = pd.DataFrame({
       "Name" : name, 
       "Rating" : overallRating,
       "Picture" : pic,
       "PAC": pac,
       "SHO" : sho,
       "PAS" : pas,
       "DRI" : dri,
       "DEF" : defend,
       "PHY" : phy
    })

    return result

#---------------------------------------------------------------------------------------------------------------------------
# Draft Order
#---------------------------------------------------------------------------------------------------------------------------
if num_players and player_names:
    st.title("⚽ FIFA Tournament Simulation")

    st.header("🎮 **Draft Order**")
    # Add your tournament simulation logic here.
    
    tier = [
            [89, 90, 91, 92, 93, 94],
            [85, 86, 87, 88],
            [81, 82, 83, 84],
            [80]]

    positions = st.session_state.get("positions", None)
    if "picks" not in st.session_state:
        st.session_state["picks"] = create_player_picks(tier, player_names, positions)
    
    # display the picks in tabs
    position_tabs = st.tabs(positions)

    for i, tab in enumerate(position_tabs):
        with tab:
            if i == 0:
                st.subheader("Team Picking Order")
                for j in range(num_players):
                    st.markdown(
                    f"""
                    <div style="font-size:24px; margin-bottom:10px;">
                        <strong>#{j + 1}</strong>: 
                        <span style="color:tan;"><strong>{st.session_state["picks"] [i][j]}</strong></span> 
                    </div>
                    """, 
                    unsafe_allow_html=True)
            else:
                st.subheader(f"Draft for {positions[i]}")
                for j in range(num_players):
                    color = ""
                    if j == 0:
                        color = "green"
                    elif j == 1:
                        color = "lightgreen"
                    elif j == 2:
                        color = "orange"
                    else:
                        color = "red"
                    st.markdown(
                    f"""
                    <div style="font-size:24px; margin-bottom:10px;">
                        <strong>#{j + 1}</strong>: 
                        <span style="color:tan;"><strong>{st.session_state["picks"] [i][j][0]}</strong></span> 
                        can pick a player with a rating ≤ 
                        <span style="color:{color};"><strong>{st.session_state["picks"] [i][j][1]}</strong></span>
                    </div>
                    """, 
                    unsafe_allow_html=True)
#---------------------------------------------------------------------------------------------------------------------------
#Team Selection
#---------------------------------------------------------------------------------------------------------------------------
    st.divider()
    st.header("💪 **Team Selection**")

    # Set up player teams in session state if not yet done
    if "player_teams" not in st.session_state:
        st.session_state["player_teams"] = {pn: [[] for _ in range(11)] for pn in player_names}

    team_tabs = st.tabs(player_names)

    positions = positions[1:]
    
    def show_player_teams():
        # Create a placeholder for the entire section
        team_placeholders = {}

        for player, tab in zip(player_names, team_tabs):
            with tab:
                st.write(f"### {player}'s Team")
                # Create placeholders for each position in the team
                team_placeholders[player] = {}
                for p in positions:
                    placeholder = st.empty()  # Create a placeholder for each position
                    team_placeholders[player][p] = placeholder

        # Update placeholders dynamically
        for player in player_names:
            for p in positions:
                position_index = positions.index(p)
                player_team = st.session_state["player_teams"][player]
                with team_placeholders[player][p]:  # Access the placeholder dynamically
                    if player_team[position_index]:
                        st.write(f"{p}:")
                        st.image(player_team[position_index], width=100)
                    else:
                        st.write(f"{p}: None")
#---------------------------------------------------------------------------------------------------------------------------
# Completion Message
#---------------------------------------------------------------------------------------------------------------------------
    count = 0
    for player in st.session_state["player_teams"]:
        for i in st.session_state["player_teams"][player]:
            if len(i) > 1:
                count += 1
    print(count)
    if(count == num_players * 11):
        st.success("You've finished selecting teams, go to the Matchups tab to start playing!")

#---------------------------------------------------------------------------------------------------------------------------
# Market
#---------------------------------------------------------------------------------------------------------------------------
    st.divider()
    st.header("🤝 **Market**")
    
    selected_player = st.selectbox("Choose a participant:", player_names)
    selected_position = st.selectbox("Choose a position:", positions)

    st.subheader("Filters: ")
    
    # Options to choose from
    options = ["GK", "LB", "CB", "RB", "CDM", "CM", "CAM", "RW", "RM", "LW", "LM", "ST"]

    # Multiselect widget
    selected_positions = st.multiselect(
        "**Position**:",
        options=options,
        default=["ST"],  # Pre-selected options (optional)
        help="You can select multiple positions from the list to filter through all the players."
    )

    max_rating = st.number_input(
    "**Maximum Rating**:", 
    min_value=75, 
    max_value=95, 
    value=95, 
    step=1, 
    help="Select a number to filter for a max rating if necessary."
)

    if(len(selected_positions) > 0):
        result = filter(selected_positions)
        result = result[result["Rating"] <= max_rating]
        result = result.set_index("Rating")
        #st.table(result)

        # Function to display images
        def display_images(df):
            # Display the DataFrame with images instead of URLs
            for index, row in df.iterrows():
                st.image(row['Picture'], width=200)  # Display image next to the player name
                b = st.button(f"Select {row['Name']}")
                if(b):
                    print(f"{selected_player} chose {row['Name']} as their {selected_position}")
                    st.session_state["player_teams"][selected_player][positions.index(selected_position)] = row['Picture']
                    print(st.session_state["player_teams"])
                    st.success(f"{selected_player} chose {row['Name']} as their {selected_position}")
                    show_player_teams()


        # Display the player data with images
        display_images(result)    
else:
    st.error("No data found. Please go back to the home page and set up the tournament.")