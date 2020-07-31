"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const GameInterface = require("./GameInterface");

class Bot {
  constructor() {
    // This method should be use to initialize some variables you will need throughout the game.
  }

  /**
   * @param {GameInterface.GameMessage} gameMessage
   */
  getNextMove(gameMessage) {
    // Here is where the magic happens, for now the moves are random. I bet you can do better ;)
    const POSSIBLE_MOVES = this.getLegalMovesForCurrentTick(gameMessage);

    // You can print out a pretty version of the map but be aware that
    // printing out long strings can impact your bot performance (30 ms in average).
    // console.log(gameMessage.game.pretty_map);

    return POSSIBLE_MOVES[Math.floor(Math.random() * POSSIBLE_MOVES.length)];
  }

  
  /**
   * @param {GameInterface.GameMessage} gameMessage
   */
  getLegalMovesForCurrentTick(gameMessage) {
    // You should define here what moves are legal for your current position and direction so that your bot does not send a lethal move
    // Your bot moves are done according to its direction, if you are in the DOWN direction.
    // A TURN_RIGHT move will make your bot move left in the map visualization (replay or logs)


    let me = gameMessage.getPlayerMapById().get(gameMessage.game.player_id);
    return Object.values(GameInterface.MOVES);
  }
}

exports.Bot = Bot;
