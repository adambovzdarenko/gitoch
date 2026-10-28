#!/usr/bin/env python3

import hashlib
import hmac
import os
import secrets
import sys
import time

BASE = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.abspath(__file__))


#Zadanie 1
def sha256_pliku(sciezka):
    with open(sciezka, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def sha256_pliku_kawalkami(sciezka, rozmiar=4096):
    h = hashlib.sha256()
    with open(sciezka, "rb") as f:
        while blok := f.read(rozmiar):
            h.update(blok)
    return h.hexdigest()


def sprawdz_sumy(plik_sum):
    katalog = os.path.dirname(os.path.abspath(plik_sum))
    wyniki = []
    with open(plik_sum, "rb") as f:
        for wiersz in f.read().decode("utf-8").splitlines():
            if not wiersz.strip():
                continue
            skrot, sciezka = wiersz[:64].lower(), wiersz[66:]
            pelna = os.path.join(katalog, sciezka)
            try:
                status = "OK" if sha256_pliku(pelna) == skrot else "BŁĄD"
            except FileNotFoundError:
                status = "BRAK"
            wyniki.append((sciezka, status))
    return wyniki


def rozne_bity(a: bytes, b: bytes):
    return bin(int.from_bytes(a, "big") ^ int.from_bytes(b, "big")).count("1")


def zadanie1():
    print("=== Zadanie 1 — sumy kontrolne ===")
    for sciezka, status in sprawdz_sumy(os.path.join(BASE, "SHA256SUMS.txt")):
        print(f"{sciezka}: {status}")
    h1 = hashlib.sha256("Ala ma kota.".encode("ascii")).digest()
    h2 = hashlib.sha256("Ola ma kota.".encode("ascii")).digest()
    print(f"SHA-256('Ala ma kota.') = {h1.hex()}")
    print(f"SHA-256('Ola ma kota.') = {h2.hex()}")
    print(f"Różniące się bity: {rozne_bity(h1, h2)} / 256")

    # dodatkowo: liczenie w kawałkach po 4096 B
    dane = os.path.join(BASE, "dokumenty", "dane.bin")
    if os.path.exists(dane):
        a, b = sha256_pliku(dane), sha256_pliku_kawalkami(dane)
        print(f"[dod.] dane.bin naraz    = {a}")
        print(f"[dod.] dane.bin kawałkami= {b}  zgodne: {a == b}")
    print()


#Zadanie 2
ITERACJE = 600000


def wczytaj_baze(sciezka):
    baza = {}
    with open(sciezka, "rb") as f:
        for wiersz in f.read().decode("utf-8").splitlines():
            if not wiersz.strip():
                continue
            login, it, sol, skrot = wiersz.split(":")
            baza[login] = (int(it), bytes.fromhex(sol), bytes.fromhex(skrot))
    return baza


def pbkdf2(haslo, sol, iteracje):
    return hashlib.pbkdf2_hmac("sha256", haslo.encode("utf-8"), sol, iteracje, dklen=32)


def weryfikuj(baza, login, haslo):
    rekord = baza.get(login)
    if rekord is None:
        return False
    it, sol, skrot = rekord
    return hmac.compare_digest(pbkdf2(haslo, sol, it), skrot)


def dodaj(baza, login, haslo):
    sol = secrets.token_bytes(16)
    skrot = pbkdf2(haslo, sol, ITERACJE)
    baza[login] = (ITERACJE, sol, skrot)
    return f"{login}:{ITERACJE}:{sol.hex()}:{skrot.hex()}"


def zadanie2(pomiary=True):
    print("=== Zadanie 2 — przechowywanie haseł ===")
    baza = wczytaj_baze(os.path.join(BASE, "hasla.txt"))
    testy = [("anna", "Kasztan-2026"), ("anna", "kasztan-2026"),
             ("piotr", "Żółw na łące"), ("kasia", "Kasztan-2026")]
    for login, haslo in testy:
        print(f"weryfikuj({login!r}, {haslo!r}) -> {weryfikuj(baza, login, haslo)}")

    haslo = "TestoweHaslo-2026"
    dodaj(baza, "test1", haslo)
    dodaj(baza, "test2", haslo)
    _, s1, k1 = baza["test1"]
    _, s2, k2 = baza["test2"]
    print(f"test1: sól {s1.hex()[:8]}…, skrót {k1.hex()[:8]}…")
    print(f"test2: sól {s2.hex()[:8]}…, skrót {k2.hex()[:8]}…")
    print(f"Sole równe: {s1 == s2}; skróty równe: {k1 == k2}")
    print(f"weryfikuj(test1) -> {weryfikuj(baza, 'test1', haslo)}; "
          f"weryfikuj(test2) -> {weryfikuj(baza, 'test2', haslo)}")
    print()


#Zadanie 3
N_WIERSZY = 13
N_WARIANTOW = 1 << N_WIERSZY


def wariant(wiersze, v):
    return b"".join(w + b" \n" if (v >> i) & 1 else w + b"\n" for i, w in enumerate(wiersze))


def h24(dane):
    return hashlib.sha256(dane).digest()[:3]


def wiersze_pliku(sciezka):
    with open(sciezka, "rb") as f:
        dane = f.read()
    wiersze = dane.split(b"\n")
    assert wiersze[-1] == b"" and len(wiersze) == N_WIERSZY + 1
    return wiersze[:-1]


def zadanie3():
    print("=== Zadanie 3 — kolizje i paradoks urodzinowy ===")
    org = wiersze_pliku(os.path.join(BASE, "oryginal.txt"))
    zm = wiersze_pliku(os.path.join(BASE, "zmieniony.txt"))

    slownik = {}
    wszystkie = {}
    for v in range(N_WARIANTOW):
        h = h24(wariant(org, v))
        slownik.setdefault(h, v)
        wszystkie.setdefault(h, []).append(v)
    h0 = h24(wariant(org, 0))
    print(f"h24(oryginał, v=0) = {h0.hex()}; różnych h24 oryginału: {len(slownik)}")

    para = None
    zgodne_z_v0 = 0
    liczba_par = 0
    for v in range(N_WARIANTOW):
        h = h24(wariant(zm, v))
        if para is None and h in slownik:
            para = (slownik[h], v, h)
        if h == h0:
            zgodne_z_v0 += 1
        liczba_par += len(wszystkie.get(h, ()))

    if para:
        vo, vz, h = para
        print(f"Znaleziona para: v_oryginał = {vo}, v_zmieniony = {vz}, h24 = {h.hex()}")
        assert h24(wariant(org, vo)) == h24(wariant(zm, vz))
    else:
        print("Nie znaleziono pary")
    print(f"Warianty zmienionego z h24 równym h24 oryginału (v=0): {zgodne_z_v0}")
    print()


if __name__ == "__main__":
    zadanie1()
    zadanie2()
    zadanie3()
