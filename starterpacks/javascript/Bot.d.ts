import { MOVES, GameMessage } from "./GameInterface";
export declare class Bot {
    constructor();
    getNextMove(gameMessage: GameMessage): MOVES;
    getLegalMovesForCurrentTick(gameMessage: GameMessage): MOVES[];
}
