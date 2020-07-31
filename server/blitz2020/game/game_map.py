import random
from typing import Optional, Tuple, List, Any, Dict

from blitz2020.game.position import Position


class OutOfBoundExeption(Exception):
    """
    A class used to represent an OutOfBoundExeption

    Attributes
    ----------
    position : Position
        the out of bound position
    bound : int
        the bound size
    """

    def __init__(self, position: Position, bound: int):
        self.position = position
        self.bound = bound


class InvalidStateException(Exception):
    pass


class GameMap:
    """
    A class used to represent a Map

    Attributes
    ----------
    tiles :
        an array of arrays of tuples[state, owner] representing the current map
    size : int
        the map size
    empty_tiles : int
        number of free tiles in the map
    """

    EMPTY = " "
    ASTEROIDS = "W"
    PLANET = "%"
    BLITZIUM = "$"
    BLACK_HOLE = "!"
    DIRECTION = "D"

    valid_tiles = {EMPTY, ASTEROIDS, PLANET, BLITZIUM, BLACK_HOLE}

    empty_tile = (EMPTY, None)

    def __init__(self, size: int = 0):
        self.size = size
        self.tiles: Optional[List[List[Tuple[str, Optional[int]]]]] = None
        self.empty_tiles = 0
        if size > 0:
            self.tiles = [[GameMap.empty_tile] * size for _ in range(size)]
            self.empty_tiles = (size - 2) ** 2

            w = (self.ASTEROIDS, None)
            for y in range(size):
                for x in range(size):
                    if x == 0 or x == size - 1 or y == 0 or y == size - 1:
                        self.tiles[y][x] = w

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, GameMap):
            return NotImplemented
        return self.size == other.size and self.tiles == other.tiles and self.empty_tiles == other.empty_tiles

    def __deepcopy__(self, _: Optional[Dict[str, Any]] = None) -> 'GameMap':
        obj = type(self)()
        obj.size = self.size
        obj.tiles = [row.copy() for row in self.tiles]
        obj.empty_tiles = self.empty_tiles
        return obj

    def __str__(self) -> str:
        return "\n".join(
            [
                "".join([(str(x[1]) if x[0] != GameMap.PLANET and x[1] is not None else x[0]) for x in y])
                for y in self.tiles
            ]
        )

    def is_out_of_bound(self, position: Position) -> bool:
        """
        Checks if position is out of bound for the current map

        Parameters
        ----------
        position : Position
            The position
        """
        x = position.x
        y = position.y
        return x < 0 or y < 0 or x >= self.size or y >= self.size

    def check_position(self, position: Position) -> None:
        """
        Checks if position is out of bound for the current map

        Parameters
        ----------
        position : Position
            The position

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        if self.is_out_of_bound(position):
            raise OutOfBoundExeption(position, self.size)

    def get_tile(self, position: Position) -> Tuple[str, Optional[int]]:
        """
        Returns the tile at the desired position

        Parameters
        ----------
        position : Position
            The position of the tile

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        self.check_position(position)

        return self.tiles[position.y][position.x]

    def set_tile(self, position: Position, state: str, player_id: Optional[int] = None) -> None:
        """
        Set the tile at the desired position

        Parameters
        ----------
        position : Position
            The position of the tile

        state : str
            The tile type

        player_id : int
            The tile owner

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        self.check_position(position)

        if state not in GameMap.valid_tiles:
            raise InvalidStateException(f"Invalid map tile state {state}")

        if (
            state == GameMap.ASTEROIDS or state == GameMap.BLITZIUM or state == GameMap.BLACK_HOLE
        ) and player_id is not None:
            raise InvalidStateException(f"Cannot have a player_id")

        if state != GameMap.ASTEROIDS and self.get_tile(position)[0] == GameMap.ASTEROIDS:
            raise InvalidStateException(f"Cannot overwrite asteroid at {position}")

        if state != GameMap.PLANET and self.get_tile(position)[0] == GameMap.PLANET:
            raise InvalidStateException(f"Cannot overwrite a planet at {position}")

        if (state, player_id) != GameMap.empty_tile and self.is_empty(position):
            self.empty_tiles -= 1
        elif (state, player_id) == GameMap.empty_tile and not self.is_empty(position):
            self.empty_tiles += 1

        self.tiles[position.y][position.x] = (state, player_id)

    def conquer_tile(self, position: Position, player_id: int) -> None:
        """
        Conquer the tile at the desired position

        Parameters
        ----------
        position : Position
            The position of the tile

        player_id : int
            The tile owner

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        self.check_position(position)
        cur_state, _ = self.get_tile(position)
        self.set_tile(position, state=cur_state, player_id=player_id)

    def clear_tile(self, position: Position) -> None:
        """
        Clear the tile at the desired position

        Parameters
        ----------
        position : Position
             The position of the tile

        Raises
        ------
        OutOfBoundExeption
             If the position is out of bound.
        """
        self.check_position(position)
        cur_state, _ = self.get_tile(position)
        if cur_state == GameMap.BLITZIUM or cur_state == GameMap.BLACK_HOLE:
            cur_state = GameMap.EMPTY
        self.set_tile(position, cur_state, None)

    def is_empty(self, position: Position) -> bool:
        """
        Checks if tile at position is empty

        Parameters
        ----------
        position : Position
            The position

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        self.check_position(position)
        return self.get_tile(position) == GameMap.empty_tile

    def is_conquered_by(self, position: Position, player_id: int) -> bool:
        """
        Checks if the tile at position is owned by you

        Parameters
        ----------
        position : Position
            The position of the tile

        player_id : int
            Your player id

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """

        self.check_position(position)
        state, owner = self.get_tile(position)
        return (state == GameMap.PLANET or state == GameMap.EMPTY) and owner == player_id

    def is_asteroids(self, position: Position) -> bool:
        """
        Checks if tile at position is an asteroids

        Parameters
        ----------
        position : Position
            The position

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        self.check_position(position)
        return self.get_tile(position)[0] == GameMap.ASTEROIDS

    def is_black_hole(self, position: Position) -> bool:
        """
        Checks if tile at position is a black hole

        Parameters
        ----------
        position : Position
            The position

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        self.check_position(position)
        return self.get_tile(position)[0] == GameMap.BLACK_HOLE

    def is_blitzium(self, position: Position) -> bool:
        """
        Checks if tile at position is a blitzium

        Parameters
        ----------
        position : Position
            The position

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        self.check_position(position)
        return self.get_tile(position)[0] == GameMap.BLITZIUM

    def is_planet(self, position: Position) -> bool:
        """
        Checks if tile at position is a planet

        Parameters
        ----------
        position : Position
            The position

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        self.check_position(position)
        return self.get_tile(position)[0] == GameMap.PLANET

    def get_owner(self, position: Position) -> Optional[int]:
        """
        Get the tile owner at position

        Parameters
        ----------
        position : Position
            The position of the tile

        Raises
        ------
        OutOfBoundExeption
            If the position is out of bound.
        """
        self.check_position(position)
        return self.tiles[position.y][position.x][1]

    def clear_tile_owned_by(self, player_id: int) -> None:
        """
        Clear all tiles owned by the player_id; sets them to empty

        Parameters
        ----------
        player_id : int
            The player id
        """
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles)):
                if self.get_owner(Position(x=x, y=y)) == player_id:
                    self.clear_tile(position=Position(x=x, y=y))

    def count_tiles_owned_by(self, player_id: int) -> int:
        conquered = 0
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles)):
                if self.get_owner(Position(x=x, y=y)) == player_id:
                    conquered += 1
        return conquered

    def find_path(
        self, start: Position, goal: Position, player_id: Optional[int] = None
    ) -> Tuple[bool, List[Position]]:
        init = start

        conquered_only = player_id is not None
        init_state = self.tiles[init.y][init.x]
        if conquered_only:
            goal_state = self.tiles[goal.y][goal.x]
            if goal_state[1] != player_id or init_state[1] != player_id:
                raise Exception(f"Invalid initial or goal states: {init}, {goal}")

        delta = [[-1, 0], [0, -1], [1, 0], [0, 1]]  # go up  # go left  # go down  # go right
        cost = 1

        y_size = len(self.tiles)
        x_size = len(self.tiles[0])
        closed = [[0] * x_size for y in range(y_size)]
        action = [[0] * x_size for y in range(y_size)]

        open = [(0, init)]
        found = False  # flag that is set when search complete

        while not found and len(open) > 0:
            # pick min from open
            current = min(open, key=lambda v: v[0])

            # expand
            open.remove(current)
            closed[current[1].y][current[1].x] = 1
            g, pos = current

            if pos.x == goal.x and pos.y == goal.y:
                found = True
            else:
                for i in range(len(delta)):
                    dir = delta[i]
                    x2 = pos.x + dir[1]
                    y2 = pos.y + dir[0]
                    if (
                        x2 >= 0
                        and x2 < x_size
                        and y2 >= 0
                        and y2 < y_size
                        and closed[y2][x2] == 0
                        and self.tiles[y2][x2][0] != GameMap.ASTEROIDS
                        and (not conquered_only or self.tiles[y2][x2][1] == init_state[1])
                    ):
                        open.append((cost + g, Position(x=x2, y=y2)))
                        closed[y2][x2] = 1
                        action[y2][x2] = i

        invpath = []
        if found:
            pos = goal
            invpath.append(pos)
            while pos != init:
                x2 = pos.x - delta[action[pos.y][pos.x]][1]
                y2 = pos.y - delta[action[pos.y][pos.x]][0]
                pos = Position(x=x2, y=y2)
                invpath.append(pos)

            invpath.reverse()

        return (found, invpath)

    def get_random_empty_position(self) -> Position:
        """
        Find a random starting position for a player
        """
        map_size = self.size
        pos = Position(x=random.randint(1, map_size - 1), y=random.randint(1, map_size - 1))
        while self.empty_tiles > 0 and not self.is_empty(pos):
            pos = Position(x=random.randint(1, map_size - 1), y=random.randint(1, map_size - 1))
        return pos

    def get_empty_tiles(self) -> List[Position]:
        empty = []
        for x in range(1, self.size - 1):
            for y in range(1, self.size - 1):
                if self.tiles[y][x] == GameMap.empty_tile:
                    empty.append(Position(x, y))
        return empty
