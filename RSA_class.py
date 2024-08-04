import math
from sympy import isprime
import random


def is_prime(number):
    return isprime(number)


def generate_prime(bits):
    while True:
        num = random.getrandbits(bits)
        if is_prime(num):
            return num


def mod_inverse(public_key, totient):
    t, new_t = 0, 1
    r, new_r = totient, public_key

    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r

    if r > 1:
        raise ValueError("The modular inverse does not exist")

    if t < 0:
        t += totient

    return t


def encrypt(message, public_key):
    e, n = public_key
    encrypted_message = ''.join([pow(ord(char), e, n) for char in message])
    return encrypted_message


def decrypt(cipher_text, private_key):
    d, n = private_key
    decrypted_message = ''.join([chr(pow(char, d, n)) for char in cipher_text])
    return decrypted_message


def generate_keypair(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)

    while p == q:
        q = generate_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    e = random.randint(3, phi - 1)
    while math.gcd(e, phi) != 1:
        e = random.randint(3, phi - 1)

    d = mod_inverse(e, phi)

    return (e, n), (d, n)


