from models import LevelData, Move, Position, GameObject, Enemy
from typing import Dict, List, Optional, TypedDict, Any, Sequence
import math
import random

# Constants
ATTACK_RANGE = 125
LOW_HEALTH_THRESHOLD = 0.51
INVENTORY_MAX = {"big_potion": 6, "speed_zapper": 5, "ring": 5}
# Weights for skills can not be zero or negative
LEVEL_UP_SKILL_WEIGHTS = {"attack": 5, "health": 3, "speed": 2}

ITEM_TO_ATTRIBUTE = {
    "big_potion": "big_potions",
    "speed_zapper": "speed_zappers",
    "ring": "rings",
}

# Work in progress:
# TODO: Implement combat logic &, item usage
# TODO: Implement special attack logic
# TODO: Implement sofisticated item pickup strategy


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


def select_level_up_skill() -> str:
    """Randomly select a skill to level up based on predefined weights."""
    # TODO: Add error handling for empty or negative weights
    # TODO: Test for a potential edge case where hp is low and if leveling health gives full hp
    skill_list = list(LEVEL_UP_SKILL_WEIGHTS.keys())
    weights = list(LEVEL_UP_SKILL_WEIGHTS.values())

    return random.choices(
        population=skill_list,
        weights=weights,
    )[0]


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
    players = level_data.players  # Unused for now but may be useful later
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

    if own_player.levelling.available_skill_points > 0:
        # skill points available - level up
        moves.append({"redeem_skill_point": select_level_up_skill()})

    moves.append(
        {
            "debug_info": {
                "target_id": target.id if target else None,
                "message": "oh hai",
            }
        }
    )
    return moves
