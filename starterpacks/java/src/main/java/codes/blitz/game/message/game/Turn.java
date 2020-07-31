package codes.blitz.game.message.game;

public class Turn
{
    private int tick;
    private String message;

    public int getTick()
    {
        return tick;
    }

    public void setTick(int tick)
    {
        this.tick = tick;
    }

    public String getMessage()
    {
        return message;
    }

    public void setMessage(String message)
    {
        this.message = message;
    }

    @Override
    public int hashCode()
    {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((message == null) ? 0 : message.hashCode());
        result = prime * result + tick;
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
        Turn other = (Turn) obj;
        if (message == null) {
            if (other.message != null) {
                return false;
            }
        } else if (!message.equals(other.message)) {
            return false;
        }
        if (tick != other.tick) {
            return false;
        }
        return true;
    }

    @Override
    public String toString()
    {
        return "Turn [tick=" + tick + ", message=" + message + "]";
    }
}
