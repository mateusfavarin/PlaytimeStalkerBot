import requests as r
from time import time
from datetime import date, datetime
from bs4 import BeautifulSoup

INFINITY = 9999999999

class Exophase:

    def __init__(self):
        self.platforms = None
        self.game = None

    def set_platforms(self, platforms):
        self.platforms = platforms
        return (", ".join(platforms))+" set successfully."

    def set_game(self, query):
        game_query = "+".join(query)
        url = "https://api.exophase.com/public/archive/games?q="+game_query
        source = r.get(url).json()
        if source["games"]:
            game_name = " ".join(query)
            platforms = set()
            found = False
            for game in source["games"]["list"]:
                if game["title"].lower() == game_name.lower():
                    found = True
                    game_name = game["title"]
                    platforms.add(game["environment_slug"])
            if found:
                self.game = game_name
                self.set_platforms(tuple(platforms))
                return self.game+" set successfully for platforms: "+", ".join(platforms)+"."
            else:
                return "Game not found. Here are possible matches:\n\n"+self.find_game(query)

        return "Failed, game is not in exophase database"

    def find_game(self, game_query):
        game_query = "+".join(game_query)
        url = "https://api.exophase.com/public/archive/games?q="+game_query
        source = r.get(url).json()
        if not source["games"]:
            return "Game not found."
        games = []
        data = ""
        for game in source["games"]["list"]:
            if game["title"] not in games:
                games.append(game["title"])
                data += game["title"]+"\n"
        return data

    def get_earliest_trophy_date(self, game_data):
        game_url = game_data.find_parent("a")["href"]
        player_id = game_url[game_url.find("#") + 1 :]

        game_id = game_data.find_parent("li")["data-gameid"]

        url = "https://api.exophase.com/public/player/"+player_id+"/game/"+game_id+"/earned"
        source = r.get(url).json()

        earliest_trophy = INFINITY
        for trophy in source["list"]:
            if trophy["timestamp"] != 0 and trophy["timestamp"] < earliest_trophy:
                earliest_trophy = trophy["timestamp"]

        return earliest_trophy

    def stalk(self, player, user_list):
        if self.game is None:
            return "Game not set. Please use `!find gamename` to find a game in the exophase database, and set the game using `!set gamename`."

        playtime = 0
        acc_count = 0
        gaming_since = INFINITY
        player_exists = False
        for username in user_list:
            for console in self.platforms:
                url = "https://www.exophase.com/"+console+"/user/"+username
                source = r.get(url).text
                soup = BeautifulSoup(source, "html.parser")
                game_data = soup.find(string=self.game)
                if game_data is not None:
                    player_exists = True
                    hours_played = game_data.find_parent("li")["data-playtime"]
                    playtime += float(hours_played)
                    acc_count += 1
                    earliest_trophy = self.get_earliest_trophy_date(game_data)
                    if earliest_trophy < gaming_since:
                        gaming_since = earliest_trophy
                else:
                    if not player_exists:
                        page_exists = soup.find(string="Page Not Found")
                        if page_exists is None:
                            player_exists = True

            if not player_exists:
                return username+" is not in exophase."

            if playtime == 0:
                return username+" has not played "+self.game+"."


        data = "**Game: "+self.game+"**\n"
        data += "Player: "+player+"\n"
        data += "Accounts: "+str(acc_count)+"\n"

        if gaming_since != INFINITY:
            today = datetime.fromtimestamp(int(time()))
            first_day = datetime.fromtimestamp(gaming_since)
            days_playing = (today - first_day).days
            avg_playtime = playtime / days_playing

            data += "Playing since: "+str(first_day.day)+"/"+str(first_day.month)+"/"+str(first_day.year)+"\n"
            data += ("\nTotal playtime: %.2fh" % playtime)+"\n"
            if avg_playtime > 2:
                data += ("Average daily time played: %.2fh. Get a life!\n" % avg_playtime)
            else:
                data += ("Average daily time played: %.2fh.\n" % avg_playtime)

        else:
            data += ("\nTotal playtime: %.2fh" % playtime)+"\n"

        data += "\nData extracted from exophase. Times may be inaccurate."
        return data