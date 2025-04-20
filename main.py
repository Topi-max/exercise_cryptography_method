# r33
# Leinonen Topi

from salaukset import CaesarSalaus, AESSalaus, VigenereSalaus

def valitse_salausmenetelma():
    """
    Kysyy käyttäjältä, minkä salausmenetelmän hän haluaa valita.

    Palauttaa:
    - str: Käyttäjän valitsema salausmenetelmä (1, 2 tai 3).
    """
    while True:
        print("\nValitse salausmenetelmä:")
        print("1. Caesar - Yksinkertainen siirtosalaus.")
        print("2. AES    - Vahva lohkoalgoritmi CBC-tilassa.")
        print("3. Vigenère - Polyalfabeettinen siirtosalaus.")
        valinta = input("Anna valintasi (1-3): ")
        if valinta in ("1", "2", "3"):
            return valinta
        print("Virheellinen valinta. Valitse 1, 2 tai 3.")

def valitse_syottotapa():
    """
    Kysyy käyttäjältä, haluaako hän kirjoittaa tekstin itse vai lukea sen tiedostosta.

    Palauttaa:
    - str: Käyttäjän valitsema syöttötapa (1 tai 2).
    """
    while True:
        print("\nHaluatko kirjoittaa tekstin itse vai lukea tiedostosta?")
        print("1. Kirjoitan itse")
        print("2. Lue tiedostosta")
        valinta = input("Anna valintasi (1-2): ")
        if valinta in ("1", "2"):
            return valinta
        print("Virheellinen valinta. Valitse 1 tai 2.")

