from models import LevelData, Move, Position, GameObject, Enemy
from typing import Dict, List, Optional, Sequence, Any


def play(level_data: LevelData) -> List[Move]:
    """
    Main decision function for the bot.
    """
    moves: List[Move] = []

    moves.append({"speak": "Hello Botomy!"})

    moves.append(
        {
            "debug_info": {
                "target_id": target.id if target else None,
                "message": "oh hai",
            }
        }
    )

    return moves
