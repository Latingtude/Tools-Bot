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

#---------------------------------------------------------
'''
采用AES对称加密算法
'''
# str不是16的倍数那就补足为16的倍数
def add_to_16(message):
    while len(message) % 16 != 0:
        message = str(message)
        message += '\0'
        # message = str(message)
    return message.encode('utf-8')  # 返回bytes


# 加密方法
def encoaes(message,key_pri):
    '''
    加密函数，传入明文 & 秘钥，返回密文；
    :param message: 明文
    :param key_pri: 秘钥
    :return:encrypted  密文
    '''
    # 初始化加密器
    aes = AES.new(add_to_16(key_pri), AES.MODE_ECB)
    # 将明文转为 bytes
    message_bytes = message.encode('utf-8')
    # 长度调整
    message_16 = add_to_16(message_bytes)
    #先进行aes加密
    encrypt_aes = aes.encrypt(message_16)
    #用base64转成字符串形式
    encrypt_aes_64 = base64.b64encode(encrypt_aes)
    return encrypt_aes_64.decode('utf-8')


# 解密方法
def decoaes(message,key_pri):
    '''
    解密函数，传入密文 & 秘钥，返回明文；
    :param message: 密文
    :param key_pri: 秘钥
    :return: encrypted 明文
    '''
    # 初始化加密器
    aes = AES.new(add_to_16(key_pri), AES.MODE_ECB)
    #优先逆向解密base64成bytes
    message_de64 = base64.b64decode(message)
    # 解密 aes
    message_de64_deaes = aes.decrypt(message_de64)
    try:
        message_de64_deaes_de = message_de64_deaes.decode('utf-8')
    except UnicodeDecodeError as e:
        print(f'UnicodeDecodeError:{e}\n疑似密码错误')
    else:
        return eval(message_de64_deaes_de.replace('\x00','')).decode()

aes_eventer = on_command("aes", priority=5, block=True)

@aes_eventer.handle()
async def handle_function(args: Message = CommandArg()):
    if params := args.extract_plain_text():
        msg += "\nAES 加密解密"
        params_l = params.split(" ")
        if params_l[0] == "encrypt":
            wait(wrd(0.5,0.9))
            msg += f"\n内容 {params_l[1]} \n密钥 {params_l[2]}\n加密为：\n{encoaes(params_l[1],params_l[2])}"
        elif params_l[0] == "decrypt":
            wait(wrd(0.5,0.9))
            msg += f"\n内容 {params_l[1]} \n密钥 {params_l[2]}\n解密为：\n{decoaes(params_l[1],params_l[2])}"
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
    aes_eventer.finish(msg)
