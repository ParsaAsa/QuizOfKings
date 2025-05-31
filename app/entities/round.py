from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Round:
    round_id: int
    match_id: int
    round_number: int
    round_state: str
    turn_started_at: Optional[datetime]
