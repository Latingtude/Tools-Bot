from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import Crypto.Cipher.AES as AES
import base64
from nonebot.adapters.cqhttp import Adapter
import nonebot
from time import sleep as wait
from random import uniform,randint

question = on_command("question", priority=5, block=True)

@question.handle()
async def _(args: Message = CommandArg()):
    msg += "弱智吧问题精选"
    questions:dict = eval(open("./ruozhiba_question.json", "r", encoding="utf-8"))
    msg += f"您抽到的问题为：{questions.keys()[randint(0,90)]}"
    await question.finish(msg)
