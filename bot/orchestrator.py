from models import LevelData, Move, Position, GameObject, Enemy
from typing import Dict, List, Optional, Sequence, Any


def play(level_data: LevelData) -> List[Move]:
    """
    Main decision function for the bot.
    1. Gather current game state
    2. Pass it to the state machine
    3. Submit the chosen action
    """

    # --- 1. Gather current game state ---
    moves = []
    own_player = level_data.own_player
    items = level_data.items

    moves.append({"speak": "Hello Botomy!"})

    moves.append(
        {
            "debug_info": {
                "message": "Hello from inside the debug info!",
            }
        }
    )

    return moves
