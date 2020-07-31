package codes.blitz.game.message;

import javax.websocket.DecodeException;
import javax.websocket.Decoder;
import javax.websocket.EndpointConfig;

import com.google.gson.FieldNamingPolicy;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import codes.blitz.game.message.game.GameMessage;

public class MessageDecoder implements Decoder.Text<GameMessage>
{

    private static Gson gson = new GsonBuilder().setFieldNamingPolicy(FieldNamingPolicy.LOWER_CASE_WITH_UNDERSCORES)
                                                .create();

    @Override
    public GameMessage decode(String message) throws DecodeException
    {
        return gson.fromJson(message, GameMessage.class);
    }

    @Override
    public boolean willDecode(String s)
    {
        return (s != null);
    }

    @Override
    public void init(EndpointConfig endpointConfig)
    {
        // Custom initialization logic
    }

    @Override
    public void destroy()
    {
        // Close resources
    }
}