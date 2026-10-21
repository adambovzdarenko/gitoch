
def vig_encrypt(data, key):
    if len(key) == 0:
        raise ValueError("Klucz nie moze byc pusty")
    wynik = bytearray()
    for i, b in enumerate(data):
        k = key[i % len(key)]
        wynik.append((b + k) % 256)
    return bytes(wynik)

def vig_decrypt(data, key):
    if len(key) == 0:
        raise ValueError("Klucz nie moze byc pusty")
    return bytes((b - key[i % len(key)]) % 256 for i, b in enumerate(data))

with open("tekst_pl.txt", "rb") as f:
    jawny = f.read()
print("Zrodlo:", len(jawny), "bajtow", repr(jawny[:50]))

szyfr = vig_encrypt(jawny, b"ZAMEK")
with open("vigenere.bin", "wb") as f:
    f.write(szyfr)

with open("vigenere.bin", "rb") as f:
    odczyt = f.read()
odszyfr = vig_decrypt(odczyt, b"ZAMEK")
print("Zgodnosc bajt po bajcie:", odszyfr == jawny)

print("Puste dane:", vig_decrypt(vig_encrypt(b"", b"ZAMEK"), b"ZAMEK") == b"")
test = bytes([0, 255, 0, 255, 128, 1, 254])
print("Bajty 0 i 255:", vig_decrypt(vig_encrypt(test, b"ZAMEK"), b"ZAMEK") == test)

tekst = b"BRAMABRAMABRAMA"
for klucz in (b"SZYFR", b"KOD"):
    c = vig_encrypt(tekst, klucz)
    fragmenty = [c[i:i + 5].hex() for i in range(0, len(c), 5)]
    print(klucz.decode(), fragmenty)
