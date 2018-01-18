import com.rabbitmq.client.ConnectionFactory;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.DefaultConsumer;
import com.rabbitmq.client.AMQP;
import com.rabbitmq.client.Envelope;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;

import java.io.IOException;
import java.util.UUID;
import java.util.concurrent.ArrayBlockingQueue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.TimeoutException;

public class ModelInferenceRpcClient {

    private Connection connection;
    private Channel channel;
    private String requestQueueName = "rpc_queue";
    private String replyQueueName;

    public ModelInferenceRpcClient() throws IOException, TimeoutException {
        ConnectionFactory factory = new ConnectionFactory();
        factory.setHost("white-swan.rmq.cloudamqp.com");
        factory.setVirtualHost("rxuhxbbh");
        factory.setUsername("rxuhxbbh");
        factory.setPassword("mkywerCtgEVDC-LOARLwgi7mm4xhteZA");

        connection = factory.newConnection();
        channel = connection.createChannel();

        replyQueueName = channel.queueDeclare().getQueue();
    }

    public String call(JSONObject input) throws IOException, InterruptedException {
        String corrId = UUID.randomUUID().toString();
        AMQP.BasicProperties props = new AMQP.BasicProperties
                .Builder()
                .correlationId(corrId)
                .replyTo(replyQueueName)
                .build();

        channel.basicPublish("", requestQueueName, props, input.toJSONString().getBytes("UTF-8"));

        final BlockingQueue<String> response = new ArrayBlockingQueue<String>(1);

        channel.basicConsume(replyQueueName, true, new DefaultConsumer(channel) {
            @Override
            public void handleDelivery(String consumerTag, Envelope envelope, AMQP.BasicProperties properties, byte[] body) throws IOException {
                if (properties.getCorrelationId().equals(corrId)) {
                    response.offer(new String(body, "UTF-8"));
                }
            }
        });

        return response.take();
    }

    public void close() throws IOException {
        connection.close();
    }

    @SuppressWarnings("unchecked")
    public static void main(String[] argv) {
        ModelInferenceRpcClient ModelInferenceRpc = null;
        String response = null;
        try {
            ModelInferenceRpc = new ModelInferenceRpcClient();
            System.out.println(" [x] Requesting fib(10)");
            JSONObject obj = new JSONObject();
            obj.put("model", "fib");
            obj.put("n", new Integer(10));
            response = ModelInferenceRpc.call(obj);
            System.out.println(" [.] Got '" + response + "'");
        }
        catch  (IOException | TimeoutException | InterruptedException e) {
            e.printStackTrace();
        }
        finally {
            if (ModelInferenceRpc!= null) {
                try {
                    ModelInferenceRpc.close();
                }
                catch (IOException _ignore) {}
            }
        }
    }
}