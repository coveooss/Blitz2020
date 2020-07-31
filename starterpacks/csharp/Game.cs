using System;

public enum TileType
{
    EMPTY, ASTEROIDS, CONQUERED, BLITZIUM, PLANET, CONQUERED_PLANET, BLACK_HOLE
}

public class Game
{
    public String prettyMap;
    public String[][] map;
    public int tick;
    public int ticksLeft;
    public int playerId;

    public class Position
    {
        public int x;
        public int y;

        public override string ToString()
        {
            return String.Format("({0}, {1})", x, y);
        }
    }

    public class PointOutOfMapException : Exception
    {
        public PointOutOfMapException(Position position, int size)
        : base(String.Format("Point {0} is out of map, x and y must be greater than 0 and less than {1}.", position, size))
        { }
    }

    public class TileIsNotCapturedException : Exception
    {
        public TileIsNotCapturedException(Position position, TileType tile)
        : base(String.Format("Tile at {0} is not captured, TileType is {1}", position, tile))
        { }
    }

    public int getMapSize()
    {
        return this.map.Length;
    }

    public int getTileOwnerId(Position position)
    {
        this.validateTileExists(position);

        string rawTile = this.getRawTileValueAt(position);
        TileType tile = this.getTileTypeAt(position);

        if (!rawTile.Contains("-"))
        {
            throw new TileIsNotCapturedException(position, tile);
        }

        return int.Parse(rawTile.Split("-")[1]);
    }

    public TileType getTileTypeAt(Position position)
    {
        string rawTile = this.getRawTileValueAt(position);

        switch (rawTile)
        {
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
                if (rawTile.StartsWith("C-"))
                {
                    return TileType.CONQUERED;
                }
                else if (rawTile.StartsWith("%-"))
                {
                    return TileType.CONQUERED_PLANET;
                }

                throw new ArgumentException(String.Format("'{0}' is not a valid tile", rawTile));
        }
    }

    public String getRawTileValueAt(Position position)
    {
        this.validateTileExists(position);
        return this.map[position.y][position.x];
    }

    public void validateTileExists(Position position)
    {
        if (position.x < 0 || position.y < 0 || position.x >= this.getMapSize() || position.y >= this.getMapSize())
        {
            throw new PointOutOfMapException(position, this.getMapSize());
        }
    }
}