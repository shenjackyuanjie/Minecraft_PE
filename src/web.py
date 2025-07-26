from __future__ import annotations

import threading

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
    response = requests.get(f"http://{URL}/pubkey")
    data: list[int] = response.json()
    str_pubkey = str(data)
    if str_pubkey not in PUB_KEY_MAP:
        PUB_KEY_MAP.append(str_pubkey)

init_pub_key_map()

def get_my_block() -> list[float]:
    """Get the texture coordinates for the player's block."""
    init_pub_key_map()
    if len(PUB_KEY_MAP) == 0:
        return GRASS
    index = get_key_index(PUB_KEY_MAP[0])
    return chose_block(index)

def get_key_index(pub_key: str) -> int:
    """Get the index of the public key in the PUB_KEY_MAP."""
    if pub_key not in PUB_KEY_MAP:
        PUB_KEY_MAP.append(pub_key)
    return PUB_KEY_MAP.index(pub_key) % (len(WOOLS) - 1)

def check_block_type(block_type: str) -> bool:
    """检查该方块是否需要渲染"""
    if block_type in ["air", "unknown", "water", "lava"]:
        return False
    return True

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
        if not check_block_type(block_type):
            continue
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
            pos = (block_pos["x"], block_pos["y"], block_pos["z"])
            block_type = block["block_info"]["type_id"]
            if not check_block_type(block_type):
                if pos in world.world:
                    world.remove_block(pos)
                continue
            world.add_block(pos, chose_block(index), immediate=True)
    except Exception as e:
        logger.error(f"Error processing tick update: {e}")
        logger.error(f"Data: {data}")
        raise e


def send_block(pos: tuple[int, int, int], block_type: str, once: bool = True) -> None:
    thread = threading.Thread(target=send_block_inner, args=(pos, block_type, once))
    thread.start()

def send_block_inner(pos: tuple[int, int, int], block_type: str, once: bool = True) -> None:
    """Send a block to the server."""
    data = {
        "duration": 100,
        "x": pos[0],
        "y": pos[1],
        "z": pos[2],
        "info": {
            "type_id": block_type,
        }
    }
    target = "set_block_once" if once else "set_block"
    response = requests.post(f"http://{URL}/{target}", json=data)
    if response.status_code != 200:
        logger.error(f"Failed to send block: {response.text}")
