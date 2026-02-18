import dataclasses


@dataclasses.dataclass
class StatDTO:
    attempts: int = 0
    wins: int = 0

    @property
    def defeats(self) -> int:
        return self.attempts - self.wins

    @property
    def winrate(self) -> float:
        return round(self.wins / self.attempts, 4) * 100 if self.attempts else 0

    def as_dict(self) -> dict:
        data = dataclasses.asdict(self)
        data['winrate'] = self.winrate
        return data
