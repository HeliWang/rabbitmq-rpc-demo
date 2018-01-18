set CP=.;amqp-client-4.0.2.jar;slf4j-api-1.7.21.jar;slf4j-simple-1.7.22.jar
javac -classpath amqp-client-4.0.2.jar ModelInferenceRpcClient.java Send.java
java -cp %CP% Send