import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc

class DemoService(service_pb2_grpc.DemoServiceServicer):
    def UnaryCall(self, request, context):
        print(f"UnaryCall received: {request.message}")
        return service_pb2.ResponseMessage(message="Hello from server (Unary)")

    def ServerStreamingCall(self, request, context):
        print(f"ServerStreamingCall received: {request.message}")
        for i in range(3):
            yield service_pb2.ResponseMessage(message=f"Stream {i+1} from server")

    def ClientStreamingCall(self, request_iterator, context):
        messages = []
        for req in request_iterator:
            print(f"ClientStreamingCall received: {req.message}")
            messages.append(req.message)
        return service_pb2.ResponseMessage(message=f"Received {len(messages)} messages")

    def BidiStreamingCall(self, request_iterator, context):
        for req in request_iterator:
            print(f"BidiStreamingCall received: {req.message}")
            yield service_pb2.ResponseMessage(message=f"Echo: {req.message}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_DemoServiceServicer_to_server(DemoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
