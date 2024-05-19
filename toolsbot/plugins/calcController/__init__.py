from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import Crypto.Cipher.AES as AES
import base64
from nonebot.adapters.cqhttp import Adapter
import nonebot
from time import sleep as wait
from random import uniform as wrd

calc_eventer = on_command("calc", priority=5)

@calc_eventer.handle()
async def _(event: Message = CommandArg()):
    msg = "简易计算器\n"
    if event.extract_plain_text() == "":
        msg += "请输入算式"
        await calc_eventer.send(msg)
    else:
        try:
            expression = event.extract_plain_text()
            msg += "结果：\n"
            if "+" in expression:
                msg += str(eval(expression))
            elif "-" in expression:
                msg += str(eval(expression))
            elif "*" in expression:
                msg += str(eval(expression))
            elif "/" in expression:
                msg += str(eval(expression))
            else:
                msg += "\n请输入正确的算式 PS: 本计算器为简易计算器，不支持高级运算。"
        except BaseException:
            msg += "\n请输入正确的算式 PS: 本计算器为简易计算器，不支持高级运算。"
        await calc_eventer.send(msg)