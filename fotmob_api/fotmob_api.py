import json
from typing import Any, Dict, List

import ratelimiter
import requests
from requests import Response


class FotmobAPI:
    def __init__(
        self,
        requests_per_sec: int = 6,
    ):

        self.base = "www.fotmob.com"
        self.base_api = "/api/"
        self.rate_limiter = ratelimiter.RateLimiter(
            max_calls=requests_per_sec, period=1
        )

    # Loaders
    def _url(self, *route):
        return "https://{base}/{route}/".format(
            base=self.base + self.base_api, route="/".join(str(r) for r in route)
        )

    def _parse_response(self, response: Response):
        return response.json()

    def _get(self, *route, **params):

        for param, val in params.items():
            if isinstance(param, bool):
                params[param] = json.dumps(val)  # So that True -> 'true'

        with self.rate_limiter:
            r = requests.get(self._url(*route), params=params)

        return self._parse_response(r)

    # Location

    def get_my_location(self) -> Dict[str, Any]:
        """Get information about your current location

        Returns:
            Dict[str, Any]: Location information
        """
        return self._get("myLocation")

    # League

    def get_league_all(self) -> Dict[str, Any]:
        """Get all leagues from FotMob

        Returns:
            _type_: Basic description of all leagues in FotMob
        """
        return self._get("allLeagues")

    def get_league_of_the_week(self, ccode: str = "ENG"):
        """League of the week is a weekly league that is highlighted on the FotMob front page

        Args:
            ccode (str, optional): Code for the country to get league of the week. Defaults to "ENG".

        Returns:
            _type_: ID for the league of the week
        """
        return self._get("leagueOfTheWeek", ccode3=ccode)

    def get_league_overview(self, id: int):
        """Get basic information about the specified league

        Args:
            id (int): ID identifier for the league

        Returns:
            json: Basic information about a specified league
        """
        return self._get("leagues", id, "overview")

    def get_league_table(
        self, league_id: int, teams: int | List[int] = None
    ) -> Dict[str, Any]:
        """Get league table of specific league. Including teams yields advanced stats for the specified teams

        Args:
            league_id (int): ID identifier for the league
            teams (int | List[int], optional): ID identifier of one or multiple teams. Defaults to None.

        Returns:
            Dict[str, Any]: League table with position and statististics for each team.
        """
        return self._get("tltable", leagueId=league_id, teams=teams)

    # Fixtures

    def get_fixtures(self, id: int, season: str) -> List[Dict[str, Any]]:
        """Get fixtures for a specific league and season

        Args:
            id (int): ID identifier for the league
            season (str): Season name in the format "YYYY/YYYY" or "YYYY", e.g. "2022/2023" or "2022"

        Returns:
            List[Dict[str, Any]]: All fixtures with basic information
        """
        return self._get("fixtures", id=id, season=season)

    # Team of the week

    def get_team_of_the_week_rounds(
        self, league_id: int, season: str
    ) -> Dict[str, Any]:
        """Get all rounds from which team of the week have been awarded

        Args:
            league_id (int): ID identifier for the league
            season (str): Season name in the format "YYYY/YYYY" or "YYYY", e.g. "2022/2023" or "2022"

        Returns:
            Dict[str, Any]: Basic information about each round from which team of the week have been awarded
        """
        return self._get(
            "team-of-the-week",
            "rounds",
            leagueId=league_id,
            season=season,
        )

    def get_team_of_the_week(
        self, league_id: int, round_id: int, season: str
    ) -> List[Dict[str, Any]]:
        """Get the highest performing players for round in a season for league, i.e. team of the week

        Args:
            league_id (int): ID identifier for the league
            round_id (int): ID identifier for the round, e.g. 23 (for round 23)
            season (str): Season name in the format "YYYY/YYYY" or "YYYY", e.g. "2022/2023" or "2022"

        Returns:
            List[Dict[str, Any]]: _description_
        """
        return self._get(
            "team-of-the-week",
            "team",
            leagueId=league_id,
            roundId=round_id,
            season=season,
        )

    # Matches

    def get_matches(
        self, date: str = None, timezone: str = None, ccode: str = "ENG"
    ) -> Dict[str, Any]:
        """Get basic information about matches for a specific date

        Args:
            date (str, optional): The date to get matches for, should be in the format "YYYYMMDD".
                                  If None, matches from the current date is extracted. Defaults to None.
            timezone (str, optional): Timezone from which you want information from such as kickoff times. Defaults to None.
            ccode (str, optional): Code for the country to get league of the week. Defaults to "ENG".

        Returns:
            Dict[str, Any]: Basic information about matches for a specific date
        """
        return self._get("matches", date=date, timezone=timezone, ccode3=ccode)

    def get_match(self, match_id: int) -> Dict[str, Any]:
        """Get information about a specific match.

        Args:
            match_id (int): ID identifier for the match.

        Returns:
            Dict[str, Any]: Information about the specified match.
        """
        return self._get("match", id=match_id)

    def get_match_details(self, match_id: int) -> Dict[str, Any]:
        """Get detailed information about a specific match.

        Args:
            match_id (int): ID identifier for the match.

        Returns:
            Dict[str, Any]: Detailed information about the specified match.
        """
        return self._get("matchDetails", matchId=match_id)

    def get_match_media(self, match_id: int, ccode: str = "ENG") -> Dict[str, Any]:
        """Get media-related information for a specific match.

        Args:
            match_id (int): ID identifier for the match.
            ccode (str, optional): Code for the country. Defaults to "ENG".

        Returns:
            Dict[str, Any]: Media-related information for the specified match.
        """
        return self._get("matchMedia", matchId=match_id, ccode3=ccode)

    # Match odds

    def get_match_odds(
        self, match_id: int, ccode: str = "ENG", betting_provider: str = None
    ) -> Dict[str, Any]:
        """Get odds-related information for a specific match.

        Args:
            match_id (int): ID identifier for the match.
            ccode (str, optional): Code for the country. Defaults to "ENG".
            betting_provider (str, optional): Betting provider code. Defaults to None.

        Returns:
            Dict[str, Any]: Odds-related information for the specified match.
        """
        return self._get(
            matchId=match_id, ccode3=ccode, bettingProvider=betting_provider
        )

    # Team

    def get_team(self, team_id: int, ccode: str = "ENG") -> Dict[str, Any]:
        """Get information about a specific team.

        Args:
            team_id (int): ID identifier for the team.
            ccode (str, optional): Code for the country. Defaults to "ENG".

        Returns:
            Dict[str, Any]: Information about the specified team.
        """
        return self._get("teams", id=team_id, ccode3=ccode)

    def get_team_season_stats(self, team_id: int, tournament_id: int) -> Dict[str, Any]:
        """Get season statistics for a specific team in a given tournament.

        Args:
            team_id (int): ID identifier for the team.
            tournament_id (int): ID identifier for the tournament.

        Returns:
            Dict[str, Any]: Season statistics for the specified team in the given tournament.
        """
        return self._get(teamId=team_id, tournamentId=tournament_id)

    def get_team_historical_table(self, team_id: int) -> Dict[str, Any]:
        """Get historical table information for a specific team.

        Args:
            team_id (int): ID identifier for the team.

        Returns:
            Dict[str, Any]: Historical table information for the specified team.
        """
        return self._get("historicaltable", teamId=team_id)

    # Player

    def get_player_data_simple(self, player_id: int) -> Dict[str, Any]:
        """Get simple data about a specific player.

        Args:
            player_id (int): ID identifier for the player.

        Returns:
            Dict[str, Any]: Simple data about the specified player.
        """
        return self._get("simplePlayerData", id=player_id)

    def get_player_data(self, player_id: int) -> Dict[str, Any]:
        """Get detailed data about a specific player.

        Args:
            player_id (int): ID identifier for the player.

        Returns:
            Dict[str, Any]: Detailed data about the specified player.
        """
        return self._get("playerData", id=player_id)

    def get_player_stats(
        self, player_id: int, league_id: int, season: str
    ) -> Dict[str, Any]:
        """Get statistical information about a specific player in a given league and season.

        Args:
            player_id (int): ID identifier for the player.
            league_id (int): ID identifier for the league.
            season (str): Season name in the format "YYYY/YYYY".

        Returns:
            Dict[str, Any]: Statistical information about the specified player in the given league and season.
        """
        return self._get(
            "playerStats", playerId=player_id, seasonId=f"{season}-{league_id}"
        )

    def get_player_news(
        self, player_id: int, language: str = "en-GB"
    ) -> List[Dict[str, Any]]:
        """Get news about a specific player.

        Args:
            player_id (int): ID identifier for the player.
            language (str, optional): Language code for the news. Defaults to "en-GB".

        Returns:
            List[Dict[str, Any]]: News about the specified player.
        """
        return self._get("playerNews", id=player_id, lang=language)

    # Transfers

    def get_transfers(self, showTop: bool = True, page: int = 1) -> Dict[str, Any]:
        """Get basic information about transfers

        Args:
            showTop (bool, optional): _description_. Defaults to True.
            page (int, optional): Page to load. Defaults to 1.

        Returns:
            Dict[str, Any]: Basic information about transfers
        """
        return self._get("transfers", showTop=showTop, page=page)
