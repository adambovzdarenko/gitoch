import os
import sys

from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

ITERATIONS = 200_000
KEY_LEN = 32
SALT_LEN = 16
IV_LEN = 16
PASSWORD = "HasloHasloLubieMaslo"


def derive_key(password, salt):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=KEY_LEN,
                     salt=salt, iterations=ITERATIONS)
    return kdf.derive(password.encode("utf-8"))


def encrypt(password, data):
    salt = os.urandom(SALT_LEN)
    iv = os.urandom(IV_LEN)
    key = derive_key(password, salt)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    enc = Cipher(algorithms.AES(key), modes.CBC(iv)).encryptor()
    return salt, iv, enc.update(padded) + enc.finalize()


def decrypt(password, salt, iv, ct):
    key = derive_key(password, salt)
    dec = Cipher(algorithms.AES(key), modes.CBC(iv)).decryptor()
    padded = dec.update(ct) + dec.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(padded) + unpadder.finalize()


def expected_len(n):
    return (n // 16 + 1) * 16


def run_test(name, data):
    salt, iv, ct = encrypt(PASSWORD, data)
    back = decrypt(PASSWORD, salt, iv, ct)
    ok_eq = back == data
    ok_len = len(ct) == expected_len(len(data))
    status = "OK" if ok_eq and ok_len else "BLAD"
    print(f"[{status}] {name}: dane {len(data)} B -> kryptogram {len(ct)} B "
          f"(oczekiwano {expected_len(len(data))} B), rownosc bajtow: {ok_eq}")
    return ok_eq and ok_len


def main():
    path = "wiadomosc.txt"
    with open(path, "rb") as f:
        msg = f.read()

    print(f"Haslo testowe: {PASSWORD!r}")
    print(f"PBKDF2-HMAC-SHA256, {ITERATIONS} iteracji, klucz {KEY_LEN} B, sol {SALT_LEN} B, IV {IV_LEN} B")
    print("Testy")
    results = [
        run_test("puste dane", b""),
        run_test("16 B '0123456789ABCDEF'", b"0123456789ABCDEF"),
        run_test(path, msg),
    ]
    print("Wszystkie testy zaliczone:", all(results))

    print("Dwukrotne szyfrowanie wiadomosci tym samym haslem")
    s1, iv1, c1 = encrypt(PASSWORD, msg)
    s2, iv2, c2 = encrypt(PASSWORD, msg)
    print(f"Szyfrowanie 1: sol={s1.hex()} IV={iv1.hex()}")
    print(f"  kryptogram[:32]={c1[:32].hex()}...")
    print(f"Szyfrowanie 2: sol={s2.hex()} IV={iv2.hex()}")
    print(f"  kryptogram[:32]={c2[:32].hex()}...")
    print("Klucze rowne:", derive_key(PASSWORD, s1) == derive_key(PASSWORD, s2))
    print("Kryptogramy rowne:", c1 == c2)
    same = sum(a == b for a, b in zip(c1, c2))
    print(f"Zgodnych bajtow na tych samych pozycjach: {same}/{len(c1)}")
    print("Oba odszyfrowuja sie poprawnie:",
          decrypt(PASSWORD, s1, iv1, c1) == msg and decrypt(PASSWORD, s2, iv2, c2) == msg)


if __name__ == "__main__":
    main()
