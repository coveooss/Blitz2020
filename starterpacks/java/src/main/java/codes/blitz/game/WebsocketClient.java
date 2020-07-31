package codes.blitz.game;

import java.io.IOException;
import java.util.concurrent.CountDownLatch;

import javax.websocket.ClientEndpoint;
import javax.websocket.CloseReason;
import javax.websocket.EncodeException;
import javax.websocket.OnClose;
import javax.websocket.OnMessage;
import javax.websocket.OnOpen;
import javax.websocket.Session;

import codes.blitz.game.message.MessageDecoder;
import codes.blitz.game.message.MessageEncoder;
import codes.blitz.game.message.MessageType;
import codes.blitz.game.message.bot.BotMessage;
import codes.blitz.game.message.game.GameMessage;

@ClientEndpoint(decoders = MessageDecoder.class, encoders = MessageEncoder.class)
public class WebsocketClient
{
    private Bot bot;
    private CountDownLatch latch;

    public WebsocketClient(CountDownLatch latch)
    {
        this.latch = latch;
        this.bot = new Bot();
    }

    @OnOpen
    public void onOpen(Session session) throws IOException, EncodeException
    {
        BotMessage message = new BotMessage();
        message.setType(MessageType.REGISTER);
        if (System.getenv("TOKEN") != null) {
            String token = System.getenv("TOKEN");
            message.setToken(token);
        } else {
            message.setName("MyBot");
        }

        session.getBasicRemote().sendObject(message);
    }

    @OnMessage
    public void processMessageFromServer(GameMessage receivedMessage, Session session)
            throws IOException,
                EncodeException
    {
        System.out.println("\nTurn " + receivedMessage.getGame().getTick());
        // Send back a move
        BotMessage botMessage = new BotMessage();
        botMessage.setType(MessageType.MOVE);
        botMessage.setTick(receivedMessage.getGame().getTick());
        botMessage.setAction(bot.getNextMove(receivedMessage));

        session.getBasicRemote().sendObject(botMessage);

    }

    @OnClose
    public void onClose(Session session, CloseReason closeReason)
    {
        latch.countDown();
    }
}
