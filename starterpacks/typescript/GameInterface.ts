export enum MOVES {
  TURN_LEFT = "TURN_LEFT",
  TURN_RIGHT = "TURN_RIGHT",
  FORWARD = "FORWARD",
};

export enum DIRECTIONS {
  LEFT = 'LEFT',
  RIGHT = 'RIGHT',
  UP = 'UP',
  DOWN = 'DOWN',
}

export enum TileType {
  EMPTY = "EMPTY",
  ASTEROIDS = "ASTEROIDS",
  PLANET = "PLANET",
  BLITZIUM = "BLITZIUM",
  BLACK_HOLE = "BLACK_HOLE",
  CONQUERED = "CONQUERED",
  CONQUERED_PLANET = "CONQUERED_PLANET"
}

export interface IPosition {
  x: number;
  y: number;
}

export interface IHistoryMessage {
  timestamp: string;
  tick: number;
  message: string;
}

export interface IPlayer {
  active: boolean;
  killed: boolean;
  position: IPosition;
  spawn_position: IPosition;
  direction: DIRECTIONS;
  tail: IPosition[];
  id: number;
  name: string;
  score: number;
  stats: any;
  history: IHistoryMessage[];
}

export interface IGameTick {
  type: string;
  game: {
    map: string[][];
    player_id: number;
    tick: number;
    ticks_left: number;
    pretty_map: string;
  };
  players: IPlayer[];
}

export class PointOutOfMapException extends Error {
  constructor(point: IPosition, size: number) {
    super(`Point {${point.x}, ${point.y}} is out of map, x and y must be greater than 0 and less than ${size}.`);
  }
}

export class TileIsNotCapturedException extends Error {
  constructor(point: IPosition, tile: TileType) {
    super(`Tile at {${point.x}, ${point.y}}  is not captured, TileType is ${tile}.`);
  }
}

export class GameMessage implements IGameTick {
  public type: string;
  public game: { map: string[][]; player_id: number; tick: number; ticks_left: number; pretty_map: string; };
  public players: IPlayer[];

  constructor(rawTick: IGameTick) {
    this.type = rawTick.type;
    this.game = rawTick.game;
    this.players = rawTick.players;
  }

  public getMapSize(): number {
    return this.game.map.length;
  }

  public validateTileExists(position: IPosition) {
    if (position.x < 0 || position.y < 0 || position.x >= this.getMapSize() || position.y >= this.getMapSize()) {
      throw new PointOutOfMapException(position, this.getMapSize());
    }
  }

  public getRawTileValueAt(position: IPosition) {
    this.validateTileExists(position);
    return this.game.map[position.y][position.x];
  }

  public getTileTypeAt(position: IPosition): TileType {
    let rawTile = this.getRawTileValueAt(position);

    switch (rawTile) {
      case " ":
        return TileType.EMPTY;
      case "W":
        return TileType.ASTEROIDS;
      case "%":
        return TileType.PLANET;
      case "$":
        return TileType.BLITZIUM;
      case "!":
        return TileType.BLACK_HOLE;
      default:
        if (rawTile.startsWith("C-")) {
          return TileType.CONQUERED;
        }
        else if (rawTile.startsWith("%-")) {
          return TileType.CONQUERED_PLANET;
        }

        throw new Error(`"${rawTile}" is not a valid tile`);
    }
  }

  public getTileOwnerId(position: IPosition) {
    this.validateTileExists(position);

    let rawTile = this.getRawTileValueAt(position);
    let tile = this.getTileTypeAt(position);

    if (rawTile.indexOf("-") === -1) {
      throw new TileIsNotCapturedException(position, tile);
    }

    return Number(rawTile.split("-")[1]);
  }

  public getPlayerMapById() {
    return new Map<number, IPlayer>(this.players.map(p => [p.id, p]));
  }
}
