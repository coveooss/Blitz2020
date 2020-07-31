package codes.blitz.game.message.game;

import java.util.List;

import codes.blitz.game.message.exception.PointOutOfMapException;
import codes.blitz.game.message.exception.TileIsNotCapturedException;

public class Game
{
    private String prettyMap;
    private List<List<String>> map;
    private int tick;
    private int ticksLeft;
    private int playerId;

    public int getTileOwnerId(Point point) throws PointOutOfMapException, TileIsNotCapturedException
    {
        validateTileExists(point);

        String tile = getRawTileValueAt(point);
        if (!tile.contains("-")) {
            throw new TileIsNotCapturedException(String.format("The tile at y: '%d', x: '%d' is not captured.",
                                                               point.y,
                                                               point.x));
        }
        return Integer.parseInt(tile.split("-")[1]);
    }

    public TileType getTileTypeAt(Point point) throws PointOutOfMapException
    {
        validateTileExists(point);

        return TileType.getTileTypeFromString(getRawTileValueAt(point));
    }

    public String getRawTileValueAt(Point point) throws PointOutOfMapException
    {
        validateTileExists(point);

        return map.get(point.y).get(point.x);
    }

    public int getMapSize()
    {
        return map.size();
    }

    public String getPrettyMap()
    {
        return prettyMap;
    }

    public void setPrettyMap(String prettyMap)
    {
        this.prettyMap = prettyMap;
    }

    public List<List<String>> getMap()
    {
        return map;
    }

    public void setMap(List<List<String>> map)
    {
        this.map = map;
    }

    public int getTick()
    {
        return tick;
    }

    public void setTick(int tick)
    {
        this.tick = tick;
    }

    public int getTicksLeft()
    {
        return ticksLeft;
    }

    public void setTicksLeft(int ticksLeft)
    {
        this.ticksLeft = ticksLeft;
    }

    public int getPlayerId()
    {
        return playerId;
    }

    public void setPlayerId(int playerId)
    {
        this.playerId = playerId;
    }

    @Override
    public int hashCode()
    {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((map == null) ? 0 : map.hashCode());
        result = prime * result + playerId;
        result = prime * result + ((prettyMap == null) ? 0 : prettyMap.hashCode());
        result = prime * result + tick;
        result = prime * result + ticksLeft;
        return result;
    }

    @Override
    public boolean equals(Object obj)
    {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        Game other = (Game) obj;
        if (map == null) {
            if (other.map != null) {
                return false;
            }
        } else if (!map.equals(other.map)) {
            return false;
        }
        if (playerId != other.playerId) {
            return false;
        }
        if (prettyMap == null) {
            if (other.prettyMap != null) {
                return false;
            }
        } else if (!prettyMap.equals(other.prettyMap)) {
            return false;
        }
        if (tick != other.tick) {
            return false;
        }
        if (ticksLeft != other.ticksLeft) {
            return false;
        }
        return true;
    }

    @Override
    public String toString()
    {
        return "Game [prettyMap=" + prettyMap + ", map=" + map + ", tick=" + tick + ", ticksLeft=" + ticksLeft
                + ", playerId=" + playerId + "]";
    }

    private void validateTileExists(Point point) throws PointOutOfMapException
    {
        if (point.y < 0 || !(point.y < map.size())) {
            throw new PointOutOfMapException(String.format("y: '%d' is out of bounds. Max y is '%d'.",
                                                           point.y,
                                                           map.size() - 1));
        }
        if (point.x < 0 || !(point.x < map.get(point.y).size())) {
            throw new PointOutOfMapException(String.format("x: '%d' is out of bounds. Max x is '%d'.",
                                                           point.x,
                                                           map.get(point.y).size() - 1));
        }
    }
}
