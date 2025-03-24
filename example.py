import socket
import time

host = "192.168.1.1"
port = 2001


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
        time.sleep(1)

        return True
    except socket.error as e:
        print(f"Ошибка сокета: {e}")
        return False
    finally:
        # Закрываем соединение
        s.close()
        print("Соединение закрыто")


# Первая команда
while True:
    x = hex(int(input()))[2:]

    exec(f"command = b'\\xff\\x02\\x01\\x{x}\\xff'")  # Пример отправки команды  # 50 - поворот на 90
    result = send_command(command)
    send_command(b'\xff\x02\x02\x00\xff')
    send_command(b'\xff\x00\x01\x00\xff')
    print('Команда на установку цвета отправлена: ', result)
