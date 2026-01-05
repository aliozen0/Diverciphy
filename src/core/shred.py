from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


class Shred:
    def __init__(self, payload):
        self.payload = payload

        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        self.public_key = self.private_key.public_key()

    def encrypt(self) -> bytes:
        mesaj = self.payload.encode()
        sifreli_metin = self.public_key.encrypt(
            mesaj,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"Sifreli metin: {sifreli_metin.hex()}")
        return sifreli_metin

    def decrypt(self):
        sifreli_metin = self.encrypt()
        mesaj = self.private_key.decrypt(
            sifreli_metin,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        print(f"Orijinal mesaj: {mesaj.decode()}")
        return mesaj

if __name__ == "__main__":
    key = b"Muthis-Gizli-Bir-Anahtar"
    shred = Shred(payload="Sifrele beni buna ihtiyacım war!")
    shred.decrypt()
        