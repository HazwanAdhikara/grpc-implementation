import grpc
import service_pb2
import service_pb2_grpc
import time

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = service_pb2_grpc.DemoServiceStub(channel)

    while True:
        print("\nChoose an RPC type:")
        print("1. Unary RPC")
        print("2. Server Streaming RPC")
        print("3. Client Streaming RPC")
        print("4. Bidirectional Streaming RPC")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '1':
            # Unary RPC
            message = input("Enter message to send: ")
            response = stub.UnaryCall(service_pb2.RequestMessage(message=message))
            print(f"Server Response: {response.message}")
            
        elif choice == '2':
            # Server Streaming RPC
            message = input("Enter message to send: ")
            responses = stub.ServerStreamingCall(service_pb2.RequestMessage(message=message))
            print("Server Responses:")
            for res in responses:
                print(f"-> {res.message}")
                
        elif choice == '3':
            # Client Streaming RPC
            messages = []
            print("Enter messages to send (type 'done' when finished):")
            while True:
                message = input("> ")
                if message.lower() == 'done':
                    break
                messages.append(message)
                
            def client_stream():
                for msg in messages:
                    yield service_pb2.RequestMessage(message=msg)
                    
            response = stub.ClientStreamingCall(client_stream())
            print(f"Server Response: {response.message}")
            
        elif choice == '4':
            # Bidirectional Streaming RPC
            print("Enter messages to send (type 'done' when finished):")
            
            def bidi_stream():
                while True:
                    message = input("> ")
                    if message.lower() == 'done':
                        break
                    yield service_pb2.RequestMessage(message=message)
                    
            responses = stub.BidiStreamingCall(bidi_stream())
            print("Server Responses:")
            for res in responses:
                print(f"-> {res.message}")
                
        elif choice == '5':
            print("Exiting...")
            break
            
        else:
            print("Invalid choice. Please try again.")
        
        time.sleep(1)

if __name__ == '__main__':
    run()