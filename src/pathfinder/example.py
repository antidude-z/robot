import socket
import time

host = "192.168.1.1"
port = 2001

s = None

def connect():
    global s
    # Создаем сокет
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Устанавливаем соединение
    s.connect((host, port))

    s.sendall(b'\xff\xef\xef\xee\xff')


def close():
    global s
    s.close()

def convert(speed, d):
    # numbers = [255, 2, d, speed, 255]
    # # processed = [f"{hex(i)}"for i in numbers]
    # escaped = "".join(fr"\x{b:02x}" for b in numbers)
    # command = escaped.encode('latin1')
    # return command
    
    # return bytearray(x).decode('all-escapes').encode()

    m = {
        8: b'\xff\x02\x01\x35\xff',
        16: b'\xff\x02\x01\x5a\xff',
        # 24: b'\xff\x02\x02\x\xff',
        11: b'\xff\x02\x01\x49\xff',
        # 23: b'\xff\x02\x02\x40\xff'
    }

    n = {
        8: b'\xff\x02\x02\x35\xff',
        16: b'\xff\x02\x02\x5a\xff',
        # 24: b'\xff\x02\x02\x\xff',
        11: b'\xff\x02\x02\x49\xff',
        # 23: b'\xff\x02\x02\x40\xff'
    }

    if d == 1:
        return m[speed]
    elif d == 2:
        return n[speed]

def send_command(command):
    try:
        # Создаем сокет
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(f"Соединение с {host}:{port}")

        # Устанавливаем соединение
        s.connect((host, port))
        print(f"Отправка команды: {command}")

        # Отправляем команду
        s.sendall(command)

        # Добавляем небольшой задержку между отправками команд
        time.sleep(0.01)

        return True
    except socket.error as e:
        print(f"Ошибка сокета: {e}")
        return False
    finally:
        # Закрываем соединение
        s.close()
        print("Соединение закрыто")

def move(speed):
    send_command(convert(speed, 1))
    send_command(convert(speed, 2))

    send_command(b'\xff\x00\x01\x00\xff')

def turn(direction):
        # send_command(b'\xff\x00\x02\x14\xff')  # back

        if direction == 'left':
            send_command(b'\xff\x02\x01\x35\xff')
            send_command(b'\xff\x02\x02\x35\xff')
            send_command(b'\xff\x00\x03\x00\xff')
        elif direction == 'right':
            send_command(b'\xff\x02\x01\x35\xff')
            send_command(b'\xff\x02\x02\x35\xff')
            send_command(b'\xff\x00\x04\x00\xff')

if __name__ == '__main__':
    # Первая команда
    while True:
        s = input().split(' ')
        if s[0] == 'forward':
            x = hex(int(s[1]))[2:].zfill(2)

            # right and left same velocity
            exec("send_command(b'\\xff\\x02\\x02\\x{x}\\xff')")
            exec("send_command(b'\\xff\\x02\\x01\\x{x}\\xff')")

            send_command(b'\xff\x00\x01\x00\xff')
        if s[0] == 'back':
            x = hex(int(s[1]))[2:].zfill(2)

            # right and left same velocity
            exec(f"send_command(b'\\xff\\x02\\x02\\x{x}\\xff')")
            exec(f"send_command(b'\\xff\\x02\\x01\\x{x}\\xff')")

            send_command(b'\xff\x00\x02\x00\xff')
        elif s[0] == 'turn':
            direction = s[1]
            x = hex(int(s[2]))[2:].zfill(2)
            if direction == 'left':
                exec(f"send_command(b'\\xff\\x02\\x02\\x{x}\\xff')")
                send_command(b'\xff\x02\x01\x00\xff')
            elif direction == 'right':
                exec(f"send_command(b'\\xff\\x02\\x01\\x{x}\\xff')")
                send_command(b'\xff\x02\x02\x00\xff')
            
            send_command(b'\xff\x00\x01\x00\xff')  # forward

        # данные показатели возможно пропорциональны заряду батареи.
        # 90 grad - 65%
        # 60 grad - 53%
        # 45 grad - 41%
        # 30 grad - 33%
        # 15 grad - 24%

        # поворот на 45 - 45 скорость
        # поворот на 90 - 75 скорость

        # Робот 628 назад - это вперёд, а вперёд - это назад

        # exec(f"command = b'\\xff\\x02\\x02\\x{x}\\xff'")
        # send_command(command)
        # send_command(b'\xff\x02\x01\x00\xff')
        # send_command(b'\xff\x00\x02\x00\xff')
        # print('Команда на установку цвета отправлена: ', result)

