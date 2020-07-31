import WebSocket from "ws";
import { Bot } from "./Bot";
import { GameMessage } from "./GameInterface";

const webSocket = new WebSocket("ws://0.0.0.0:8765");
let bot;

webSocket.onopen = (event: WebSocket.OpenEvent) => {
  bot = new Bot();
  if (process.env.TOKEN) {
    webSocket.send(
      JSON.stringify({ type: "register", token: process.env.TOKEN })
    );
  } else {
    webSocket.send(JSON.stringify({ type: "register", name: "MyBot" }));
  }
};

webSocket.onmessage = (message: WebSocket.MessageEvent) => {
  let rawGameMessage = JSON.parse(message.data.toString())
  let gameMessage = new GameMessage(rawGameMessage);

  webSocket.send(
    JSON.stringify({
      type: "move",
      action: bot.getNextMove(gameMessage),
      tick: gameMessage.game.tick
    })
  );
};
