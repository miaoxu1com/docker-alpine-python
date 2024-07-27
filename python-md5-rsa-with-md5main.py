import sys
import uuid

from AesUtil import *
from RsaUtil import *
from SignUtil import *


class Client:
    def __init__(self):
        self.appId = None
        self.version = None
        self.timestamp = None
        self.reqSecretKey = None
        self.reqIv = None
        self.outId = None
        # python中得None被序列化之后是null，但是如果是用了'&'.join(self.__dict__)拼接会被拼接成key=None
        self.sign = 'null'
        self.bizContent = None

    def set_sign(self, own_private_key: str):
        signStr = get_sign_str(self.__dict__);
        self.sign = sign_rsa(signStr, own_private_key).decode('utf-8')


def main():
    print(phone)
    md5_hex = hashlib.md5(phone.encode()).hexdigest()
    reqIv = AesUtil.gen_iv()
    reqSecretKey = AesUtil.gen_key()
    # 非“-----BEGIN PUBLIC KEY-----”开头 “-----END PUBLIC KEY-----” 结尾
    service_public_key = ""
    own_private_key = ""
        "phoneNoMd5": md5_hex
    }
    req_json = json.dumps(req_dict)
    c = Client()
    biz_content = req_json
    c.appId = ""
    c.version = "1.0"
    c.reqIv = encrypt_rsa(reqIv, service_public_key)
    c.reqSecretKey = encrypt_rsa(reqSecretKey, service_public_key)
    c.outId = str(uuid.uuid4()).replace("-", "")
    c.timestamp = int(time.time() * 1000)
    c.bizContent = AesUtil.encrypt_by_cbc(biz_content, reqSecretKey, reqIv)
    c.set_sign(own_private_key)
    print(c.__dict__)


if __name__ == '__main__':
    phone = sys.argv[1]
    main()
