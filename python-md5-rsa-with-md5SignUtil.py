import base64
import warnings

from Crypto.Hash import MD5
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

warnings.filterwarnings("ignore")


def sign_rsa(data, private_key_base64):
    private_keyBytes = base64.b64decode(private_key_base64)
    priKey = RSA.importKey(private_keyBytes)
    signer = PKCS1_v1_5.new(priKey, )
    hash_obj = MD5.new(data.encode('utf-8'))

    signature = base64.b64encode(signer.sign(hash_obj))
    return signature


def get_sign_str(data_map):
    if data_map is None:
        return None
    sorted_data = sorted(data_map.items())
    sign_str = '&'.join([f"{k}={v}" for k, v in sorted_data])
    return sign_str


# Example usage
if __name__ == "__main__":
    private_key_str = "YOUR_PRIVATE_KEY_STRING"
    public_key_str = "YOUR_PUBLIC_KEY_STRING"
    data = "Hello, World!"
    signed_data = sign_rsa(data, private_key_str)
    print(f"Signed Data: {signed_data}")

