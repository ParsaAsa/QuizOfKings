from dataclasses import dataclass
from typing import Optional

@dataclass
class PlayerAnswer:
    match_id: int
    round_number: int
    question_id: int
    question_number: int
    player_id: int
    player_answer: Optional[str] = None