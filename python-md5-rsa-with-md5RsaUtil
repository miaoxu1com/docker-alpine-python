from base64 import b64encode, b64decode

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding


def encrypt_rsa(data, public_key_base64):
    # 解码Base64编码的公钥
    decoded_public_key = b64decode(public_key_base64)

    # 加载公钥
    public_key = serialization.load_der_public_key(
        decoded_public_key,
        backend=default_backend()
    )
    ciphertext = public_key.encrypt(
        data.encode('utf-8'),
        padding.PKCS1v15()
    )
    return b64encode(ciphertext).decode('utf-8')


if __name__ == '__main__':
    pass
