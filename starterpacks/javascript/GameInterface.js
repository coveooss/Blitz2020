"use strict";
Object.defineProperty(exports, "__esModule", { value: true });

var MOVES;
(function (MOVES) {
    MOVES["TURN_LEFT"] = "TURN_LEFT";
    MOVES["TURN_RIGHT"] = "TURN_RIGHT";
    MOVES["FORWARD"] = "FORWARD";
})(MOVES = exports.MOVES || (exports.MOVES = {}));

var DIRECTIONS;
(function (DIRECTIONS) {
    DIRECTIONS["LEFT"] = "LEFT";
    DIRECTIONS["RIGHT"] = "RIGHT";
    DIRECTIONS["UP"] = "UP";
    DIRECTIONS["DOWN"] = "DOWN";
})(DIRECTIONS = exports.DIRECTIONS || (exports.DIRECTIONS = {}));
var TileType;
(function (TileType) {
    TileType["EMPTY"] = "EMPTY";
    TileType["ASTEROIDS"] = "ASTEROIDS";
    TileType["PLANET"] = "PLANET";
    TileType["BLITZIUM"] = "BLITZIUM";
    TileType["BLACK_HOLE"] = "BLACK_HOLE";
    TileType["CONQUERED"] = "CONQUERED";
    TileType["CONQUERED_PLANET"] = "CONQUERED_PLANET";
})(TileType = exports.TileType || (exports.TileType = {}));


class PointOutOfMapException extends Error {
    constructor(point, size) {
        super(`Point {${point.x}, ${point.y}} is out of map, x and y must be greater than 0 and less than ${size}.`);
    }
}
exports.PointOutOfMapException = PointOutOfMapException;

class TileIsNotCapturedException extends Error {
    constructor(point, tile) {
        super(`Tile at {${point.x}, ${point.y}}  is not captured, TileType is ${tile}.`);
    }
}

exports.TileIsNotCapturedException = TileIsNotCapturedException;

class GameMessage {
    constructor(rawTick) {
        this.type = rawTick.type;
        this.game = rawTick.game;
        this.players = rawTick.players;
    }

    getMapSize() {
        return this.game.map.length;
    }

    validateTileExists(position) {
        if (position.x < 0 || position.y < 0 || position.x >= this.getMapSize() || position.y >= this.getMapSize()) {
            throw new PointOutOfMapException(position, this.getMapSize());
        }
    }

    getRawTileValueAt(position) {
        this.validateTileExists(position);
        return this.game.map[position.y][position.x];
    }

    getTileTypeAt(position) {
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

    getTileOwnerId(position) {
        this.validateTileExists(position);
        let rawTile = this.getRawTileValueAt(position);
        let tile = this.getTileTypeAt(position);

        if (rawTile.indexOf("-") === -1) {
            throw new TileIsNotCapturedException(position, tile);
        }

        return Number(rawTile.split("-")[1]);
    }

    getPlayerMapById() {
        return new Map(this.players.map(p => [p.id, p]));
    }
}

exports.GameMessage = GameMessage;