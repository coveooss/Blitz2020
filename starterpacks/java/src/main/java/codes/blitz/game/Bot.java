package codes.blitz.game;

import java.util.Map;
import java.util.Random;

import codes.blitz.game.message.bot.Move;
import codes.blitz.game.message.game.Game;
import codes.blitz.game.message.game.GameMessage;
import codes.blitz.game.message.game.Player;

public class Bot
{
    private static final Random random = new Random();
    private static final Move[] POSSIBLE_MOVES = Move.class.getEnumConstants();

    public Bot()
    {
        // initialize some variables you will need throughout the game here
    }

    public Move getNextMove(GameMessage gameMessage)
    {
        // Here is where the magic happens, for now the moves are random. I bet you can do better ;)

        Map<Integer, Player> playersByIdMap = gameMessage.generatePlayersByIdMap();

        Move[] legalMoves = getLegalMovesForCurrentTick(gameMessage.getGame(), playersByIdMap);

        // You can print out a pretty version of the map but be aware that 
        // printing out long strings can impact your bot performance (30 ms in average).
        // System.out.println(gameMessage.getGame().getPrettyMap());

        return legalMoves[random.nextInt(legalMoves.length)];
    }

    public Move[] getLegalMovesForCurrentTick(Game game, Map<Integer, Player> playersByIdMap)
    {
        // You should define here what moves are legal for your current position and direction so that your bot does not send a lethal move

        // Your bot moves are done according to its direction, if you are in the DOWN direction.
        // A TURN_RIGHT move will make your bot move left in the map visualization (replay or logs)

        Player me = playersByIdMap.get(game.getPlayerId());

        return POSSIBLE_MOVES;
    }
}
