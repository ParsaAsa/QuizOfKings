from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Match:
    match_id: int
    player1_username: str
    player2_username: str
    match_state: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    winner_username: Optional[str]
    accepted: Optional[bool]
