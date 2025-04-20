# r33
# Leinonen Topi

# Salakirjoitusmenetelmä - Harjoitustyö

Tämä projekti on toteutettu osana ohjelmoinnin perusteiden kurssia. Projekti sisältää erilaisia salakirjoitusmenetelmiä, kuten Caesar-salauksen, AES-salauksen ja Vigenère-salauksen. Ohjelma mahdollistaa tekstin salaamisen ja purkamisen käyttäjän valitsemalla menetelmällä.

## Sisältö

- **`main.py`**: Ohjelman päälogiikka, joka hallitsee käyttäjän valinnat, salauksen ja purkamisen.
- **`salaukset.py`**: Sisältää salausmenetelmien toteutukset (Caesar, AES, Vigenère).
- **`testaus.py`**: Testimoduuli, joka varmistaa salausmenetelmien toimivuuden.
- **`testi_salaus_teksti.txt`**: Esimerkkitiedosto, jota voidaan käyttää ohjelman kanssa.

---

## Käyttöohjeet

### 1. Ohjelman suorittaminen
Suorita ohjelma `main.py` tiedostosta. Ohjelma kysyy käyttäjältä seuraavat tiedot:
1. Valitse salausmenetelmä:
   - **1**: Caesar-salaus
   - **2**: AES-salaus
   - **3**: Vigenère-salaus
2. Valitse syöttötapa:
   - **1**: Kirjoita teksti itse
   - **2**: Lue teksti tiedostosta
3. Valitse toiminto:
   - **1**: Salaa teksti
   - **2**: Pura teksti

Ohjelma näyttää tuloksen ja tarjoaa mahdollisuuden tallentaa sen tiedostoon.

### 2. Testaus
Voit testata ohjelman toimivuutta suorittamalla `testaus.py` tiedoston. Testit tarkistavat kaikkien salausmenetelmien salauksen ja purkamisen oikeellisuuden.

Suorita testit komennolla:
```bash
python testaus.py
```

---

## Tiedostojen kuvaus

### `main.py`
Ohjelman pääfunktio, joka hallitsee käyttäjän valinnat ja suorittaa salaus- tai purkuprosessin. Tukee seuraavia salausmenetelmiä:
- **Caesar-salaus**: Yksinkertainen siirtosalaus, jossa kirjaimia siirretään aakkosissa tietty määrä.
- **AES-salaus**: Vahva lohkoalgoritmi, joka käyttää CBC-tilaa.
- **Vigenère-salaus**: Polyalfabeettinen siirtosalaus, jossa käytetään avainsanaa.

### `salaukset.py`
Sisältää salausmenetelmien toteutukset:
- **CaesarSalaus**: Toteuttaa Caesar-salauksen ja purun.
- **AESSalaus**: Toteuttaa AES-salauksen ja purun. Tukee hex-muotoista tulostusta.
- **VigenereSalaus**: Toteuttaa Vigenère-salauksen ja purun.

### `testaus.py`
Testimoduuli, joka sisältää yksikkötestit kaikille salausmenetelmille. Testit varmistavat, että:
- Salaus tuottaa odotetun tuloksen.
- Purku palauttaa alkuperäisen tekstin.

### `testi_salaus_teksti.txt`
Esimerkkitiedosto, jota voidaan käyttää ohjelman kanssa. Sisältää testitekstiä, joka voidaan salata ja purkaa.

---

## Esimerkki käytöstä

### Caesar-salaus
1. Valitse salausmenetelmä: **1**
2. Kirjoita teksti: **Hello**
3. Anna siirtoluku: **3**
4. Tulostus:
   ```
   Tulos:
   Khoor
   ```

### AES-salaus
1. Valitse salausmenetelmä: **2**
2. Kirjoita teksti: **Salainen**
3. Anna avain: **0123456789abcdef**
4. Tulostus:
   ```
   Tulos:
   6bc1bee22e409f96e93d7e117393172a
   ```

---

## Riippuvuudet

Ohjelma käyttää seuraavia kirjastoja:
- **`os`**: Tiedostojen käsittelyyn.
- **`cryptography`**: AES-salauksen toteutukseen.

Asenna tarvittavat riippuvuudet komennolla:
```bash
pip install cryptography
```

---

## Kehittäjä

**Topi Leinonen**  
Insinööri AMK - Ohjelmoinnin perusteet  
Kevät 2025