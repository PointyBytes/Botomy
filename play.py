from models import LevelData, Move, Position, GameObject, Enemy
from typing import Dict, List, Optional, TypedDict, Any
import math
import random


def dist_to(a: Position, b: Position) -> float:
    # Use dot notation to access attributes of Position
    return math.sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))


def get_closest_item(
    position: Position, items: List[GameObject]
) -> Optional[GameObject]:
    min_dist = float("inf")
    target = None

    for item in items:
        dist = dist_to(position, item.position)
        if dist < min_dist:
            min_dist = dist
            target = item

    return target


def play(level_data: LevelData) -> List[Move]:
    moves = []
    own_player = level_data.own_player
    players = level_data.players
    items = level_data.items

    # Build a list of potential targets (items, enemies, etc.)
    potential_targets = items + level_data.enemies

    # Get the closest item to your own player's position
    target = get_closest_item(own_player.position, potential_targets)

    if target:
        if target.type in ["wolf", "ghoul", "minotaur", "tiny"]:
            if dist_to(own_player.position, target.position) < 125:
                moves.append("attack")
                moves.append("shield")
        moves.append({"move_to": target.position})
    else:
        print("no target found")

    if own_player.health / own_player.max_health < 0.51:
        # health is less than 50% so use the potion to heal
        moves.append({"use": "big_potion"})

    if own_player.levelling.available_skill_points > 0:
        # skill points available - level up
        skill = random.choice(["attack", "health", "speed"])
        moves.append({"redeem_skill_point": skill})

    moves.append(
        {
            "debug_info": {
                "target_id": target.id if target else None,
                "message": "oh hai",
            }
        }
    )
    return moves
