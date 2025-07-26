from __future__ import annotations


def tex_coord(x, y, n=8):
    """Return the bounding vertices of the texture square."""
    m = 1.0 / n
    dx = x * m
    dy = y * m
    return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
    """Return a list of the texture squares for the top, bottom and side."""
    top = tex_coord(*top)
    bottom = tex_coord(*bottom)
    side = tex_coord(*side)
    result = []
    result.extend(top)
    result.extend(bottom)
    result.extend(side * 4)
    return result


def same_tex_coords(x: int, y: int) -> list[float]:
    """Return the texture coordinates for a block with the same texture on all sides."""
    index = (x, y)
    return tex_coords(index, index, index)


GRASS = tex_coords((1, 0), (0, 1), (0, 0))
SAND = same_tex_coords(1, 1)
BRICK = same_tex_coords(2, 0)
STONE = same_tex_coords(2, 1)

WOOLS = {
    "RED": same_tex_coords(1, 2),
    "WHITE": same_tex_coords(2, 2),
    "PURPLE": same_tex_coords(0, 2),
    "YELLOW": same_tex_coords(3, 2),
    "PINK": same_tex_coords(3, 1),
    "ORANGE": same_tex_coords(3, 0),
    "BLUE": same_tex_coords(4, 1),
    "BROWN": same_tex_coords(4, 2),
    "CYAN": same_tex_coords(5, 0),
    "LIME": same_tex_coords(6, 0),
    "MAGENTA": same_tex_coords(7, 0),
    "GRAY": same_tex_coords(6, 1),
    "LIGHT_GRAY": same_tex_coords(6, 1),
    "LIGHT_BLUE": same_tex_coords(6, 0),
    "GREEN": same_tex_coords(5, 2),
    "BLACK": same_tex_coords(4, 0),
}
