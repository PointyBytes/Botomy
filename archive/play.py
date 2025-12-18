from bot.data.flavor import FLAVOR_PHRASES
from models import LevelData, Move, Position, GameObject, Enemy
from typing import Dict, List, Optional, Sequence, Any
import math
import random

# --- Combat and environment constants ---
ATTACK_RANGE: int = 125

# --- AI tuning constants ---
LOW_HEALTH_THRESHOLD: float = 0.51
# Weights for skills can not be zero or negative
LEVEL_UP_SKILL_WEIGHTS: Dict[str, int | float] = {"attack": 5, "health": 3, "speed": 2}

# --- Inventory rules ---
INVENTORY_MAX: Dict[str, int] = {"big_potion": 6, "speed_zapper": 5, "ring": 5}
ITEM_TO_ATTRIBUTE: Dict[str, str] = {
    "big_potion": "big_potions",
    "speed_zapper": "speed_zappers",
    "ring": "rings",
}

# Other constants and configurations
ADD_FLAVOR: bool = False  # Toggle for adding flavor messages

# Work in progress:
# TODO: Implement combat logic &, item usage
# TODO: Implement special attack logic
# TODO: Implement sofisticated item pickup prioritization
# TODO: Implement escape & evasion logic
# TODO: Implement different strategies based on game_info.game_type

# Flavor and fun:
# TODO: Implement heroic battle cries and taunts


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


def filter_alive_enemies(enemy: Enemy) -> bool:
    """Check if an enemy is alive based on its health attribute."""
    enemy_health = getattr(enemy, "health", None)
    return isinstance(enemy_health, (int, float)) and float(enemy_health) > 0.0


def build_flavor_message(action: str) -> Dict[str, str]:
    """
    Create a flavor message dictionary based on the action.
    Args:
        action (str): The action type (e.g., "attack", "pickup").
    Returns:
        Dict[str, str]: A dictionary containing the flavor message.
    """
    # TODO: Fix message changing every loop
    phrases = FLAVOR_PHRASES.get(action)
    message = random.choice(phrases) if phrases else "404 Action Cry Not Found!"
    return {"speak": message}


def build_debug_message(message: str, **kwargs: Any) -> Dict[str, Any]:
    """
    Create a debug message dictionary.
    Args:
        message (str): The main debug message.
        **kwargs: Additional key-value pairs to include in the debug info.
    Returns:
        Dict[str, Any]: A dictionary containing the debug information.
    """
    return {"debug_info": {"message": message, **kwargs}}


def play(level_data: LevelData) -> List[Move]:
    """
    Main decision function for the bot.

    Steps:
    1. Gather current game state
    2. Handle progression (level-up)
    3. Apply survival logic (healing, escape)
    4. Determine valid targets
    5. Select primary target
    6. Execute movement and combat
    """
    # TODO: Attach debug information at each step for better traceability
    # TODO: Refactor steps to match the listed order above

    # --- 1. Gather current game state ---
    moves = []
    own_player = level_data.own_player
    players = level_data.players  # Unused for now but may be useful later
    items = level_data.items

    # --- 2. Handle progression (level-up) ---
    if own_player.levelling.available_skill_points > 0:
        moves.append({"redeem_skill_point": select_level_up_skill()})

    # --- 3. Apply survival logic (healing, escape) ---
    if own_player.health / own_player.max_health < LOW_HEALTH_THRESHOLD:
        moves.append({"use": "big_potion"})
        if ADD_FLAVOR:
            moves.append(build_flavor_message("heal"))

    # --- 4. Determine valid targets ---
    # Only include enemies that have a numeric health value > 0
    alive_enemies = [
        enemy for enemy in level_data.enemies if filter_alive_enemies(enemy)
    ]
    potential_targets = filter_pickable_items(items, own_player) + alive_enemies

    # --- 5. Select primary target ---
    target = get_closest_item(own_player.position, potential_targets)
    moves.append(
        {
            "debug_info": build_debug_message(
                "Current Target",
                target_type=target.type if target else "None",
            )
        }
    )

    # --- 6. Execute movement and combat ---
    # TODO: Check if target HP > 0 before attacking
    if target:
        target_health = getattr(target, "health", None)
        has_health = isinstance(target_health, (int, float))
        if (
            target.type in ["wolf", "ghoul", "minotaur", "tiny", "chest"]
            and has_health
            and float(target_health) > 0.0
        ):
            if dist_to(own_player.position, target.position) < ATTACK_RANGE:
                moves.append("attack")
                moves.append("shield")
                if ADD_FLAVOR:
                    moves.append(build_flavor_message("attack"))
        moves.append({"move_to": target.position})
    else:
        print("no target found")

    # --- 7. Attach debug information ---
    moves.append(
        {
            "debug_info": build_debug_message(
                "Current Target",
                target_type=target.type if target else "None",
                target_position=target.position if target else "N/A",
            )
        }
    )

    return moves
