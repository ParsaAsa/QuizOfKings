from dataclasses import dataclass
from typing import Optional

@dataclass
class Question:
    question_id: int
    question_text: str
    right_option: str  # 'A', 'B', 'C', or 'D'
    difficulty: str     # 'easy', 'medium', or 'hard'
    confirmed: Optional[bool]
    option_A: str
    option_B: str
    option_C: str
    option_D: str
    category_id: int
    author_id: int
