from __future__ import annotations

# import json

from src import chose_block, WOOLS
from src.main import GRASS, SAND, BRICK, STONE
from typing import TYPE_CHECKING

import requests

from lib_not_dr.loggers.config import get_logger

logger = get_logger(__name__)

if TYPE_CHECKING:
    from src.main import Model

URL = "127.0.0.1:1416"

PUB_KEY_MAP = []

def init_pub_key_map() -> None:
    global PUB_KEY_MAP
    response = requests.get(f"http://{URL}/pub_key")
    data: list[int] = response.json()
    str_pubkey = str(data)
    if str_pubkey not in PUB_KEY_MAP:
        PUB_KEY_MAP.append(str_pubkey)

def get_key_index(pub_key: str) -> int:
    """Get the index of the public key in the PUB_KEY_MAP."""
    if pub_key not in PUB_KEY_MAP:
        PUB_KEY_MAP.append(pub_key)
    return PUB_KEY_MAP.index(pub_key) % (len(WOOLS) - 1)

def init_world(world: Model) -> None:
    # 获取 know world
    response = requests.get(f"http://{URL}/known_world_state")
    data: list[dict[str, dict]] = response.json()
    # logger.info(f"Received known world state: {data}")
    for block in data:
        pub_key = block["pub_key"]
        index = get_key_index(str(pub_key))
        # if pub_key not in PUB_KEY_MAP:
        #     PUB_KEY_MAP.append(pub_key)
        block_pos = block["block"]["point"]
        block_type = block["block"]["block_info"]["type_id"]
        pos = (block_pos["x"], block_pos["y"], block_pos["z"])
        world.add_block(pos, chose_block(index), immediate=False)
    # logger.info(GRASS)


def get_update(world: Model) -> None:
    response = requests.get(f"http://{URL}/tick_update_vec")
    data = response.json()
    if len(data) == 0:
        return
    try:
        for block in data:
            pub_key = block["block"]["pub_key"]
            index = get_key_index(str(pub_key))
            block = block["block"]["block"]
            block_pos = block["point"]
            block_type = block["block_info"]["type_id"]
            pos = (block_pos["x"], block_pos["y"], block_pos["z"])
            world.add_block(pos, chose_block(index), immediate=True)
    except Exception as e:
        logger.error(f"Error processing tick update: {e}")
        logger.error(f"Data: {data}")
        raise e
