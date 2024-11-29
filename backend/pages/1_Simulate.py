import streamlit as st
import copy
import random

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

        print("----------------------------------------------")
        print("POSITION: ", positions[i])
        for j in range(len(people)):
            index = random.randint(0, len(temp_people) - 1)
            rating = tiers[j][random.randint(0, len(tiers[j]) - 1)]

            output = f"#{j + 1}. {temp_people[index]}: pick a player with a rating <= {rating}" if positions[i] != "TEAM" else (temp_people[index])
            
            if i == 0:
                picks[0].append(temp_people[index])
            else:
                picks[i].append([temp_people[index], rating])

            print(output)
            temp_people.pop(index)

        print("----------------------------------------------")
    return picks

print(player_names)
print(type(player_names))

if num_players and player_names:
    st.title("⚽ FIFA Tournament Simulation")

    st.header("🎮 **Draft Order**")
    # Add your tournament simulation logic here.
    #positions lists for different formations
    FOUR_THREE_THREE = ["TEAM", "GK", "LB", "CB", "CB", "RB", "CM", "CM", "CM", "LW", "ST", "RW"]
    FOUR_FOUR_TWO = ["TEAM", "GK", "LB", "CB", "CB", "RB", "LM", "CM", "CM", "RM", "ST", "ST"]
    THREE_FIVE_TWO = ["TEAM", "GK", "CB", "CB", "CB", "LM", "CM", "CM", "RM", "LW", "ST", "RW"]

    positions = FOUR_THREE_THREE
    
    tier = [
            [89, 90, 91, 92, 93, 94],
            [85, 86, 87, 88],
            [81, 82, 83, 84],
            [80]]

    picks = create_player_picks(tier, player_names, positions)
    
    # display the picks in tabs
    tabs = st.tabs(positions)

    for i, tab in enumerate(tabs):
        with tab:
            if i == 0:
                st.subheader("Team Picking Order")
                for j in range(num_players):
                    st.write(f"#{j + 1}. {picks[i][j]}")
            else:
                st.subheader(f"Draft for {positions[i]}")
                for j in range(num_players):
                    st.write(
                        f"#{j + 1}. {picks[i][j][0]} can pick a player with a rating ≤ {picks[i][j][1]}"
                    )
else:
    st.error("No data found. Please go back to the home page and set up the tournament.")
