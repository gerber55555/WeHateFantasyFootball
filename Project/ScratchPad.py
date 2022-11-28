from GetSentimentForTopPlayers import get_sentiment_for_top_players
from espn_api.football import League
import config
if __name__ == '__main__':
    league = League(league_id=config.league_id, year=2022, swid=config.swid,
                    espn_s2=config.espn_s2)

    print(league.current_week)
    number_of_players = 250
    for week in range(1, league.current_week):
        get_sentiment_for_top_players(number_of_players, week, None)

