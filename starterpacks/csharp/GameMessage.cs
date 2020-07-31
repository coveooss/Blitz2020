using System.Collections.Generic;
using System.Linq;

namespace Blitz2020
{
    public class GameMessage
    {
        public List<Player> players;
        public Game game;

        public string type;

        public Dictionary<int, Player> getPlayerMapById
        {
            get { return this.players.ToDictionary(p => p.id, p => p); }
        }
    }
}