from pydantic import BaseModel
from typing import List, Literal, Union, Dict, Optional
from enum import Enum


# Enums and Type Aliases
class GameState(str, Enum):
    WAITING = "WAITING"
    STARTING = "STARTING"
    STARTED = "STARTED"
    ENDING = "ENDING"
    ENDED = "ENDED"
    MATCH_COMPLETED = "MATCH_COMPLETED"


ALL_ENEMIES = Literal["wolf", "ghoul", "minotaur", "tiny"]
PlayerType = Literal["player"]
ItemType = Literal["big_potion", "ring", "speed_zapper", "chest", "coin", "power_up"]
PowerUpType = Literal["freeze", "bomb", "shockwave"]
HazardType = Literal["bomb", "icicle", "lightning_storm"]
Direction = Literal["right", "left"]
HazardStatus = Literal["idle", "active", "charging"]

GameObjectType = Union[PlayerType, ALL_ENEMIES, ItemType, HazardType]


class Position(BaseModel):
    x: float
    y: float


class GameObject(BaseModel):
    id: str
    position: Position
    type: GameObjectType


class Item(GameObject):
    value: Optional[float] = None  # Make value optional with a default value
    points: float
    power: Optional[PowerUpType] = None  # Make power optional with a default value
    health: Optional[float] = None


class Character(GameObject):
    attack_damage: float
    direction: Direction
    health: float
    max_health: float
    is_attacking: bool
    is_frozen: bool
    is_pushed: bool
    is_zapped: bool
    points: float


class Enemy(Character):
    pass


class Collision(BaseModel):
    type: str
    relative_position: Position


class Levelling(BaseModel):
    level: int
    available_skill_points: int = 0
    attack: int = 0
    speed: int = 0
    health: int = 0


class ItemInventory(BaseModel):
    big_potions: int
    speed_zappers: int
    rings: int


class Player(Character):
    display_name: str
    is_dashing: bool
    levelling: Levelling
    score: float
    shield_raised: bool
    special_equipped: str
    speech: str
    unleashing_shockwave: bool
    is_overclocking: bool
    has_health_regen: bool
    base_speed: float


class OwnPlayer(Player):
    collisions: List[Collision]
    items: ItemInventory
    is_cloaked: bool
    is_colliding: bool
    is_dash_ready: bool
    is_shield_ready: bool
    is_special_ready: bool
    is_zap_ready: bool
    overclock_duration: float


class Hazard(GameObject):
    status: HazardStatus
    attack_damage: float
    owner_id: str


class GameInfo(BaseModel):
    friendly_fire: bool
    game_type: str
    map: str
    match_id: str
    state: GameState
    time_remaining_s: float
    latency: float


class PlayerStat(BaseModel):
    id: str
    score: int
    kills: int
    deaths: int
    coins: int
    kd_ratio: float
    kill_streak: int
    overclocks: int
    xps: Optional[float] = 0.0  # Make xps optional with a default value
    wolf_kills: int
    ghoul_kills: int
    tiny_kills: int
    minotaur_kills: int
    player_kills: int
    self_destructs: int


class LevelData(BaseModel):
    game_info: GameInfo
    own_player: OwnPlayer
    items: List[Item]
    enemies: List[Enemy]
    players: List[Player]
    obstacles: List[Position]
    hazards: List[Hazard]
    stats: Optional[List[PlayerStat]] = []

    @classmethod
    def from_json(cls, json_str: str) -> "LevelData":
        return cls.model_validate_json(json_str)


class DebugInfo(BaseModel):
    target_id: str
    message: str


MoveType = Union[
    Literal["attack"],
    Literal["special"],
    Literal["dash"],
    Literal["shield"],
    Dict[Literal["move_to"], Position],
    Dict[Literal["speak"], str],
    Dict[Literal["use"], Literal["ring", "speed_zapper", "big_potion"]],
    Dict[Literal["redeem_skill_point"], Literal["attack", "health", "speed"]],
    Dict[Literal["debug_info"], DebugInfo],
]


class Move(BaseModel):
    move: MoveType
