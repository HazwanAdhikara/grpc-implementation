import grpc
from concurrent import futures
import time
import service_pb2
import service_pb2_grpc

class DemoService(service_pb2_grpc.DemoServiceServicer):
    def UnaryCall(self, request, context):
        print(f"UnaryCall received: {request.message}")
        # Dynamic response based on client input
        return service_pb2.ResponseMessage(message=f"Server received: '{request.message}'")

    def ServerStreamingCall(self, request, context):
        print(f"ServerStreamingCall received: {request.message}")
        # Generate multiple responses based on client input
        for i in range(3):
            yield service_pb2.ResponseMessage(message=f"Stream response {i+1} for message: '{request.message}'")
            time.sleep(0.5)  # Simulate processing time

    def ClientStreamingCall(self, request_iterator, context):
        messages = []
        for req in request_iterator:
            print(f"ClientStreamingCall received: {req.message}")
            messages.append(req.message)
        
        # Process the received messages
        message_count = len(messages)
        message_summary = ', '.join([f"'{msg}'" for msg in messages[:3]])
        if message_count > 3:
            message_summary += f", and {message_count - 3} more"
            
        return service_pb2.ResponseMessage(
            message=f"Processed {message_count} messages: {message_summary}"
        )

    def BidiStreamingCall(self, request_iterator, context):
        for req in request_iterator:
            print(f"BidiStreamingCall received: {req.message}")
            # Process each message and respond immediately
            response_message = self._process_bidirectional_message(req.message)
            yield service_pb2.ResponseMessage(message=response_message)
    
    def _process_bidirectional_message(self, message):
        # Add some processing logic to make responses more interactive
        if message.lower().startswith("hello"):
            return f"Hi there! You said: '{message}'"
        elif message.lower().startswith("how"):
            return f"I'm a gRPC server responding to: '{message}'"
        elif "?" in message:
            return f"You asked: '{message}'. I'm just a simple echo server."
        else:
            return f"Echo: '{message}'"

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_DemoServiceServicer_to_server(DemoService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started at port 50051")
    print("Waiting for client requests...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
