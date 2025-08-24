from nonebot import *
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import *
from nonebot.permission import SUPERUSER
import nonebot,random,json,requests
from time import sleep as wait
from random import uniform as wrd
import os
import dauCtl as dc

help_eventer = on_command("help", aliases={"帮助", "使用说明"}, priority=5)


@help_eventer.handle()
async def _(event: MessageEvent,arg: Message = CommandArg()):
    user = dc.User(event.get_user_id())
    if not user.isbanned():
        msg = "ToolsBot 工具菜单"
        msg += "\n功能："
        msg += "\n*base64*32*58*16*85 编码解码"
        msg += "\n*aes 加密解密"
        msg += "\n*help 显示此帮助信息"
        msg += "\n*check 检测bot是否存活"
        msg += "\n*about 关于bot"
        msg += "\n*morning 签到"
        msg += "\n*info 查看用户面板"
        msg += "\n*setinfo 设置用户 [注意：此功能仅 SUPERUSER 用户组可用]"
        msg += "\n*buy 买东西"
        msg += "\n*calc 计算器"
        msg += "\n*question 随机挑选弱智吧问题"
        msg += "\n*usecode 兑换码兑换"
        msg += "\n*pay 支付"
        msg += "\n*ban banlist unban 封禁用户 封禁用户列表 解封用户"
        msg += "\n*accountState 查看帐号状态"
        msg += "\n*ping Ping网站"
        msg += "\nping *pong 打 乒 乓 球"
        msg += "\n*echo 复读机"
        msg += "\n*ai AI 功能。"
        msg += "\n*cleanwaste 捡 垃 圾"
        wait(wrd(0.5,0.9))
        await help_eventer.send(msg)
    else:
        await help_eventer.send("ToolsBot 工具菜单\n    您的账号已被封禁。可执行 *accountState 查看帐号状态")

check_eventer = on_command("check", aliases={"检测"}, priority=5)

@check_eventer.handle()
async def _(event: Message = CommandArg()):
    msg = "ToolsBot 还活着"
    wait(wrd(0.5,0.9))
    await check_eventer.send(msg)

about_eventer = on_command("about", aliases={"关于"}, priority=5)

@about_eventer.handle()
async def _(event: MessageEvent,arg: Message = CommandArg()):
    user = dc.User(event.get_user_id())
    if not user.isbanned():
        """
        关于 Bot
        版本: 1.0.3-release (Skills 10)
        最后一次更新时间：2024/5/19 11:12
        [作者网站]
        https://moesoft.xyz
        https://virtual.icp.moesoft.xyz (虚拟ICP备案，玩的)
        [代码]
        基于Python-Nonebot1 (https:**v1.nonebot.dev*)
        Python版本:3.12.2 VIRTUAL ENVIRONMENT
        NoneBot版本:1.9.1
        """
        msg = "关于 Bot"
        msg += "\n版本: 1.0.5-release (Skills 12)"
        msg += "\n最后一次更新时间：2025/8/24 15: 33"
        msg += "\n[作者网站]"
        msg += "\nhttps://airoj.latingtude-studios.icu"
        msg += "\nhttps://icp.latingtude-studios.icu (虚拟ICP备案，玩的)"
        msg += "\n[代码]"
        msg += "\n基于 Python, Nonebot 2 (https://nonebot.dev/)"
        msg += "\nPython 版本: v3.13.3 VIRTUAL ENVIRONMENT"
        msg += "\nNoneBot 版本: v2.1.2"
        msg += "\nOpenShamrock: v1.0.9 (偶尔用)"
        msg += "\nNapCatQQ: v4.8.98"
        msg += "\nDKoEzDatabase: 0.0.1"
        wait(wrd(0.5,0.9))
        await about_eventer.send(msg)
    else:
        await about_eventer.send("关于 Bot\n    您的账号已被封禁。")

ban_eventer = on_command("ban", aliases={"封禁"}, priority=5)

@ban_eventer.handle()
async def _(event: GroupMessageEvent,arg: Message = CommandArg()):
    msg = ""
    text = arg.extract_plain_text()
    if text == "":
        msg = "ToolsBot 封禁功能"
        msg += "\n功能："
        msg += "\n*ban 封禁用户"
        msg += "\n*banlist 查看封禁列表"
        msg += "\n*unban 解封用户"
    else:
        msg = "ToolsBot 封禁用户"
        msg += "\n用户ID: " + text
        if event.get_user_id() == "2733392694":
            bannedlist:dict = eval(open("./banned.json","r").read())
            bannedlist.update({text:True})
            open("./banned.json","w+").write(str(bannedlist))
            msg += "\n封禁成功"
        else:
            msg += "\n权限不足."
    await ban_eventer.finish(msg)


banlist_eventer = on_command("banlist", aliases={"封禁列表"}, priority=5)

@banlist_eventer.handle()
async def _(event: GroupMessageEvent):
    msg = "ToolsBot 封禁列表"
    bannedlist:dict = eval(open("./banned.json","r").read())
    for id in bannedlist:
        msg += "\n封禁用户-用户ID: " + id
    await banlist_eventer.finish(msg)
    

unban_eventer = on_command("unban", aliases={"解封"}, priority=5)

@unban_eventer.handle()
async def _(event: GroupMessageEvent,arg: Message = CommandArg()):
    msg = "ToolsBot 解封"
    text = arg.extract_plain_text()
    if text == "":
        msg = "ToolsBot 解封"
        msg += "\n*unban [id] 来解封"
    else:
        msg = "ToolsBot 解封"
        msg += "\n用户ID: " + text
        if event.get_user_id() == "2733392694":
            bannedlist:dict = eval(open("./banned.json","r").read())
            del bannedlist[text]
            open("./banned.json","w+").write(str(bannedlist))
            msg += "\n解封成功"
        else:
            msg += "\n权限不足."
    
    await unban_eventer.finish(msg)

accountState_eventer = on_command("accountState", aliases={"账号状态"}, priority=5)

@accountState_eventer.handle()
async def _(event: GroupMessageEvent,arg: Message = CommandArg()):
    msg = "ToolsBot 账号状态"
    user = dc.User(event.get_user_id())
    if user.isbanned():
        msg += "\n账号状态：被封禁"
    else:
        msg += "\n账号状态：正常"
    await accountState_eventer.finish(msg)

ping_eventer = on_startswith("ping", priority=5)

@ping_eventer.handle()
async def _(event: GroupMessageEvent):
    await ping_eventer.send("pong")

pong_eventer = on_startswith("*pong")

@pong_eventer.handle()
async def _(event: GroupMessageEvent):
    await pong_eventer.send("ping")

def ping(url:str):
    return str(requests.get(url).status_code)
r_ping_eventer  = on_command("ping", aliases={"ping网站"}, priority=5)

@r_ping_eventer.handle()
async def _(event: GroupMessageEvent,arg: Message = CommandArg()):
    msg = "ToolsBot 网站状态"
    url = arg.extract_plain_text()
    if url == "":
        msg += "\n*ping [url] 来测试网站状态"
    else:
        msg += "\n测试网站状态: " + url
        msg += "\n状态: " + ping(url)
    await r_ping_eventer.finish(msg)
