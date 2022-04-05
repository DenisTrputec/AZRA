import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet


class CryptoFile:
    @staticmethod
    def create_cypher(main_window, password):
        main_window.logDebug.info("Call:CryptoFile.create_cypher()")

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256,
            length=32,
            salt=b'w\x08\x92\nLe\x8fB\xd8X&|\xa9\x88\xd5y',
            iterations=100000,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        cipher = Fernet(key)

        main_window.logDebug.info("Return:CryptoFile.create_cypher()")

        return cipher

    @staticmethod
    def encrypt(main_window, filepath_source, filepath_destination, password):
        if main_window is not None:
            main_window.logDebug.info("Call:CryptoFile.encrypt()")

        with open(filepath_source, 'rb') as f:
            file = f.read()

        cipher = CryptoFile.create_cypher(main_window, password)
        encrypted_file = cipher.encrypt(file)

        with open(filepath_destination, 'wb') as f:
            f.write(encrypted_file)

        if main_window is not None:
            main_window.logDebug.info("Return:CryptoFile.encrypt()")

    @staticmethod
    def decrypt(main_window, filepath, password):
        main_window.logDebug.info("Call:CryptoFile.decrypt()")

        with open(filepath, 'rb') as ef:
            encrypted_file = ef.read()
        cipher = CryptoFile.create_cypher(main_window, password)

        ef = cipher.decrypt(encrypted_file)

        main_window.logDebug.info("Return:CryptoFile.decrypt()")
        return ef
