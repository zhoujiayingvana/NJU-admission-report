from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
from PIL import Image
from io import BytesIO


def convert2base64(input_path, output_path):
    with open(input_path, 'rb') as f_reader:
        with open(output_path, 'wb+') as f_writer:
            im = f_reader.read()
            b64 = base64.b64encode(im)
            f_writer.write(b64)


def compress_img(input_path, output_path, quality=10):
    # quality 是压缩比，数字越小压缩后的图片大小越小
    im = Image.open(input_path)
    im.save(output_path, quality=quality)


'''
AES工具类：使用ECB模式加密，pkcs7格式的padding
'''


class AESUtil:
    # 使用ECB模式加密
    MODE = AES.MODE_ECB
    # 使用默认的pkcs7 padding
    PAD_STYLE = 'pkcs7'
    ENCODING = 'UTF-8'

    # key长度为16或24或32，分别对应AES-128、AES-192、AES-256，暂时采用16
    def _add_to_16(par):
        par = par.encode()  # 先将字符串类型数据转换成字节型数据
        if len(par) > 16:
            par = par[:16]
        while len(par) % 16 != 0:  # 对字节型数据进行长度判断
            par += b'\x00'  # 如果字节型数据长度不是16倍整数就进行补充
        return par.decode()

    @staticmethod
    def encrypt(plaintext: str, key: str) -> str:
        # 将密钥编码为UTF-8格式的bytes
        key = AESUtil._add_to_16(key)
        key_bytes = key.encode(AESUtil.ENCODING)
        # 创建AES对象
        cipher = AES.new(key_bytes, AESUtil.MODE)
        # 将明文编码为UTF-8格式的bytes
        plaintext_bytes = plaintext.encode(AESUtil.ENCODING)
        # 为编码后的明文添加padding
        plaintext_bytes_padded = pad(
            plaintext_bytes, AES.block_size, AESUtil.PAD_STYLE)
        # 执行加密
        ciphertext_bytes = cipher.encrypt(plaintext_bytes_padded)
        # 将加密后的bytes进行base64编码
        # 注意：不能用encodebytes！否则会每76个字符增加一个换行符，见：https://docs.python.org/zh-cn/3/library/base64.html
        ciphertext_base64_bytes = base64.b64encode(ciphertext_bytes)
        # 将base64编码过的bytes，解码为Python中使用的字符串类型（即unicode字符串）
        ciphertext = ciphertext_base64_bytes.decode(AESUtil.ENCODING)
        return ciphertext

    @staticmethod
    def decrypt(ciphertext: str, key: str) -> str:
        key = AESUtil._add_to_16(key)
        # 将密钥编码为UTF-8格式的bytes
        key_bytes = key.encode(AESUtil.ENCODING)
        # 创建AES对象
        decrypter = AES.new(key_bytes, AESUtil.MODE)
        # 将密文编码为UTF-8格式的（同时也是base64编码的）bytes
        ciphertext_base64_bytes = ciphertext.encode(AESUtil.ENCODING)
        # 将base64编码的bytes，解码为原始的密文bytes
        ciphertext_bytes = base64.b64decode(ciphertext_base64_bytes)
        # 解码为明文
        plaintext_bytes_padded = decrypter.decrypt(ciphertext_bytes)
        # 去掉Padding
        plaintext_bytes = unpad(plaintext_bytes_padded,
                                AES.block_size, AESUtil.PAD_STYLE)
        # 将UTF-8格式编码的明文bytes，解码为Python中的字符串类型（即unicode字符串）
        plaintext = plaintext_bytes.decode(AESUtil.ENCODING)
        return plaintext


def encrypt_img(input_path, output_path, key="123456"):
    with open(input_path, 'rb') as f_reader:
        with open(output_path, 'w') as f_writer:
            im = f_reader.read()
            b64 = base64.b64encode(im)
            f_writer.write(AESUtil.encrypt(b64.decode(), key))


def decrypt_img(input_path, key):
    with open(input_path, 'r') as f_reader:
        im = f_reader.read()
        de = AESUtil.decrypt(im, key)
        return base64.b64decode(de)


if __name__ == '__main__':
    i_path = './for_test/002.jpg'
    compress_path = './for_test/002_compress.jpg'
    encrypt_path = './assets/xcm_pic.txt'
    key = "123456"
    encrypt_img(compress_path, encrypt_path, key)
    # de = decrypt_img(encrypt_path, key)
    # im = Image.open(BytesIO(de))
    # im.show()
    pass
