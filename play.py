# play.py

from math import dist
from models import LevelData
from typing import Dict, List


# Constants
ATTACK_RANGE = 50  # Example attack range
LOW_HP_THRESHOLD = 0.40  # 40% health threshold


def distance(a, b):
    return dist((a["x"], a["y"]), (b["x"], b["y"]))


def is_attackable(entity: dict) -> bool:
    return "health" in entity and entity["health"] is not None and entity["health"] > 0


def is_chest(entity: dict) -> bool:
    return entity.get("type") == "chest"


def drink_potion(player, moves):
    items = player["items"]

    # Prefer big potions
    if items.get("big_potions", 0) > 0:
        moves.append({"use": "big_potion"})
        return True

    # Fall back to normal potions
    if items.get("potions", 0) > 0:
        moves.append({"use": "potion"})
        return True

    return False


def engage_target(player, target, moves):
    p_pos = player["position"]
    t_pos = target["position"]
    d = distance(p_pos, t_pos)

    if is_attackable(target):
        if d <= ATTACK_RANGE:
            moves.append("attack")
        else:
            moves.append({"move_to": t_pos})
    else:
        # Non-attackable item (coins etc.)
        moves.append({"move_to": t_pos})

    return moves


def play(level_data: dict) -> List[dict]:
    """
    Entry point called by the game server. Convert the raw dict to LevelData
    for type safety and convenience methods, then run the AI logic.
    """
    # Convert dict -> LevelData model (Pydantic v2 style)
    data = LevelData.model_validate(level_data)

    me = data.own_player
    moves = []

    # Survival check using model fields
    if me.health <= me.max_health * LOW_HP_THRESHOLD:
        # example: prefer big_potion
        if me.items.big_potions > 0:
            moves.append({"use": "big_potion"})
            return moves
        # if you had a normal potion field, you'd check that here

    # Build lists of living enemies and items
    living_enemies = [e for e in data.enemies if e.is_alive()]
    items = data.items  # these are Item models

    # Find closest chest first (using Position.distance())
    chests = [
        i for i in items if i.type == "chest" and (i.health is None or i.health > 0)
    ]
    closest_chest = None
    if chests:
        closest_chest = min(chests, key=lambda c: me.position.distance(c.position))

    # If chest exists, go for it
    if closest_chest:
        d = me.position.distance(closest_chest.position)
        if (closest_chest.health or 0) > 0:
            # attackable chest
            if d <= ATTACK_RANGE:
                moves.append("attack")
            else:
                moves.append({"move_to": closest_chest.position.dict()})
        else:
            moves.append({"move_to": closest_chest.position.dict()})
        return moves

    # Otherwise decide between nearest item and nearest enemy (simple heuristic)
    # ... you can reuse earlier logic but call position.distance(...) and enemy.is_alive() etc.

    # fallback
    moves.append({"debug_info": {"message": "Nothing to do right now."}})
    return moves
