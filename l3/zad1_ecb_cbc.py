import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK = 16

def aes(key, mode, data, encrypt):
    cipher = Cipher(algorithms.AES(key), mode)
    ctx = cipher.encryptor() if encrypt else cipher.decryptor()
    return ctx.update(data) + ctx.finalize()


def blocks(data):
    return [data[i:i + BLOCK] for i in range(0, len(data), BLOCK)]


def equal_blocks(bl):
    pairs = []
    for i in range(len(bl)):
        for j in range(i + 1, len(bl)):
            if bl[i] == bl[j]:
                pairs.append((i + 1, j + 1))
    return pairs


def show(name, ct):
    print(f"--- {name} ---")
    bl = blocks(ct)
    for n, b in enumerate(bl, 1):
        print(f"  blok {n}: {b.hex()}")
    pairs = equal_blocks(bl)
    if pairs:
        print("  rowne bloki:", ", ".join(f"{a}={b}" for a, b in pairs))
    else:
        print("  rowne bloki: brak")


def main():
    plaintext = b"0123456789ABCDEF" * 4
    key = bytes.fromhex("000102030405060708090a0b0c0d0e0f")
    iv = os.urandom(16)

    print("Tekst jawny (64 B):", plaintext.decode())
    print("Klucz:", key.hex())
    print("IV CBC:", iv.hex())

    ct_ecb = aes(key, modes.ECB(), plaintext, True)
    ct_cbc = aes(key, modes.CBC(iv), plaintext, True)
    show("ECB", ct_ecb)
    show("CBC", ct_cbc)

    pt_ecb = aes(key, modes.ECB(), ct_ecb, False)
    pt_cbc = aes(key, modes.CBC(iv), ct_cbc, False)
    print("Odszyfrowanie ECB == wejscie:", pt_ecb == plaintext)
    print("Odszyfrowanie CBC == wejscie:", pt_cbc == plaintext)


if __name__ == "__main__":
    main()
