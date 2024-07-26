from base64 import b64decode, b64encode
from os import urandom

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


class AesUtil:
    @staticmethod
    def encrypt_by_cbc(data, secret_key, iv):
        if not data:
            return data
        if not iv:
            raise ValueError("IV must not be blank")

        # 解码Base64编码的密钥和IV
        key = b64decode(secret_key)
        iv_bytes = b64decode(iv)

        # 创建AES Cipher对象
        cipher = AES.new(key, AES.MODE_CBC, iv=iv_bytes)

        # 使用PKCS5Padding填充数据
        padded_data = pad(data.encode(), AES.block_size)

        # 加密数据
        encrypted = cipher.encrypt(padded_data)

        # 将加密后的数据转换为Base64编码的字符串并返回
        return b64encode(encrypted).decode()

    @staticmethod
    def gen_key():
        return b64encode(urandom(16)).decode('utf-8')

    @staticmethod
    def gen_iv():
        return b64encode(urandom(16)).decode('utf-8')

    @staticmethod
    def gen_client_iv():
        return urandom(16).decode('utf-8')


if __name__ == "__main__":
    data = "Hello, World!"
    secret_key = "YOUR_BASE64_ENCODED_SECRET_KEY"
    iv = "YOUR_BASE64_ENCODED_IV"
