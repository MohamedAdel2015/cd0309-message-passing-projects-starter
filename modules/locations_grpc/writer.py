import grpc
import location_pb2
import location_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30004")
stub = location_pb2_grpc.LocationServiceStub(channel)

location = location_pb2.LocationMessage(
    person_id=5,
    longitude=-98.782788,
    latitude=964.31798,
    creation_time='2020-09-30',
)
response = stub.Create(location)

location = location_pb2.LocationMessage(
    person_id=6,
    longitude=-98.782788,
    latitude=964.31798,
    creation_time='2020-07-30',
)


response = stub.Create(location)