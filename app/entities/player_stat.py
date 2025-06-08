from dataclasses import dataclass
from typing import Optional

@dataclass
class PlayerStat:
    player_id: int
    total_matches: int
    wins: int
    accuracy: float