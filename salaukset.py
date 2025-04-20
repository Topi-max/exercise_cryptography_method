#r33
#Leinonen Topi

import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import sys


class CaesarSalaus:
    # Lista sallituista merkeistä, joihin salaus vaikuttaa
    merkit = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?;:-_@#$%^&*()[]{}<>|/~`"

    @staticmethod
    def encrypt(message: str, shift: int) -> str:
        """
        Salakirjoittaa viestin Caesar-salauksella käyttäjän määrittämällä shift-arvolla.
        
        Parametrit:
        - message (str): Salattava viesti.
        - shift (int): Siirtoarvo, joka määrittää, kuinka monta askelta merkkejä siirretään.

        Palauttaa:
        - str: Salattu viesti.
        """
        salattu_viesti = ""  # Lopullinen salattu viesti
        for merkki in message:
            if merkki in CaesarSalaus.merkit:  # Tarkistetaan, onko merkki sallittu
                # Haetaan merkin indeksi ja lasketaan uusi indeksi siirron perusteella
                uusi_indeksi = (CaesarSalaus.merkit.index(merkki) + shift) % len(CaesarSalaus.merkit)
                salattu_viesti += CaesarSalaus.merkit[uusi_indeksi]  # Lisätään uusi merkki salattuun viestiin
            else:
                salattu_viesti += merkki  # Jos merkki ei ole sallittu, lisätään se sellaisenaan
        return salattu_viesti

    @staticmethod
    def decrypt(ciphertext: str, shift: int) -> str:
        """
        Purkaa Caesar-salauksen käyttäjän määrittämällä shift-arvolla.
        
        Parametrit:
        - ciphertext (str): Salattu viesti.
        - shift (int): Siirtoarvo, joka määrittää, kuinka monta askelta merkkejä siirretään takaisin.

        Palauttaa:
        - str: Purettu alkuperäinen viesti.
        """
        purettu_viesti = ""  # Lopullinen purettu viesti
        for merkki in ciphertext:
            if merkki in CaesarSalaus.merkit:  # Tarkistetaan, onko merkki sallittu
                # Haetaan merkin indeksi ja lasketaan alkuperäinen indeksi siirron perusteella
                uusi_indeksi = (CaesarSalaus.merkit.index(merkki) - shift) % len(CaesarSalaus.merkit)
                purettu_viesti += CaesarSalaus.merkit[uusi_indeksi]  # Lisätään alkuperäinen merkki purettuun viestiin
            else:
                purettu_viesti += merkki  # Jos merkki ei ole sallittu, lisätään se sellaisenaan
        return purettu_viesti
    
