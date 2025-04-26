import dataclasses

@dataclasses.dataclass
class Team:
    id: int
    name: str
    copetition_id: int
    rank: int
    total_players: int
