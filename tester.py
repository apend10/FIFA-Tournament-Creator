import random 

people = ["Athul", "Sankar", "Vivek", "Pendi"]
positions = ["TEAM", "GK", "LB", "CB", "CB", "RB", "CM", "CM", "CM", "LW", "ST", "RW"]

# def create_fixtures(people):
#     #Home, Away, Score, Winner
#     games = []

#     while len(games) < 12:
#         temp_people = people

#         #pick random home team
#         home_team = random.randint(0, len(people) - 1)
#         people.pop(home_team)
#         away_team = random.randint(0, len(people) - 1)

#         away_team = temp_people[away_team]
#         home_team = people[home_team]

#         if([away_team, home_team] in games or [home_team, away_team] in games):

picks = [[] for _ in range(12)]
print(picks)