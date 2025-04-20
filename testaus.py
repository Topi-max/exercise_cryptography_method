# r33
# Leinonen Topi

"""Testaus moduuli testataakseni toiminnonallisuutta."""

from salaukset import CaesarSalaus, AESSalaus, VigenereSalaus

def test_caesar():
    print("Testataan Caesar-salausta...")
    pt = "Hello"
    shift = 3
    ct = CaesarSalaus.encrypt(pt, shift)
    assert ct == "Khoor", f"Caesar-salauksen salaus epäonnistui: {ct} != Khoor"
    print(f"Salaus onnistui: {pt} -> {ct}")
    decrypted = CaesarSalaus.decrypt(ct, shift)
    assert decrypted == pt, f"Caesar-salauksen purku epäonnistui: {decrypted} != {pt}"
    print(f"Purku onnistui: {ct} -> {decrypted}")

def test_aes():
    print("Testataan AES-salausta...")
    key = b"0123456789abcdef"
    aes = AESSalaus(key)
    pt = "Salainen"
    raw = aes.encrypt(pt)
    hex_ct = AESSalaus.to_hex(raw)
    assert raw != pt.encode('utf-8'), "AES-salaus epäonnistui: ciphertext == plaintext"
    print(f"  Salattu: {pt} -> {hex_ct}")
    decrypted = aes.decrypt(raw)
    assert decrypted == pt, f"AES-purku epäonnistui: {decrypted} != {pt}"
    print(f"  Purettu: {hex_ct} -> {decrypted}")

def test_vigenere():
    print("Testataan Vigenère-salausta...")
    vig = VigenereSalaus("lemon")
    pt = "Attack at dawn!"
    ct = vig.encrypt(pt)
    assert ct != pt, f"Vigenère-salauksen salaus epäonnistui: {ct} == {pt}"
    print(f"Salaus onnistui: {pt} -> {ct}")
    decrypted = vig.decrypt(ct)
    assert decrypted == pt, f"Vigenère-salauksen purku epäonnistui: {decrypted} != {pt}"
    print(f"Purku onnistui: {ct} -> {decrypted}")

if __name__ == "__main__":
    try:
        test_caesar()
        test_aes()
        test_vigenere()
        print("\nKaikki testit läpäisty!")
    except AssertionError as e:
        print(f"\nTesti epäonnistui: {e}")
