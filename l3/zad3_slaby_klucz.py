import math
import sys
from collections import Counter

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"
SAMPLE = 4096

def decrypt_ecb(key, data):
    dec = Cipher(algorithms.AES(key), modes.ECB()).decryptor()
    return dec.update(data) + dec.finalize()


def entropy(data):
    n = len(data)
    h = 0.0
    for count in Counter(data).values():
        p = count / n
        h -= p * math.log2(p)
    return h


def main():
    path = "slaby_ecb.bin"
    out = "odszyfrowany_slaby_ecb.txt"
    with open(path, "rb") as f:
        ct = f.read()
    print(f"Kryptogram: {len(ct)} B")

    sample = ct[:SAMPLE]
    ranking = []
    for ch in ALPHABET:
        key = (ch * 16).encode("ascii")
        ranking.append((entropy(decrypt_ecb(key, sample)), ch))
    ranking.sort()

    print("Ranking wszystkich kandydatow:")
    for i, (h, ch) in enumerate(ranking, 1):
        print(f"  {i:2d}. '{ch}'  H = {h:.4f}")
    print("Top 5:")
    for h, ch in ranking[:5]:
        print(f"  '{ch}'  H = {h:.4f}")

    best = ranking[0][1]
    key = (best * 16).encode("ascii")
    padded = decrypt_ecb(key, ct)
    unpadder = padding.PKCS7(128).unpadder()
    plain = unpadder.update(padded) + unpadder.finalize()
    text = plain.decode("utf-8")
    printable = sum(c.isprintable() or c in "\n\r\t" for c in text) / len(text)
    print(f"Odzyskany znak klucza: '{best}' (klucz {key.decode()})")
    print(f"Tekst jawny: {len(plain)} B, dopelnienie {len(padded) - len(plain)} B, "
          f"znaki drukowalne: {printable:.2%}")
    print("Pierwszy wiersz:", text.splitlines()[0])
    with open(out, "wb") as f:
        f.write(plain)
    print("Zapisano:", out)


if __name__ == "__main__":
    main()
