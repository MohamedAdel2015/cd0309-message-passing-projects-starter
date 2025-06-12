from concurrent import futures
import os
from kafka import KafkaProducer
import grpc
import json

import location_pb2
import location_pb2_grpc

TOPIC_NAME = os.environ["TOPIC_NAME"]
KAFKA_SERVER = os.environ["KAFKA_SERVER"]

producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER])

class LocationServicer(location_pb2_grpc.LocationServiceServicer):
    def Create(self, request, context):
        print("Received a message!")

        request_value = {
            "person_id": int(request.person_id),
            "latitude": request.latitude,
            "longitude": request.longitude
        }
        print(f"Request: {request_value} ")
        
        encoded_data = json.dumps(request_value).encode('utf-8')
        print(f"Encoded Data: {encoded_data}")
        producer.send(TOPIC_NAME, encoded_data)
        producer.flush()
        print("Message sent to Kafka topic.")
        
        return location_pb2.LocationMessage(**request_value)


# Initialize gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_pb2_grpc.add_LocationServiceServicer_to_server(LocationServicer(), server)


print("Server starting on port 5005...")
server.add_insecure_port("[::]:5005")
server.start()
# Keep thread alive
server.wait_for_termination()
