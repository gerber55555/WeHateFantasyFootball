import config
from espn_api.football import League


class Stats:
    def __init__(self):
        self.points = 0
        self.projectedPoints = 0


if __name__ == '__main__':
    league = League(league_id=config.league_id, year=2022, swid=config.swid,
                    espn_s2=config.espn_s2)
    data = {}
    for name in league.player_map.values():
        if player := league.player_info(name=name):
            data[name] = []
            for i in range(league.current_week):
                if len(player.stats) > 0:
                    if player.stats.get(i):
                        if points := player.stats.get(i).get('points'):
                            data[name].append(points)
                    else:
                        data[name].append(0)
    print(data)
