from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Match:
    match_id: int
    player1_id: int
    player2_id: int
    match_state: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    winner_id: Optional[int]
    accepted: Optional[bool]
