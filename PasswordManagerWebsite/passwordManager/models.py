import base64

from django.db import models
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Password(models.Model):
    website = models.TextField(unique=True)
    username = models.TextField()
    hashed_pswd = models.TextField()

    @staticmethod
    def hash_pswd(password):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'0000000',
            iterations=480000,
        )

        return base64.urlsafe_b64encode(kdf.derive(password))

    def get_password(self, masterpswd_hash):
        f = Fernet(masterpswd_hash)
        return f.decrypt(self.hashed_pswd)

    def set_password(self, new_password, masterpswd_hash):
        f = Fernet(masterpswd_hash)
        if isinstance(new_password, str):
            new_password = bytes(new_password, 'utf-8')
        self.hashed_pswd = f.encrypt(new_password).decode('utf-8')
        self.save()
