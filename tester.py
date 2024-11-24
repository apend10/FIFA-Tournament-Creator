import random 

people = ["Athul", "Sankar", "Vivek", "Pendi"]
positions = ["TEAM", "GK", "LB", "CB", "CB", "RB", "CM", "CM", "CM", "LW", "ST", "RW"]

def create_fixtures(people):
    #Home, Away, Score, Winner
    games = []

    while len(games) < 12:
        temp_people = people

        #pick random home team
        home_team = random.randint(0, len(people) - 1)
        people.pop(home_team)
        away_team = random.randint(0, len(people) - 1)

        away_team = temp_people[away_team]
        home_team = people[home_team]

        if([away_team, home_team] in gamaes or [home_team, away_team] in games):
            


    
def create_player_picks():
    tier = [
        [87, 88, 89, 90, 91, 92, 93, 94],
        [84, 85, 86],
        [80, 81, 82, 83],
        [79]
    ]

    for i in positions:
        people = ["Athul", "Sankar", "Vivek", "Pendi"]

        print("----------------------------------------------")
        print("POSITION: ", i)
        for j in range(4):
            index = random.randint(0, len(people) - 1)
            rating = tier[j][random.randint(0, len(tier[j]) - 1)]

            output = f"#{j + 1}. {people[index]}: pick a player with a rating <= {rating}" if i != "TEAM" else (people[index])
            print(output)
            people.pop(index)

        print("----------------------------------------------")
