from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.cqhttp import Adapter
import nonebot
from time import sleep as wait
from random import uniform as wrd

nonebot.init(superusers={"2733392694"},command_start={"*"})
driver = nonebot.get_driver()
driver.register_adapter(Adapter)
nonebot.load_plugin("nonebot_plugin_gocqhttp")

help_eventer = on_command("help", aliases={"帮助", "使用说明"}, priority=5)


@help_eventer.handle()
async def _(event: Message = CommandArg()):
    msg = "ToolsBot 工具菜单"
    msg += "\n功能：\n"
    msg += "\n*base64*32*58*16*85 编码解码\n"
    msg += "\n*aes 加密解密\n"
    msg += "\n*help 显示此帮助信息\n"
    msg += "\n*check 检测bot是否存活\n"
    msg += "\n*about 关于bot\n"
    msg += "\n*morning 签到\n"
    msg += "\n*info 查看用户面板\n"
    msg += "\n*setinfo 设置用户 [注意：此功能仅 SUPERUSER 用户组可用]\n"
    msg += "\n*buy 买东西"
    wait(wrd(0.5,0.9))
    await help_eventer.send(msg)

check_eventer = on_command("check", aliases={"检测"}, priority=5)

@check_eventer.handle()
async def _(event: Message = CommandArg()):
    msg = "ToolsBot 还活着"
    wait(wrd(0.5,0.9))
    await check_eventer.send(msg)

about_eventer = on_command("about", aliases={"关于"}, priority=5)

@about_eventer.handle()
async def _(event: Message = CommandArg()):
    """
    关于 Bot
    版本: 1.0.3-release (Skills 8)
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
    msg += "\n版本: 1.0.3-release (Skills 8)"
    msg += "\n最后一次更新时间：2024/5/18 14:30"
    msg += "\n[作者网站]"
    msg += "\nhttps://moesoft.xyz"
    msg += "\nhttps://virtual.icp.moesoft.xyz (虚拟ICP备案，玩的)"
    msg += "\n[代码]"
    msg += "\n基于Python-Nonebot1 (https://v1.nonebot.dev/)"
    msg += "\nPython版本:3.12.2 VIRTUAL ENVIRONMENT"
    msg += "\nNoneBot版本:1.9.1"
    msg += "\nOpenShamrock: 1.0.9 (偶尔用)"
    msg += "\nLLOneBot: v3.26.0"
    msg += "\nDKoEzDatabase: 0.0.1"
    wait(wrd(0.5,0.9))
    await about_eventer.send(msg)
