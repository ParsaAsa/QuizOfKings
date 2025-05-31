from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Match:
    match_id: int
    player1_username: str
    player2_username: str
    match_state: str  # "on_going" or "done"
    start_time: datetime
    end_time: Optional[datetime]
    winner: Optional[str]
