from queue import SimpleQueue
from typing import List

from blitz2020.game.direction import directions
from blitz2020.game.position import Position


def flood(flood: List[List[int]], target: int, replacement: int) -> None:
    x_size = len(flood[0])
    y_size = len(flood)

    queue: SimpleQueue = SimpleQueue()
    queue.put(Position(0, 0))
    while not queue.empty():
        cur = queue.get()
        for _, delta in directions:
            sibblingX = cur.x + delta[0]
            sibblingY = cur.y + delta[1]
            if sibblingX >= 0 and sibblingX < x_size and sibblingY >= 0 and sibblingY < y_size:
                if flood[sibblingY][sibblingX] == target:
                    flood[sibblingY][sibblingX] = replacement
                    queue.put(Position(sibblingX, sibblingY))
