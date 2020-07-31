package codes.blitz.game.message.exception;

public class TileIsNotCapturedException extends Exception
{
    private static final long serialVersionUID = 1L;

    public TileIsNotCapturedException(String message)
    {
        super(message);
    }
}
