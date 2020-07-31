package codes.blitz.game.message.bot;

import codes.blitz.game.message.MessageType;

public class BotMessage
{
    private MessageType type;
    private Move action;
    private String name;
    private String token;
    private Integer tick;


    public Integer getTick() 
    {
        return this.tick;
    }

    public void setTick(Integer tick) 
    {
        this.tick = tick;
    }

    public MessageType getType()
    {
        return type;
    }

    public void setType(MessageType type)
    {
        this.type = type;
    }

    public Move getAction()
    {
        return action;
    }

    public void setAction(Move action)
    {
        this.action = action;
    }

    public String getName()
    {
        return name;
    }

    public void setName(String name)
    {
        this.name = name;
    }

    public String getToken()
    {
        return token;
    }

    public void setToken(String token)
    {
        this.token = token;
    }

    @Override
    public int hashCode()
    {
        final int prime = 31;
        int result = 1;
        result = prime * result + ((action == null) ? 0 : action.hashCode());
        result = prime * result + ((name == null) ? 0 : name.hashCode());
        result = prime * result + ((token == null) ? 0 : token.hashCode());
        result = prime * result + ((type == null) ? 0 : type.hashCode());
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
        BotMessage other = (BotMessage) obj;
        if (action != other.action) {
            return false;
        }
        if (name == null) {
            if (other.name != null) {
                return false;
            }
        } else if (!name.equals(other.name)) {
            return false;
        }
        if (token == null) {
            if (other.token != null) {
                return false;
            }
        } else if (!token.equals(other.token)) {
            return false;
        }
        if (type != other.type) {
            return false;
        }
        return true;
    }

    @Override
    public String toString()
    {
        return "BotMessage [type=" + type + ", action=" + action + ", name=" + name + ", token=" + token + "]";
    }
}
