import espn_api.requests.espn_requests

import config
from espn_api.football import League
import sys
import pandas as pd
import json
import pprint


# def get_player_card(league, playerIds, max_scoring_period):
#     '''Gets the player card'''
#     params = {'view': 'kona_playercard'}
#
#     additional_value = ["00{}".format(league.year), "10{}".format(league.year)]
#
#     filters = {'players': {'filterIds': {'value': playerIds},
#                            'filterStatsForTopScoringPeriodIds': {'value': max_scoring_period,
#                                                                  'additionalValue': additional_value}}}
#     headers = {'x-fantasy-filter': json.dumps(filters)}
#
#     data = league.league_get(params=params, headers=headers)
#     return data

# pp.pprint(get_player_card(league.espn_request, [players[110].playerId], 100000))

def get_player_stats():
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
                                                  'Projected Points': player.projected_total_points, 'Sentiment': 0,
                                                  "NumOfDataPoints": 0, "Average Sentiment": 0,
                                                  "Most Positive Comment": "", "Most Positive Comment Score": 0,
                                                  "Most Negative Comment": "", "Most Negative Comment Score": 0},
                                                 index=[0])], axis=0, ignore_index=True)
    return data


if __name__ == '__main__':
    print(get_player_stats())
