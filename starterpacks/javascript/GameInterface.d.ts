export declare enum MOVES {
    TURN_LEFT = "TURN_LEFT",
    TURN_RIGHT = "TURN_RIGHT",
    FORWARD = "FORWARD"
}
export declare enum DIRECTIONS {
    LEFT = "LEFT",
    RIGHT = "RIGHT",
    UP = "UP",
    DOWN = "DOWN"
}
export declare enum TileType {
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
export declare class PointOutOfMapException extends Error {
    constructor(point: IPosition, size: number);
}
export declare class TileIsNotCapturedException extends Error {
    constructor(point: IPosition, tile: TileType);
}
export declare class GameMessage implements IGameTick {
    type: string;
    game: {
        map: string[][];
        player_id: number;
        tick: number;
        ticks_left: number;
        pretty_map: string;
    };
    players: IPlayer[];
    constructor(rawTick: IGameTick);
    getMapSize(): number;
    validateTileExists(position: IPosition): void;
    getRawTileValueAt(position: IPosition): string;
    getTileTypeAt(position: IPosition): TileType;
    getTileOwnerId(position: IPosition): number;
    getPlayerMapById(): Map<number, IPlayer>;
}
