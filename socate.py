import socket

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))  # استبدل بـ IP الخادم إذا لزم الأمر

    while True:
        command = input("Enter command (type 'exit' to quit): ")
        client_socket.send(command.encode())

        if command.lower() == 'exit':
            break

        output = client_socket.recv(1024).decode()
        print("Output:", output)

    client_socket.close()

if __name__ == '__main__':
    client_program()