class AESSalaus:
    """Luodaan salaus AES-128/192/256 algoritmilla"""

    def __init__(self, avain: bytes):
        """
        Alustaa AES-salauksen annetulla avaimella.

        Parametrit:
        - avain (bytes): Avain AES-salausta varten. Pituus tarkistetaan ja korjataan tarvittaessa.
        """
        self.avain = self._varmista_avain(avain)

    @staticmethod
    def _varmista_avain(avain: bytes) -> bytes:
        """
        Varmistaa, että avain on 16, 24 tai 32 tavua pitkä.
        Jos avain on liian lyhyt, sitä täydennetään (pad) nollatavuilla.
        Jos avain on liian pitkä, se leikataan (trim) lähimpään sallittuun pituuteen.

        Parametrit:
        - avain (bytes): Tarkistettava avain.

        Palauttaa:
        - bytes: Oikean pituinen avain.
        """
        sallitut = (16, 24, 32)
        # Jos liian pitkä, leikataan 32 tavuun
        if len(avain) > max(sallitut):
            return avain[:32]
        # Etsi pienin sallittu pituus, joka on >= avaimen pituutta
        target = next(k for k in sallitut if k >= len(avain))
        # Pad: jos avain on lyhyt, täydennetään nollilla
        return avain.ljust(target, b'\0')

    def encrypt(self, plaintext: str) -> bytes:
        """
        Salaa merkkijonon AES-CBC-tilassa.

        Palauttaa:
        - bytes: iv (16 tavua) + ciphertext
        """
        data = plaintext.encode('utf-8')
        padder = padding.PKCS7(128).padder()
        padded = padder.update(data) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(
            algorithms.AES(self.avain),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        ct = encryptor.update(padded) + encryptor.finalize()

        return iv + ct

    def decrypt(self, iv_and_ciphertext: bytes) -> str:
        """
        Purkaa AES-CBC-salauksen.

        Parametrit:
        - iv_and_ciphertext (bytes): iv (16 tavua) + ciphertext

        Palauttaa:
        - str: Purettu plaintext
        """
        iv = iv_and_ciphertext[:16]
        ct = iv_and_ciphertext[16:]
        cipher = Cipher(
            algorithms.AES(self.avain),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        try:
            padded = decryptor.update(ct) + decryptor.finalize()
        except ValueError:
            raise ValueError("Purku epäonnistui: tarkista avain ja data")

        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded) + unpadder.finalize()

        return data.decode('utf-8')

    @staticmethod
    def to_hex(iv_and_ct: bytes) -> str:
        """Muuntaa iv+ct tavut hex-merkkijonoksi."""
        return iv_and_ct.hex()

    @staticmethod
    def from_hex(hexstr: str) -> bytes:
        """Muuntaa hex-merkkijonon takaisin tavujonoksi."""
        return bytes.fromhex(hexstr)
    

class VigenereSalaus:
    """Luokka Vigenere-salauksen toteuttamiseen.
    Käyttää Vigenere-salausta, joka on polyalfabeettinen siirtosalausmenetelmä.
    """

    def __init__(self, avain: str):
        """
        Alustaa Vigenere-salauksen avainsanalla.

        Parametrit:
        - avain (str): Avainsana, josta koostetaan siirrot.
        """
        puhdas = self._puhdista_avain(avain)
        if not puhdas:
            raise ValueError("Avainsanan täytyy sisältää vähintään yksi kirjain.")
        self.avain: str = puhdas

    @staticmethod
    def _puhdista_avain(avain: str) -> str:
        """
        Muuttaa avaimen pieniksi kirjaimiksi ja poistaa kaikki ei-kirjaimelliset merkit.

        Parametrit:
        - avain (str): Alkuperäinen avain.

        Palauttaa:
        - str: Puhdistettu, pienille kirjaimille muutettu avain.
        """
        return ''.join(filter(str.isalpha, avain)).lower()

    def encrypt(self, viesti: str) -> str:
        """
        Salaa merkkijonon Vigenere-algoritmilla käyttäen instanssin avainsanaa.

        Parametrit:
        - viesti (str): Salattava viesti.

        Palauttaa:
        - str: Salattu viesti.
        """
        salattu_viesti = []
        avain_pituus = len(self.avain)
        avain_indeksi = 0

        for merkki in viesti:
            if merkki.isalpha():
                offset = ord('a') if merkki.islower() else ord('A')
                siirto = ord(self.avain[avain_indeksi % avain_pituus]) - ord('a')
                uusi_merkki = chr((ord(merkki) - offset + siirto) % 26 + offset)
                salattu_viesti.append(uusi_merkki)
                avain_indeksi += 1
            else:
                salattu_viesti.append(merkki)

        return ''.join(salattu_viesti)

    def decrypt(self, ciphertext: str) -> str:
        """
        Purkaa Vigenere-salauksen käyttäen instanssin avainsanaa.

        Parametrit:
        - ciphertext (str): Purkuseen menevä salattu viesti.

        Palauttaa:
        - str: Purettu alkuperäinen viesti.
        """
        purettu_viesti = []
        avain_pituus = len(self.avain)
        avain_indeksi = 0

        for merkki in ciphertext:
            if merkki.isalpha():
                offset = ord('a') if merkki.islower() else ord('A')
                siirto = ord(self.avain[avain_indeksi % avain_pituus]) - ord('a')
                alkuperainen_merkki = chr((ord(merkki) - offset - siirto) % 26 + offset)
                purettu_viesti.append(alkuperainen_merkki)
                avain_indeksi += 1
            else:
                purettu_viesti.append(merkki)

        return ''.join(purettu_viesti)


