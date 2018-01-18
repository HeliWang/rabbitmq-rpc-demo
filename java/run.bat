@echo off
set CPC=./;jars/amqp-client-4.0.2.jar;jars/json-simple-1.1.1.jar
set CP=./;jars/amqp-client-4.0.2.jar;jars/slf4j-api-1.7.21.jar;jars/slf4j-simple-1.7.22.jar;jars/json-simple-1.1.1.jar
javac -classpath %CPC% ModelInferenceRpcClient.java  -Xlint:unchecked
java -classpath %CP% ModelInferenceRpcClient