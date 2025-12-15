from models import LevelData, Move, Position, GameObject, Enemy
from typing import Dict, List, Optional, TypedDict, Any, Sequence
import math
import random

# Constants
ATTACK_RANGE = 125
LOW_HEALTH_THRESHOLD = 0.51
INVENTORY_MAX = {"big_potion": 6, "speed_zapper": 5, "ring": 5}
ITEM_TO_ATTRIBUTE = {
    "big_potion": "big_potions",
    "speed_zapper": "speed_zappers",
    "ring": "rings",
}


def dist_to(a: Position, b: Position) -> float:
    # Use dot notation to access attributes of Position
    return math.sqrt(pow(a.x - b.x, 2) + pow(a.y - b.y, 2))


def get_closest_item(
    position: Position, items: Sequence[GameObject]
) -> Optional[GameObject]:
    min_dist = float("inf")
    target = None

    for item in items:
        dist = dist_to(position, item.position)
        if dist < min_dist:
            min_dist = dist
            target = item

    return target


def filter_pickable_items(items, own_player) -> List[GameObject]:
    """Return all world items the player is allowed to pick up, given current inventory limits."""

    # TODO: Filtering logic
    # 1. Iterate over world items
    # 2. For each item:
    #     2.1. Decide whether it is limited
    #     2.2. If limited, compare player_inv vs max
    #     2.3. If allowed, append to filtered_list
    # 3. Return filtered_list

    filtered_items = []
    inventory = own_player.items
    for item in items:
        if item.type in INVENTORY_MAX:
            attribute_name = ITEM_TO_ATTRIBUTE[item.type]
            current_count = getattr(inventory, attribute_name)
            if current_count < INVENTORY_MAX[item.type]:
                filtered_items.append(item)
        else:
            filtered_items.append(item)
    return filtered_items


def play(level_data: LevelData) -> List[Move]:
    """
    Main decision function for the bot.

    Steps:
    1. Filter world items based on inventory limits.
    2. Identify closest target (item or enemy).
    3. Decide combat actions (attack/shield).
    4. Use items if necessary (healing potions, power-ups).
    5. Redeem available skill points.
    6. Return list of moves for this turn.
    """
    moves = []
    own_player = level_data.own_player
    players = level_data.players
    items = level_data.items

    # Build a list of potential targets (items, enemies, etc.)
    potential_targets = filter_pickable_items(items, own_player) + level_data.enemies

    # Get the closest item to your own player's position
    target = get_closest_item(own_player.position, potential_targets)

    if target:
        if target.type in ["wolf", "ghoul", "minotaur", "tiny"]:
            if dist_to(own_player.position, target.position) < ATTACK_RANGE:
                moves.append("attack")
                moves.append("shield")
        moves.append({"move_to": target.position})
    else:
        print("no target found")

    if own_player.health / own_player.max_health < LOW_HEALTH_THRESHOLD:
        # health is less than 50% so use the potion to heal
        moves.append({"use": "big_potion"})

    # TODO: Add logic for leveling up skills acording to my strategy
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
