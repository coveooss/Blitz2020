package codes.blitz.game.message.exception;

public class PointOutOfMapException extends Exception
{
    private static final long serialVersionUID = 1L;

    public PointOutOfMapException(String message)
    {
        super(message);
    }
}
