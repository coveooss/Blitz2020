"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};

Object.defineProperty(exports, "__esModule", { value: true });

const ws_1 = __importDefault(require("ws"));
const Bot_1 = require("./Bot");
const GameInterface_1 = require("./GameInterface");
const webSocket = new ws_1.default("ws://0.0.0.0:8765");
let bot;


webSocket.onopen = (event) => {
    bot = new Bot_1.Bot();
    if (process.env.TOKEN) {
        webSocket.send(JSON.stringify({ type: "register", token: process.env.TOKEN }));
    }
    else {
        webSocket.send(JSON.stringify({ type: "register", name: "MyBot" }));
    }
};


webSocket.onmessage = (message) => {
    let rawGameMessage = JSON.parse(message.data.toString());
    let gameMessage = new GameInterface_1.GameMessage(rawGameMessage);
    webSocket.send(JSON.stringify({
        type: "move",
        action: bot.getNextMove(gameMessage),
        tick: gameMessage.game.tick
    }));
};