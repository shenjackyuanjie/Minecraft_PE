from __future__ import annotations

import random

def tex_coord(x, y, n=8):
    """返回纹理方块的边界顶点。"""
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """返回顶部、底部和侧面的纹理方块列表。"""
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


def same_tex_coords(x: int, y: int) -> list[float]:
    """返回所有面使用相同纹理的方块的纹理坐标。"""
    index = (x, y)
    return tex_coords(index, index, index)

# 基础方块纹理坐标定义
# 每个方块由顶部、底部和侧面的纹理坐标组成

# 草方块：顶部是草皮(1,0)，底部是泥土(0,1)，侧面是草皮侧面(0,0)
GRASS = tex_coords((1, 0), (0, 1), (0, 0))
# 沙子：所有面都使用相同的沙子纹理(1,1)
SAND = same_tex_coords(1, 1)
# 砖块：所有面都使用相同的红砖纹理(2,0)
BRICK = same_tex_coords(2, 0)
# 石头：所有面都使用相同的石头纹理(2,1)
STONE = same_tex_coords(2, 1)
# TNT：顶部是TNT顶面(7,1)，底部是TNT底面(7,3)，侧面是TNT侧面(7,2)
TNT = tex_coords((7, 1), (7, 3), (7, 2))

# 羊毛方块颜色映射
# 每种颜色对应纹理图集中的不同位置
WOOLS = {
    "RED": same_tex_coords(1, 2),        # 红色羊毛
    "WHITE": same_tex_coords(2, 2),      # 白色羊毛
    "PURPLE": same_tex_coords(0, 2),     # 紫色羊毛
    "YELLOW": same_tex_coords(3, 2),     # 黄色羊毛
    "PINK": same_tex_coords(3, 1),       # 粉色羊毛
    "ORANGE": same_tex_coords(3, 0),     # 橙色羊毛
    "BLUE": same_tex_coords(4, 1),       # 蓝色羊毛
    "BROWN": same_tex_coords(4, 2),      # 棕色羊毛
    "CYAN": same_tex_coords(5, 0),       # 青色羊毛
    "LIME": same_tex_coords(6, 0),       # 黄绿色羊毛
    "MAGENTA": same_tex_coords(7, 0),    # 品红色羊毛
    "GRAY": same_tex_coords(6, 1),       # 灰色羊毛
    "LIGHT_GRAY": same_tex_coords(6, 1), # 浅灰色羊毛
    "LIGHT_BLUE": same_tex_coords(6, 0), # 浅蓝色羊毛
    "GREEN": same_tex_coords(5, 2),      # 绿色羊毛
    "BLACK": same_tex_coords(4, 0),      # 黑色羊毛
}

def chose_block(index: int | None = None) -> list[float]:
    """返回随机方块的纹理坐标。"""
    if index is None:
        index = random.randint(0, len(WOOLS) - 1)
    return list(WOOLS.values())[index % len(WOOLS)]


def select_block(name: str) -> list[float]:
    """根据名称返回方块的纹理坐标。

    如果名称匹配羊毛颜色，返回该羊毛的纹理。
    否则，返回沙子纹理。
    """
    upper_name = name.upper()
    if upper_name in WOOLS:
        return WOOLS[upper_name]
    return SAND
