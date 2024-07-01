from dataclasses import dataclass

@dataclass
class Match:
    MatchID: int
    TeamHomeID : int
    TeamAwayID: int
    nomeHome: str
    nomeAway: str

    def __hash__(self):
        return hash(self.MatchID)

    def __str__(self):
        return f"{self.MatchID}: {self.nomeHome} ({self.TeamHomeID}) vs. {self.nomeAway} {self.TeamAwayID}"