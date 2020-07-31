using System;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;
using System.Text;
using Newtonsoft.Json;
using Blitz2020;
using Newtonsoft.Json.Serialization;

public static class Application
{
    public static void Main(string[] args)
    {
        Task t = startClient();
        t.Wait();
    }


    public async static Task startClient(string address = "127.0.0.1:8765")
    {
        using (ClientWebSocket webSocket = new ClientWebSocket())
        {
            Uri serverUri = new Uri("ws://" + address);
            Bot bot = new Bot();

            await webSocket.ConnectAsync(serverUri, CancellationToken.None);

            string? token = Environment.GetEnvironmentVariable("TOKEN");
            string registerPayload = "";

            if (token == null)
            {
                registerPayload = "{\"type\": \"register\", \"name\": \"" + Bot.NAME + "\"}";
            }
            else
            {
                registerPayload = "{\"type\": \"register\", \"token\": \"" + token + "\"}";
            }

            await webSocket.SendAsync(
                new ArraySegment<byte>(Encoding.UTF8.GetBytes(registerPayload)),
                WebSocketMessageType.Text, true, CancellationToken.None);

            while (webSocket.State == WebSocketState.Open)
            {
                DefaultContractResolver contractResolver = new DefaultContractResolver
                {
                    NamingStrategy = new SnakeCaseNamingStrategy()
                };

                GameMessage message = JsonConvert.DeserializeObject<GameMessage>(await readMessage(webSocket), new JsonSerializerSettings
                {
                    ContractResolver = contractResolver,
                    Formatting = Formatting.Indented
                });

                if (message != null)
                {
                    Player.Move move = bot.nextMove(message);

                    await webSocket.SendAsync(
                        Encoding.UTF8.GetBytes("{\"type\": \"move\", \"action\": \"" + move.ToString() + "\", \"tick\": " + message.game.tick + "}"),
                        WebSocketMessageType.Text,
                        true, CancellationToken.None);
                }
            }
        }
    }

    public async static Task<string> readMessage(ClientWebSocket client)
    {
        string result = "";

        WebSocketReceiveResult receiveResult;
        do
        {
            ArraySegment<byte> segment = new ArraySegment<byte>(new byte[1024]);
            receiveResult = await client.ReceiveAsync(segment, CancellationToken.None);
            result += Encoding.UTF8.GetString(segment.Array);
        } while (!receiveResult.EndOfMessage);


        return result;
    }
}