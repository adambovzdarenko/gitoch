Zadanie 1.
Przesunięcie k = 233
Wybrałem k = 233, bo tylko ono daje sensowny angielski tekst.

Wyjaśnij, dlaczego sama entropia histogramu wartości
0–255 nie rozstrzygnie, które przesunięcie jest poprawne:

Dlatego że Cezar tylko zamienia wartości bajtów, więc wszystkie 256 wyników mają taki sam histogram, tylko przesunięty, czyli taką samą entropię.

Zadanie 2.
Testy: zgodność bajt po bajcie - True, puste dane - True, bajty 0 i 255 - True

SZYFR: ['95ac9a9393', '95ac9a9393', '95ac9a9393']
KOD: ['8da1859890', '869d90918c', '91968c9c85']

W 2–3 zdaniach wyjaśnij, dlaczego w jednym przypadku powtarzają się całe pięciobajtowe fragmenty
kryptogramu, a w drugim nie. Odnieś to do położenia powtarzanego tekstu względem klucza i informacji
widocznej dla atakującego:

Dlatego że długość BRAMA i klucza SZYFR jest taka sama, więc BRAMA zawsze trafia na ten sam fragment klucza.
Przy KOD każde BRAMA zaczyna się w innym miejscu klucza, więc fragmenty są różne.
Atakujący widzi powtórzenie co 5 bajtów, więc wie, że długość klucza dzieli 5.

Zadanie 3.
Program sprawdził wszystkie 17576 kluczy (26^3) w 5.60 s i automatycznie wybrał klucz tat, bo miał najniższą entropię.
Pięciu najlepszych kandydatów: tat (H=4.3910), neg (H=7.4304), mcn (H=7.4512), oxo (H=7.4536), tnx (H=7.4592).
Entropia całego kryptogramu wynosi 7.9271, a całego odszyfrowania 4.3259.
Podwójne RC4 z tym samym kluczem i ponowne szyfrowanie dały to samo co wejście (True), a odszyfrowany tekst jest sensownym angielskim tekstem.

W 2–3 zdaniach wyjaśnij, dlaczego ponowne szyfrowanie może odtworzyć kryptogram również dla błędnego klucza
i kiedy ranking entropii mógłby zawieść:

Dlatego że RC4 to XOR, a (C ^ K) ^ K = C dla każdego klucza, więc to sprawdza tylko kod, a nie klucz.
Ranking entropii mógłby zawieść, gdy tekst jest za krótki albo nie jest zwykłym tekstem (np. dane skompresowane).