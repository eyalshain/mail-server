import socket
import json
import base64
from RSA_class import decrypt, generate_keypair


def string_to_dict(input_str):
    new_string = json.loads(input_str)
    return new_string


def save_image(data_dict):
    try:
        if 'image' in data_dict:
            image_data = base64.b64decode(data_dict['image'])
            with open('received_image', 'wb') as img_file:
                img_file.write(image_data)
            print('Received image and saved it as received_image')

    except FileNotFoundError:
        print('Image was not found or path was incorrect.')
    except PermissionError:
        print('Permission denied to write this file')
    except IOError:
        print('Error: Something bad happened in the process... ')


def save_file(data_dict):
    try:
        if 'file' in data_dict:
            file_data = base64.b64decode(data_dict['file'])
            with open('received_file', 'wb') as file_f:
                file_f.write(file_data)
            print('Received file and saved it as received_file')

    except FileNotFoundError:
        print('File was not found or path was incorrect.')
    except PermissionError:
        print('Permission denied to write this file')
    except IOError:
        print('Error: Something bad happened in the process... ')


def handle_client(conn, addr):
    print(f'Connected by {addr}')
    print('')
    print('')
    data = b''
    while True:
        try:
            part = conn.recv(1024)
            if not part:
                break
            data += part
            if b'\n' in part:
                break  # Stop receiving when newline character is encountered
        except ConnectionResetError:
            print('Connection was reset unexpectedly')
            break

    if data:
        data = data.decode()
        data_dict = string_to_dict(data)

        print(f"Sender: {data_dict.get('sender')}")
        print(f"Receiver: {data_dict.get('receiver')}")
        print(f"Subject: {data_dict.get('subject')}")
        print('')
        print(f"Message:\n{data_dict.get('message')}")

        save_image(data_dict)
        save_file(data_dict)

    else:
        print('There is no data received')


if __name__ == "__main__":
    HOST = '127.0.0.1'
    PORT = 65432

    print("Server is listening for connections...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)
