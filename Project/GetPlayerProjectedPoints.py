import config
from espn_api.football import League
import pandas as pd


# Get a player's stats for a specific week
def __get_player_stats(player, week):
    if player.stats is not None and player.stats.get(week) is not None \
            and player.stats.get(week).get('points') is not None:
        return player.stats.get(week).get('points')
    return 0


# Get every player's stats for a specific week
def get_players_stats(week):
    league = League(league_id=config.league_id, year=2022, swid=config.swid,
                    espn_s2=config.espn_s2)
    data = pd.DataFrame(columns=['Full Name', 'First Name', 'Last Name', 'Projected Points', 'Sentiment',
                                 'NumOfDataPoints', 'Average Sentiment', 'Most Positive Comment',
                                 'Most Positive Comment Score', 'Most Negative Comment', 'Most Negative Comment Score'])
    ids = []
    for player in league.espn_request.get_pro_players():
        if float(player['ownership']['percentOwned']) > 0.1:
            ids.append(player['id'])

    players = league.player_info(playerId=ids)
    for player in players:
        name = player.name.split()
        if name[1] != "D/ST":
            data = pd.concat([data, pd.DataFrame({'Full Name': player.name, 'First Name': name[0], 'Last Name': name[1],
                                                  "Position": player.position,
                                                  "Actual Points": __get_player_stats(player, week),
                                                  'Projected Points': player.projected_total_points, 'Sentiment': 0,
                                                  "NumOfDataPoints": 0,
                                                  "Most Positive Comment": "", "Most Positive Comment Score": 0,
                                                  "Most Negative Comment": "", "Most Negative Comment Score": 0},
                                                 index=[0])], axis=0, ignore_index=True)
    return data


if __name__ == '__main__':
    print(get_players_stats(10))
