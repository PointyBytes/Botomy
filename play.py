from models import LevelData, Move
from typing import List


# Python (External Server)
# example modifying play.py
def play(level_data: dict) -> list:
    moves = []

    # Find the enemies
    enemies = level_data["enemies"]
    if enemies:
        enemy = enemies[0]
        # Move to the enemy's position
        moves.append({"move_to": enemy["position"]})

        # Attack
        moves.append("attack")

    # Find the coins
    coins = [item for item in level_data["items"] if item["type"] == "coin"]
    if coins:
        coin = coins[0]
        # Move to the coin's position
        moves.append(
            {"move_to": {"x": coin["position"]["x"], "y": coin["position"]["y"]}}
        )

    # Default move
    moves.append(
        {
            "debug_info": {
                "message": "Congratulations! You have reached the play function. Modify this file (play.py) to implement your bot's logic.",
            }
        }
    )
    return moves
