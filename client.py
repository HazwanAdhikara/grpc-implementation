import grpc
import service_pb2
import service_pb2_grpc

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = service_pb2_grpc.DemoServiceStub(channel)

    # Unary RPC
    print("\n--- Unary ---")
    response = stub.UnaryCall(service_pb2.RequestMessage(message="Hello Server"))
    print(f"Response: {response.message}")

    # Server Streaming RPC
    print("\n--- Server Streaming ---")
    responses = stub.ServerStreamingCall(service_pb2.RequestMessage(message="Stream to me"))
    for res in responses:
        print(f"Streamed: {res.message}")

    # Client Streaming RPC
    print("\n--- Client Streaming ---")
    def client_stream():
        for i in range(3):
            yield service_pb2.RequestMessage(message=f"Message {i+1} from client")

    response = stub.ClientStreamingCall(client_stream())
    print(f"Response: {response.message}")

    # Bi-directional Streaming RPC
    print("\n--- Bi-directional Streaming ---")
    def bidi_stream():
        for i in range(3):
            yield service_pb2.RequestMessage(message=f"Bidi message {i+1}")

    responses = stub.BidiStreamingCall(bidi_stream())
    for res in responses:
        print(f"Echoed: {res.message}")

if __name__ == '__main__':
    run()