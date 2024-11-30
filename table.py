import pandas as pd

games = [
    ["Pendi", "Shankar", "Pendi", 1, 0],
    ["Athul", "Vivek", "Athul", 3, 1],
    ["Athul", "Shankar", "Athul", 8, 0],
    ["Pendi", "Vivek", "Pendi", 2, 0],
    ["Vivek", "Shankar", "Shankar", 2, 0],
    ["Athul", "Pendi", "Pendi", 1, 2]
]


def create_table():
    points = {
        "Pendi" : 0, 
        "Shankar" : 0, 
        "Vivek" : 0,
        "Athul" : 0
    }

    gd = {
        "Pendi" : 0, 
        "Shankar" : 0, 
        "Vivek" : 0,
        "Athul" : 0
    }


    for game in games:
        #assign points and goal difference
        if game[2] != "Tie":
            points[game[2]] += 3
            gd_game = abs(game[4] - game[3])

            #winner is at the first index
            if(game[0] == game[2]):
                gd[game[0]] += gd_game
                gd[game[1]] -= gd_game
            elif(game[1] == game[2]):
                gd[game[0]] -= gd_game
                gd[game[1]] += gd_game
        else:
            points[game[0]] += 1
            points[game[1]] += 1

    pointsdf =  pd.DataFrame([points]).T
    gddf = pd.DataFrame([gd]).T
    pointsdf.columns, gddf.columns = ["points"], ["goal difference"]
    pointsdf.index.name, gddf.index.name = "player", "player"

    table = pd.merge(left = pointsdf, right= gddf, how="inner", on="player", )
    table = table.sort_values(by=['points', 'goal difference'], ascending=False)
    
    print("-----------------------------------")
    print(table)
    print("-----------------------------------")

create_table()