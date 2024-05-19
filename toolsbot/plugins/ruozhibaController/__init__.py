from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
import Crypto.Cipher.AES as AES
import base64
from nonebot.adapters.cqhttp import Adapter
import nonebot
from time import sleep as wait
from random import uniform,randint

question_eventer = on_command("question", priority=5, block=True)

@question_eventer.handle()
async def _(args: Message = CommandArg()):
    msg = ""
    msg += "弱智吧问题精选\n"
    questions_dict:dict = eval(open("./ruozhiba_question.json", "r", encoding="utf-8").read())
    question = list(questions_dict.values())[randint(0,90)]
    msg += f"您抽到的问题为：{question}"
    await question_eventer.finish(msg)
