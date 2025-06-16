from dataclasses import dataclass

@dataclass
class Team:
    ID: int
    year: int
    teamCode: str
    divID: str
    div_ID: int
    teamRank: int
    games: int
    gamesHome: int
    wins: int
    losses: int
    divisionWinnner: bool
    leagueWinner: bool
    worldSeriesWinnner: bool
    runs: int
    hits: int
    homeruns: int
    stolenBases: int
    hitsAllowed: int
    homerunsAllowed: int
    name: str
    park: str

    def __hash__(self):
        return hash((self.ID, self.year))

    def __str__(self):
        return (f"{self.name} ({self.year}) – {self.teamCode} | "
                f"Wins: {self.wins}, Losses: {self.losses}, HR: {self.homeruns}, SB: {self.stolenBases}")
