using System;

namespace Blitz2020
{
    public class Bot
    {
        public static string NAME = "MyBot C#";
        public static Player.Move[] POSSIBLE_MOVES = (Player.Move[])Enum.GetValues(typeof(Player.Move));

        public Bot()
        {
            // initialize some variables you will need throughout the game here
        }

        public Player.Move nextMove(GameMessage gameMessage)
        {
            // Here is where the magic happens, for now the moves are random. I bet you can do better ;)
            Player.Move[] legalMoves = getLegalMovesForCurrentTick(gameMessage);
            Random random = new Random();

            // You can print out a pretty version of the map but be aware that 
            // printing out long strings can impact your bot performance (30 ms in average).
            // Console.WriteLine(gameMessage.game.prettyMap);

            return legalMoves[random.Next(legalMoves.Length)];
        }

        public Player.Move[] getLegalMovesForCurrentTick(GameMessage gameMessage)
        {
            // You should define here what moves are legal for your current position and direction so that your bot does not send a lethal move

            // Your bot moves are done according to its direction, if you are in the DOWN direction.
            // A TURN_RIGHT move will make your bot move left in the map visualization (replay or logs)
            
            Player me;
            gameMessage.getPlayerMapById.TryGetValue(gameMessage.game.playerId, out me);

            return POSSIBLE_MOVES;
        }
    }
}