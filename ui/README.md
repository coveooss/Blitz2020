# Blitz 2020 UI

Blitz 2020 UI application

The UI is split in 3 different applications:

-   Viewer
-   HumanBot
-   Replay

## Viewer

The viewer automatically connects on the websocket and stream the game. No interaction are possible.

## HumanBot

The human bot connects to the server and register as a player.
It can be usefull if you want to try to beat your own bot or if you want to test some scenarios more easily.
Use the arrow key to move.

## Replay

The replay loads a file and mimic the streaming of the game. You can interact with the replay via some shortcuts:

-   Space: pause/un-pause the game
-   Z: go to game start
-   X: go to game end
-   , (Comma): go back one tick
-   . (Period): go forward one tick
-   1-5: set replay speed

## Instructions

NodeJs must be installed on your system

```
> npm install
> npm start
```

Then you can open

-   http://localhost:1234/viewer.html
-   http://localhost:1234/human_bot.html
-   http://localhost:1234/replay.html (currently loads a mock)

### Tests

You can run tests using `npm test`. Tests are located in the `src/**/tests` folder.
Coverage will be run automatically and you can see the html report if you open the `coverage/index.html` file

# TODOs

-   Game elements

    -   Show Asteroids
    -   Show Planet
    -   Show Blitzium
    -   Show Black holes

-   Stats
    -   Show scores
    -   Show player names
    -   Additionnal stats (nemesis, kill count, suicide count, etc)