def lue_viesti(valinta):
    """
    Lukee viestin käyttäjän valinnan perusteella.

    Parametrit:
    - valinta (str): Käyttäjän valitsema syöttötapa (1 tai 2).

    Palauttaa:
    - str: Käyttäjän kirjoittama tai tiedostosta luettu viesti.
    - None: Jos tiedostoa ei löydy tai käyttäjä haluaa lopettaa.
    """
    if valinta == "1":
        # Käyttäjä kirjoittaa viestin itse
        print("Jos haluat purkaa AES salauksen, kirjoita hex-muotoinen merkkijono.")
        print("Jos haluat purkaa Caesar tai Vigenere salauksen, kirjoita merkkijono.")
        print("Jos haluat salata tekstin, niin kirjoita teksti")
        return input("Kirjoita teksti: ")
    
    # Käyttäjä haluaa lukea viestin tiedostosta
    while True:
        tiedosto = input("Anna tiedoston nimi (esim. viesti.txt), jos se on samassa kansiossa kuin ohjelma. "
                         "Jos tiedosto sijaitsee toisessa kansiossa, anna koko tiedostopolku (esim. C:\\Users\\Käyttäjä\\Documents\\viesti.txt). "
                         "Jätä tyhjäksi ja paina Enter lopettaaksesi: ")
        if tiedosto.strip() == "":
            # Käyttäjä haluaa lopettaa
            print("Lopetetaan tiedoston lukeminen.")
            return None
        try:
            # Yritetään avata tiedosto ja lukea sen sisältö
            with open(tiedosto, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            # Jos tiedostoa ei löydy, ilmoitetaan virheestä ja pyydetään uusi syöte
            print("Tiedostoa ei löytynyt. Tarkista tiedoston nimi ja sijainti tai jätä tyhjäksi lopettaaksesi.")

def main():
    """
    Ohjelman pääfunktio, joka hallitsee salaus- ja purkuprosessia.
    """
    print("Tervetuloa salausohjelmaan!")

    salaus_valinta = valitse_salausmenetelma()
    syotto_valinta = valitse_syottotapa()
    viesti = lue_viesti(syotto_valinta)
    if viesti is None:
        return  # Lopetetaan, jos viestiä ei saatu

    salaa_vai_pura = input("Haluatko (1) salata vai (2) purkaa? ")
    if salaa_vai_pura not in ("1", "2"):
        print("Virheellinen valinta. Valitse 1 (salataan) tai 2 (puretaan).")
        return

    tulos = None

    # 1) Caesar-salaus
    if salaus_valinta == "1":
        while True:
            try:
                shift = int(input("Anna Caesar-salauksen siirtoluku (kokonaisluku): "))
                break  # Kelvollinen siirtoluku, poistutaan silmukasta
            except ValueError:
                print("Siirtoluvun pitää olla kokonaisluku! Yritä uudelleen.")
        if salaa_vai_pura == "1":
            tulos = CaesarSalaus.encrypt(viesti, shift)
        else:
            tulos = CaesarSalaus.decrypt(viesti, shift)

    # 2) AES-salaus
    elif salaus_valinta == "2":
        print("AES-avain padataan tai trimmataan automaattisesti 16/24/32 tavuun.")
        while True:
            avain_str = input("Anna AES-avain (vähintään 16 merkkiä): ")
            if len(avain_str) < 16:
                print("Avain on liian lyhyt! Sen tulee olla vähintään 16 merkkiä. Yritä uudelleen.")
            else:
                break  # Kelvollinen avain, poistutaan silmukasta
        avain = avain_str.encode('utf-8')
        aes = AESSalaus(avain)
        if salaa_vai_pura == "1":
            raw = aes.encrypt(viesti)
            tulos = AESSalaus.to_hex(raw)
        else:
            while True:
                hexstr = input("Anna hex-muotoinen salattu teksti: ")
                try:
                    raw = AESSalaus.from_hex(hexstr)
                    tulos = aes.decrypt(raw)
                    break  # Kelvollinen syöte, poistutaan silmukasta
                except (ValueError, TypeError):
                    print("Virheellinen hex-syöte tai avain. Yritä uudelleen.")

    # 3) Vigenère-salaus
    else:
        print("Vigenère-avain saa sisältää vain kirjaimia.")
        while True:
            avain = input("Anna Vigenère-avain: ")
            if not avain.isalpha():
                print("Avain sisältää virheellisiä merkkejä! Yritä uudelleen.")
            else:
                break  # Kelvollinen avain, poistutaan silmukasta
        vig = VigenereSalaus(avain)
        if salaa_vai_pura == "1":
            tulos = vig.encrypt(viesti)
        else:
            tulos = vig.decrypt(viesti)

    if tulos is None:
        print("Tapahtui odottamaton virhe.")
        return

    print("\nTulos:")
    print(tulos)

    # Kysytään, tallennetaanko tulos tiedostoon
    while True:
        tallenna = input("Tallennetaanko tulos tiedostoon? (k/e): ").lower()
        if tallenna == "k":
            nimi = input("Anna tallennustiedoston nimi (esim. tulos.txt): ")
            with open(nimi, "w", encoding="utf-8") as f:
                f.write(tulos)
            print(f"Tulos tallennettu tiedostoon {nimi}.")
            break
        elif tallenna == "e":
            break
        else:
            print("Virheellinen valinta. Valitse 'k' (kyllä) tai 'e' (ei).")

    # Kysytään, haluaako käyttäjä purkaa viestin heti salauksen jälkeen
    if salaa_vai_pura == "1":
        while True:
            pura = input("Haluatko purkaa viestin heti? (k/e): ").lower()
            if pura == "k":
                if salaus_valinta == "1":
                    tulos = CaesarSalaus.decrypt(tulos, shift)
                elif salaus_valinta == "2":
                    tulos = aes.decrypt(raw)
                elif salaus_valinta == "3":
                    tulos = vig.decrypt(tulos)
                print("\nPurettu viesti:")
                print(tulos)
                break
            elif pura == "e":
                break
            else:
                print("Virheellinen valinta. Valitse 'k' (kyllä) tai 'e' (ei).")

if __name__ == "__main__":
    main()

