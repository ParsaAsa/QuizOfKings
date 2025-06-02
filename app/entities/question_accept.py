from dataclasses import dataclass

@dataclass
class QuestionAccept:
    question_id: int
    player_id: int
    confirmed: bool
