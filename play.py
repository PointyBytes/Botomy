# play.py

from models import LevelData, Move
from typing import Dict, List
from math import dist

ATTACK_RANGE = 50
LOW_HP_THRESHOLD = 0.30


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


def play(level_data: dict) -> list:
    player = level_data["own_player"]
    p_pos = player["position"]
    moves = []

    enemies = level_data.get("enemies", [])
    items = level_data.get("items", [])

    # ---------------------------------------------------------------------
    # PHASE 1 — Survival: heal first if needed
    # ---------------------------------------------------------------------
    if player["health"] <= player["max_health"] * LOW_HP_THRESHOLD:
        if drink_potion(player, moves):
            return moves  # healing is priority

    # ---------------------------------------------------------------------
    # PHASE 2 — Filter out dead or irrelevant targets
    # ---------------------------------------------------------------------
    living_enemies = [e for e in enemies if is_attackable(e)]
    valid_items = [i for i in items if i.get("type") != "dead"]

    # Split chests from other items
    chests = [i for i in valid_items if is_chest(i)]
    non_chest_items = [i for i in valid_items if not is_chest(i)]

    # ---------------------------------------------------------------------
    # PHASE 3 — Determine closest target per category
    # ---------------------------------------------------------------------
    def closest(entities):
        if not entities:
            return None, float("inf")
        annotated = [(e, distance(p_pos, e["position"])) for e in entities]
        return min(annotated, key=lambda t: t[1])

    closest_chest, dist_chest = closest(chests)
    closest_item, dist_item = closest(non_chest_items)
    closest_enemy, dist_enemy = closest(living_enemies)

    # ---------------------------------------------------------------------
    # PHASE 4 — Priority selection
    # ---------------------------------------------------------------------
    # Priority order:
    #   1. Chest (if any)
    #   2. Closest enemy vs closest item (whichever is nearer)
    if closest_chest:
        target = closest_chest
    else:
        # No chest → choose nearest of enemy or item
        if closest_item and closest_enemy:
            target = closest_item if dist_item < dist_enemy else closest_enemy
        else:
            target = closest_item or closest_enemy

    if not target:
        moves.append({"debug_info": {"message": "No targets available."}})
        return moves

    # ---------------------------------------------------------------------
    # PHASE 5 — Engage target
    # ---------------------------------------------------------------------
    return engage_target(player, target, moves)
