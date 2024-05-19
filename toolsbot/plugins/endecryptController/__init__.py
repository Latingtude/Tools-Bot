from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import Crypto.Cipher.AES as AES
import base64
from nonebot.adapters.cqhttp import Adapter
import nonebot
from time import sleep as wait
from random import uniform as wrd

nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

# 加密方法
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

def encrypt_aes_pycryptodome(message, key):
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(message.encode('utf-8'), AES.block_size))
    return base64.b64encode(iv + ciphertext).decode('utf-8')

def decrypt_aes_pycryptodome(encrypted_message, key):
    encrypted_message = base64.b64decode(encrypted_message)
    iv = encrypted_message[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(encrypted_message[16:]), AES.block_size)
    return plaintext.decode('utf-8')

aes_eventer = on_command("aes", priority=5, block=True)

@aes_eventer.handle()
async def handle_function(args: Message = CommandArg()):
    msg = ""
    if params := args.extract_plain_text():
        msg += "\nAES 加密解密"
        params_l = params.split(" ")
        if params_l[0] == "encrypt":
            wait(wrd(0.5,0.9))
            msg += f"\n内容 {params_l[1]} \n密钥 {params_l[2]}\n加密为：\n{encrypt_aes_pycryptodome(params_l[1],params_l[2])}"
        elif params_l[0] == "decrypt":
            wait(wrd(0.5,0.9))
            msg += f"\n内容 {params_l[1]} \n密钥 {params_l[2]}\n解密为：\n{decrypt_aes_pycryptodome(params_l[1],params_l[2])}"
        else:
            wait(wrd(0.5,0.9))
            msg += "\n使用方法："
            wait(wrd(0.5,0.9))
            msg += "\n@bot *aes encrypt*decrypt [内容]"
    else:
        msg += "\nAES 加密解密"
        wait(wrd(0.5,0.9))
        msg += "\n使用方法："
        wait(wrd(0.5,0.9))
        msg += "\n@[bot] *aes encrypt*decrypt [内容]"
    await aes_eventer.finish(msg)
