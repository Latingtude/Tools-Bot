from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import base64,base58
from nonebot.adapters.cqhttp import Adapter
import nonebot
from time import sleep as wait
from random import uniform as wrd


nonebot.init()
driver = nonebot.get_driver()
driver.register_adapter(Adapter)

base64_eventer = on_command("base64", aliases={"b64"}, priority=5)

@base64_eventer.handle()
async def handle_function(args: Message = CommandArg()):
    msg = ""
    if params := args.extract_plain_text():
        msg += "\nBase64 加密解密"
        params_l = params.split(" ")
        if params_l[0] == "encode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n编码为：\n{base64.b64encode(params_l[1].encode()).decode()}"
        elif params_l[0] == "decode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n解码为：\n{base64.b64decode(params_l[1].encode()).decode()}"
        else:
            wait(wrd(0.5,0.9))
            msg += "\n使用方法："
            wait(wrd(0.5,0.9))
            msg += "\n@bot *base64 encode*decode [内容]"
    else:
        msg += "\nBase64 加密解密"
        wait(wrd(0.5,0.9))
        msg += "\n使用方法："
        wait(wrd(0.5,0.9))
        msg += "\n@[bot] *base64 encode*decode [内容]"
    base64_eventer.finish(msg)

base32_eventer = on_command("base32", aliases={"b32"}, priority=5)

@base32_eventer.handle()
async def handle_function(args: Message = CommandArg()):
    msg = ""
    if params := args.extract_plain_text():
        msg += "\nBase32 加密解密"
        params_l = params.split(" ")
        if params_l[0] == "encode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n编码为：\n{base64.b32encode(params_l[1].encode()).decode()}"
        elif params_l[0] == "decode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n解码为：\n{base64.b32decode(params_l[1].encode()).decode()}"
        else:
            msg += "\n使用方法："
            wait(wrd(0.5,0.9))
            msg += "\n@bot *base32 encode*decode [内容]"
    else:
        msg += "\nBase32 加密解密"
        wait(wrd(0.5,0.9))
        msg += "\n使用方法："
        wait(wrd(0.5,0.9))
        msg += "\n@[bot] *base32 encode*decode [内容]"
    base32_eventer.finish(msg)

base16_eventer = on_command("base16", aliases={"b16"}, priority=5)

@base16_eventer.handle()
async def handle_function(args: Message = CommandArg()):
    msg = ""
    if params := args.extract_plain_text():
        msg += "\nBase16 加密解密"
        params_l = params.split(" ")
        if params_l[0] == "encode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n编码为：\n{base64.b16encode(params_l[1].encode()).decode()}"
        elif params_l[0] == "decode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n解码为：\n{base64.b16decode(params_l[1].encode()).decode()}"
        else:
            wait(wrd(0.5,0.9))
            msg += "\n使用方法："
            wait(wrd(0.5,0.9))
            msg += "\n@bot *base16 encode*decode [内容]"
    else:
        msg += "\nBase16 加密解密"
        wait(wrd(0.5,0.9))
        msg += "\n使用方法："
        wait(wrd(0.5,0.9))
        msg += "\n@[bot] *base16 encode*decode [内容]"
    base16_eventer.finish(msg)

base85_eventer = on_command("base85", aliases={"b85"}, priority=5)

@base85_eventer.handle()
async def handle_function(args: Message = CommandArg()):
    msg = ""
    if params := args.extract_plain_text():
        msg += "\nBase85 加密解密"
        params_l = params.split(" ")
        if params_l[0] == "encode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n编码为：\n{base64.b85encode(params_l[1].encode()).decode()}"
        elif params_l[0] == "decode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n解码为：\n{base64.b85decode(params_l[1].encode()).decode()}"
        else:
            msg += "\n使用方法："
            wait(wrd(0.5,0.9))
            msg += "\n@bot *base85 encode*decode [内容]"
    else:
        msg += "\nBase85 加密解密"
        wait(wrd(0.5,0.9))
        msg += "\n使用方法："
        wait(wrd(0.5,0.9))
        msg += "\n@[bot] *base85 encode*decode [内容]"
    base85_eventer.finish(msg)

base58_eventer = on_command("base58", aliases={"b58"}, priority=5)

@base58_eventer.handle()
async def handle_function(args: Message = CommandArg()):
    msg = ""
    if params := args.extract_plain_text():
        msg += "\nBase58 加密解密"
        params_l = params.split(" ")
        if params_l[0] == "encode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n编码为：\n{base58.b58encode(params_l[1].encode()).decode()}"
        elif params_l[0] == "decode":
            wait(wrd(0.5,0.9))
            msg += f"\n{params_l[1]} \n解码为：\n{base58.b58decode(params_l[1].encode()).decode()}"
        else:
            wait(wrd(0.5,0.9))
            msg += "\n使用方法："
            wait(wrd(0.5,0.9))
            msg += "\n@[bot] *base58 encode*decode [内容]"
    else:
        msg += "\nBase85 加密解密"
        wait(wrd(0.5,0.9))
        msg += "\n使用方法："
        wait(wrd(0.5,0.9))
        msg += "\n@[bot] *base58 encode*decode [内容]"
    base58_eventer.finish(msg)