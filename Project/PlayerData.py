from espn_api.football import League


class Stats:
    def __init__(self):
        self.points = 0
        self.projectedPoints = 0


if __name__ == '__main__':
    league = League(league_id=1762995020, year=2022, swid='D938D5D5-02E5-410E-99E6-966D8A1264A5',
                    espn_s2='AECTfNOXTGsnkuzWmGzl8qPTJvWEZFAnFyzizK0ti7vPEwfEhw1OySXPtxK%2FnaQv39HpTz7SoWl29dohciZ2FMMmVGT5thcB5xQu%2FFwt4hX8jtZa9DgKBdQP2WRa07BCSY7Tn5Cm%2FmkzOTupqefDbp0UZYye0O6Lcgopu8dL6mhAzk8hQP3PEBQ4xt%2BQNehXPaVrmotNWiwpXSoweHtdd91Su4R9O4fj2mXDPs1tQNofEnla5cYvbW4oNWpKdw5qT73spoN6aDcaMWpFhZoYU%2Ffd')
    data = {}
    for name in league.player_map.values():
        if player := league.player_info(name=name):
            data[name] = []
            for i in range(league.current_week):
                if player.stats:
                    if player.stats.get(i):
                        if points := player.stats.get(i).get('points'):
                            data[name].append(points)
    print(data)