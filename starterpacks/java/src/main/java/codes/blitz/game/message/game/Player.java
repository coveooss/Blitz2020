package codes.blitz.game.message.game;

import java.util.List;

public class Player
{
    private int id;
    private String name;
    private double score;
    private boolean active;
    private boolean killed;
    private Point position;
    private Point spawnPosition;
    private Direction direction;
    private List<Point> tail;
    private List<Turn> history;

    public int getId()
    {
        return id;
    }

    public void setId(int id)
    {
        this.id = id;
    }

    public String getName()
    {
        return name;
    }

    public void setName(String name)
    {
        this.name = name;
    }

    public double getScore()
    {
        return score;
    }

    public void setScore(double score)
    {
        this.score = score;
    }

    public boolean isActive()
    {
        return active;
    }

    public void setActive(boolean active)
    {
        this.active = active;
    }

    public boolean isKilled()
    {
        return killed;
    }

    public void setKilled(boolean killed)
    {
        this.killed = killed;
    }

    public Point getPosition()
    {
        return position;
    }

    public void setPosition(Point position)
    {
        this.position = position;
    }

    public Point getSpawnPosition()
    {
        return spawnPosition;
    }

    public void setSpawnPosition(Point spawnPosition)
    {
        this.spawnPosition = spawnPosition;
    }

    public Direction getDirection()
    {
        return direction;
    }

    public void setDirection(Direction direction)
    {
        this.direction = direction;
    }

    public List<Point> getTail()
    {
        return tail;
    }

    public void setTail(List<Point> tail)
    {
        this.tail = tail;
    }

    public List<Turn> getHistory()
    {
        return history;
    }

    public void setHistory(List<Turn> history)
    {
        this.history = history;
    }

    @Override
    public int hashCode()
    {
        final int prime = 31;
        int result = 1;
        result = prime * result + (active ? 1231 : 1237);
        result = prime * result + ((direction == null) ? 0 : direction.hashCode());
        result = prime * result + ((history == null) ? 0 : history.hashCode());
        result = prime * result + id;
        result = prime * result + (killed ? 1231 : 1237);
        result = prime * result + ((name == null) ? 0 : name.hashCode());
        result = prime * result + ((position == null) ? 0 : position.hashCode());
        long temp;
        temp = Double.doubleToLongBits(score);
        result = prime * result + (int) (temp ^ (temp >>> 32));
        result = prime * result + ((spawnPosition == null) ? 0 : spawnPosition.hashCode());
        result = prime * result + ((tail == null) ? 0 : tail.hashCode());
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
        Player other = (Player) obj;
        if (active != other.active) {
            return false;
        }
        if (direction != other.direction) {
            return false;
        }
        if (history == null) {
            if (other.history != null) {
                return false;
            }
        } else if (!history.equals(other.history)) {
            return false;
        }
        if (id != other.id) {
            return false;
        }
        if (killed != other.killed) {
            return false;
        }
        if (name == null) {
            if (other.name != null) {
                return false;
            }
        } else if (!name.equals(other.name)) {
            return false;
        }
        if (position == null) {
            if (other.position != null) {
                return false;
            }
        } else if (!position.equals(other.position)) {
            return false;
        }
        if (Double.doubleToLongBits(score) != Double.doubleToLongBits(other.score)) {
            return false;
        }
        if (spawnPosition == null) {
            if (other.spawnPosition != null) {
                return false;
            }
        } else if (!spawnPosition.equals(other.spawnPosition)) {
            return false;
        }
        if (tail == null) {
            if (other.tail != null) {
                return false;
            }
        } else if (!tail.equals(other.tail)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString()
    {
        return "Player [id=" + id + ", name=" + name + ", score=" + score + ", active=" + active + ", killed=" + killed
                + ", position=" + position + ", spawnPosition=" + spawnPosition + ", direction=" + direction + ", tail="
                + tail + ", history=" + history + "]";
    }
}
