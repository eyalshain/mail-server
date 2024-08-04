import json
import datetime
import socket
import base64
from RSA_class import encrypt, generate_keypair


def another_message():
    x = input('Do you want to send another message (yes / no): ')
    while x not in ['yes', 'no']:
        x = input('Do you want to send another message (yes / no): ')
    return x


def encode_image(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            encoded_image = base64.b64encode(img_file.read())
        return encoded_image
    except FileNotFoundError:
        print('Image file was not found or path is incorrect.')


def encode_file(file_path):
    try:
        with open(file_path, 'rb') as file_file:
            file_content = file_file.read()
        encoded_file = base64.b64encode(file_content)
        return encoded_file
    except FileNotFoundError:
        print('File was not found or file path was incorrect.')


def dict_to_string(input_dict):
    json_string = json.dumps(input_dict)
    return json_string


def create_message():
    x = datetime.datetime.now()
    date_str = x.strftime("%Y-%m-%d %H:%M")

    print('Enter the information needed: ')
    sender = input("sender's name: ")
    receiver = input("receiver's name: ")
    subject = input("subject: ")
    message = input("message: ")

    mail_message = {'sender': sender,
                    'receiver': receiver,
                    'subject': subject,
                    'message': message,
                    'date': date_str}

    attach_image = input('Do you want to attach an image? (yes / no): ')

    while attach_image.lower() not in ['yes', 'no']:
        print('input must be yes / no! ')
        attach_image = input('Do you want to attach an image? (yes / no): ')

    if attach_image.lower() == 'yes':
        image_path = input('Enter the path to the image file: ')
        try:
            encoded_image = encode_image(image_path)
            mail_message['image'] = encoded_image
        except NameError:
            print('Image path was undefined')

    attach_file = input('Do you want to attach a file? (yes / no): ')

    while attach_file.lower() not in ['yes', 'no']:
        print('input must be yes / no! ')
        attach_file = input('Do you want to attach a file? (yes / no): ')

    if attach_file.lower() == 'yes':
        file_path = input('Enter the path to the file: ')
        try:
            encoded_file = encode_file(file_path)
            mail_message['file'] = encoded_file
        except NameError:
            print('File path was undefined')

    return dict_to_string(mail_message)


def send_message(message):
    HOST = '127.0.0.1'
    PORT = 65432
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            s.sendall(message.encode())
        print('Message sent')

    except ConnectionRefusedError:
        print('The server is not available')

    except socket.error as s:
        print(f'Socket error: {s}')


if __name__ == '__main__':
    mail_message = create_message()
    send_message(mail_message)
    print('')

    while another_message().lower() == 'yes':
        mail_message = create_message()
        send_message(mail_message)
        print('')

    if another_message().lower() == 'no':
        print('Goodbye!')
