
def caesar_decrypt(data, k):
    return bytes((b - k) % 256 for b in data)

def ocena(tekst):

    if len(tekst) == 0:
        return 0.0
    dobre = sum(1 for b in tekst if 32 <= b <= 126 or b in (9, 10, 13))
    return dobre / len(tekst)

with open("cezar.bin", "rb") as f:
    szyfr = f.read()
print("Dlugosc:", len(szyfr), "poczatek:", repr(szyfr[:50]))

kandydaci = []
for k in range(256):
    tekst = caesar_decrypt(szyfr, k)
    kandydaci.append((ocena(tekst), k))

kandydaci.sort(key=lambda para: (-para[0], para[1]))

print("Top 5:")
for wynik, k in kandydaci[:5]:
    print(f"k={k:3d} ocena={wynik:.4f} {repr(caesar_decrypt(szyfr, k)[:50])}")

k = int(input("Wybierz przesuniecie k: "))
with open("cezar.txt", "wb") as f:
    f.write(caesar_decrypt(szyfr, k))
print("Zapisano cezar.txt dla k =", k)
