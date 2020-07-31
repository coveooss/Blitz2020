/**
 * Copyright (c) 2011 - 2019, Coveo Solutions Inc.
 */
package codes.blitz.game.message.game;

public enum TileType
{
    EMPTY, ASTEROIDS, CONQUERED, BLITZIUM, PLANET, CONQUERED_PLANET, BLACK_HOLE;

    public static TileType getTileTypeFromString(String rawTile)
    {
        switch (rawTile) {
            case " ":
                return EMPTY;
            case "W":
                return ASTEROIDS;
            case "%":
                return PLANET;
            case "$":
                return BLITZIUM;
            case "!":
                return BLACK_HOLE;
            default:
                if (rawTile.startsWith("C-")) {
                    return CONQUERED;
                } else if (rawTile.startsWith("%-")) {
                    return CONQUERED_PLANET;
                }
                throw new IllegalArgumentException(String.format("'%s' is not a valid tile", rawTile));
        }
    }
}
