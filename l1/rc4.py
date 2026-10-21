import math
import time
import itertools
from collections import Counter

def rc4(data, key):
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    i = 0
    j = 0
    wynik = bytearray()
    for b in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        wynik.append(b ^ K)
    return bytes(wynik)

def entropia(data):
    N = len(data)
    if N == 0:
        return 0.0
    H = 0.0
    for n in Counter(data).values():
        p = n / N
        H -= p * math.log2(p)
    return H

test = b"Attack at dawn"
print("Test podwojnego RC4:", rc4(rc4(test, b"abc"), b"abc") == test)
print("Test wektora:", rc4(b"Plaintext", b"Key").hex() == "bbf316e8d940af0ad3")

with open("rc4.bin", "rb") as f:
    szyfr = f.read()
print("Dlugosc:", len(szyfr), repr(szyfr[:50]))

alfabet = b"abcdefghijklmnopqrstuvwxyz"
kandydaci = []
proby = 0
t0 = time.perf_counter()
for combo in itertools.product(alfabet, repeat=3):
    klucz = bytes(combo)
    proby += 1
    tekst = rc4(szyfr[:512], klucz)
    kandydaci.append((entropia(tekst), klucz))
czas = time.perf_counter() - t0

kandydaci.sort()
print("Liczba prob:", proby)
print(f"Czas: {czas:.2f} s")
print("Top 5:")
for H, klucz in kandydaci[:5]:
    print(f"{klucz.decode()} H={H:.4f} {repr(rc4(szyfr[:50], klucz))}")

klucz = kandydaci[0][1]
jawny = rc4(szyfr, klucz)
with open("rc4.txt", "wb") as f:
    f.write(jawny)

print("Wybrany klucz:", klucz.decode())
print("Poczatek:", repr(jawny[:100]))
print("Ponowne szyfrowanie == kryptogram:", rc4(jawny, klucz) == szyfr)
print(f"Entropia kryptogramu: {entropia(szyfr):.4f}")
print(f"Entropia odszyfrowania: {entropia(jawny):.4f}")
