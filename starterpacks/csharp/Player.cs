using static Game;

public class Player
{
    public enum Move
    {
        TURN_LEFT,
        TURN_RIGHT,
        FORWARD
    }

    public enum Direction
    {
        LEFT, RIGHT, DOWN, UP
    }

    public int id;
    public string name;
    public double score;
    public bool active;
    public bool killed;
    public Direction direction;

    public Position position;
    public Position spawnPosition;
    public Position[] tail;
}