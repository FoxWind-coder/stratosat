import serial
import time
import sys

def receive_file(port, baudrate, output_filepath):
    ser = serial.Serial(port, baudrate, timeout=1)
    ser.flush()

    # Сообщение о готовности к приему данных
    ser.write(b'READY\n')

    # Получение размера файла
    size_info = ser.readline().decode().strip()
    if size_info.startswith("SIZE:"):
        file_size = int(size_info.split(":")[1])
    else:
        raise ValueError("Invalid size information received")

    packet_size = 240  # Размер пакета данных (LoRa E32 имеет ограничение на пакет данных)
    num_packets = (file_size + packet_size - 1) // packet_size

    received_data = bytearray()
    
    for _ in range(num_packets):
        packet = ser.read(packet_size)
        received_data.extend(packet)

        # Отправка подтверждения
        ser.write(b'ACK\n')
        time.sleep(0.5)  # Задержка для обеспечения надежной передачи

    with open(output_filepath, 'wb') as file:
        file.write(received_data)

    ser.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python receiver.py <port> <baudrate> <output_filepath>")
        sys.exit(1)

    port = sys.argv[1]
    baudrate = int(sys.argv[2])
    output_filepath = sys.argv[3]

    receive_file(port, baudrate, output_filepath)
