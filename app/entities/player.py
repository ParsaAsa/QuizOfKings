from dataclasses import dataclass
from datetime import datetime

@dataclass
class Player:
    player_id: int
    username: str
    email: str
    player_password: str
    signup_date: datetime
    player_role: str  # "normal", "admin", or "manager"
