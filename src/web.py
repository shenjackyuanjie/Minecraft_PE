from __future__ import annotations

# import json

from src.main import GRASS, SAND, BRICK, STONE
from typing import TYPE_CHECKING

import requests

from lib_not_dr.loggers.config import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.main import Model

URL = "127.0.0.1:1416"

def init_world(world: Model) -> None:
    # 获取 know world
    response = requests.get(f"http://{URL}/known_world_state")
    data: list[dict[str, dict]] = response.json()
    # logger.info(f"Received known world state: {data}")
    for block in data:
        block_pos = block["block"]["point"]
        pos = (block_pos["x"], block_pos["y"], block_pos["z"])
        world.add_block(pos, GRASS, immediate=False)
    # logger.info(GRASS)
