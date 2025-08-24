from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import *
from nonebot.permission import SUPERUSER
import datetime as dt
import nonebot,random,json
from time import sleep as wait
from random import uniform as wrd
import os

class Database:
    def __init__(self, db_name:str, id:str):
        self.db_name = db_name
        self.position = "./database"
        self.id = id
    
    def write(self, data:str):
        open(f"./database/{self.id}","w+", encoding="utf-8").write(data)
    
    def read(self) -> str:
        if os.path.exists(f"./database/{self.id}"):
            return open(f"./database/{self.id}","r", encoding="utf-8").read()
        else:
            return ""
    
    def delete(self):
        if os.path.exists(f"./database/{self.id}"):
            os.remove(f"./database/{self.id}")
        else:
            pass
    
    def find(self,id:str) -> bool:
        return id in os.listdir(self.position)
    
class User:
    def __init__(self,id:str = "",name:str = "",score:int = 0):
        self.id = id
        self.name = name
        self.score = score
        self.buied = []
        self.objectDatabase = Database("maindb",id)
        self.banned = False
        if (self.objectDatabase.find(id)):
            self.load(id)
        else:
            self.objectDatabase.write(json.dumps(self.get()))
    
    def load(self,userid:str): 
        self.objectDatabase: Database
        database: dict = json.loads(self.objectDatabase.read())
        self.name = database.get("name", "[ERROR FOUND]")
        self.score = database.get("score", 0)
        self.buied = database.get("buied", [])
        
        banneds = eval(open("./banned.json","r",encoding="utf-8").read())
        if userid in banneds:
            self.banned = True
        else:
            self.banned = False

        if userid == "3085132801":
            self.banned = True
        

    def addScore(self,score:int):
        if not self.banned:
            self.score += score

    def getScore(self):
        if not self.banned:
            return self.score
    
    def getName(self):
        if not self.banned:
            return self.name
    
    def getId(self):
        if not self.banned:
            return self.id
    
    def resetName(self,name:str):
        self.name = name
    
    def rebindId(self,id:str):
        self.id = id
    
    def save(self):
        Database("maindb",self.id).write(json.dumps(self.get()))
    
    def setscore(self,score:int):
        self.score = score
    
    def buyItem(self,item:str):
        if not self.banned:
            self.buied.append(item)
    
    def useItem(self,item:str):
        howcando:dict = eval(open("./howCanDo.json","r",encoding="utf-8").read())
        for name in self.buied:
            for namer,do in howcando.items():
                if name == namer:
                    return self.do(do)
        return "    - 无效的物品"
    
    def do(self,action:str) -> str | None:
        if "morning.score.x" in action:
            add_x = int(action.replace("morning.score.x",""))
            todayScorePlus:dict = eval(open("./todayScorePlus.json","r",encoding="utf-8").read())
            todayScorePlus.update({self.id:add_x})
            open("./todayScorePlus.json","w+",encoding="utf-8").write(str(todayScorePlus))
            return "    - 使用成功，如果您今天没有 /morning，使用 /morning 即可获得积分。"
        elif "guess.money.try" in action:
            cp_money = random.randint(10,10000000)
            if cp_money == 10:
                self.addScore(100000)
                self.buied.remove("彩票")
                return "    - 恭喜你，中奖了！获得 10,0000 积分"
            else:
                anwei = random.randint(0,5)
                self.addScore(anwei)
                self.buied.remove("彩票")
                return f"    - 很遗憾，没有中奖。但获得 {anwei} 积分"

    def getBuied(self):
        return self.buied
    
    def isbanned(self):
        return self.banned
    
    def get(self) -> dict:
        return {
            "name": self.name,
            "score": self.score,
            "buied": self.buied
        }
    
    def __str__(self) -> dict:
        return self.get() # 大大大大大哥别骂我，这里写 dict 纯粹因为不写这个会报错
qiandao_eventer = on_command("morning", aliases={"签到", "签到功能"}, priority=5)

@qiandao_eventer.handle()
async def _(event:GroupMessageEvent | PrivateMessageEvent,arg: Message = CommandArg()):
    msg = ""
    morningd:dict = eval(open("./todayMorningd.json","r",encoding="utf-8").read())
    score_plus:dict = eval(open("./todayScorePlus.json","r",encoding="utf-8").read())
    userid = event.get_user_id()
    user = User(userid)
    if not user.isbanned():
        if userid in morningd.keys():
            now = dt.datetime.now()
            morningd_time = dt.datetime.strptime(morningd.get(userid),"%Y-%m-%d %H:%M:%S.%f")
            if morningd_time.day < now.day:
                if userid in score_plus.keys():
                    msg += "\n签到 v1.0.0"
                    msg += "\n    - 签到中..."
                    msg += "\n    - 签到成功!"
                    useridr: int | None = score_plus.get(userid)
                    score = random.randint(1,100) * useridr
                    msg += f"\n    - 获得 {score} 积分"
                    userid = event.get_user_id()
                    user = User(userid)
                    user.addScore(score * score_plus.get(userid))
                    msg += f"\n    - 当前积分: {user.getScore()}"
                    morningd.update({userid:dt.datetime.now().__str__()})
                    open("./todayMorningd.json","w+",encoding="utf-8").write(str(morningd))
                    user.save()
                    await qiandao_eventer.finish(msg)
                else:
                    msg += "\n签到 v1.0.0"
                    msg += "\n    - 签到中..."
                    msg += "\n    - 签到成功!"
                    score = random.randint(1,100)
                    msg += f"\n    - 获得 {score} 积分"
                    userid = event.get_user_id()
                    user = User(userid)
                    user.addScore(score)
                    morningd.update({userid:dt.datetime.now().__str__()})
                    open("./todayMorningd.json","w+",encoding="utf-8").write(str(morningd))
                    msg += f"\n    - 当前积分: {user.getScore()}"
                    user.save()
                    await qiandao_eventer.finish(msg)
            elif morningd_time.month < now.month:
                if userid in score_plus.keys():
                    msg += "\n签到 v1.0.0"
                    msg += "\n    - 签到中..."
                    msg += "\n    - 签到成功!"
                    useridr: int | None = score_plus.get(userid)
                    score = random.randint(1,100) * useridr
                    msg += f"\n    - 获得 {score} 积分"
                    userid = event.get_user_id()
                    user = User(userid)
                    user.addScore(score * score_plus.get(userid))
                    msg += f"\n    - 当前积分: {user.getScore()}"
                    morningd.update({userid:dt.datetime.now().__str__()})
                    open("./todayMorningd.json","w+",encoding="utf-8").write(str(morningd))
                    user.save()
                    await qiandao_eventer.finish(msg)
                else:
                    msg += "\n签到 v1.0.0"
                    msg += "\n    - 签到中..."
                    msg += "\n    - 签到成功!"
                    score = random.randint(1,100)
                    msg += f"\n    - 获得 {score} 积分"
                    userid = event.get_user_id()
                    user = User(userid)
                    user.addScore(score)
                    morningd.update({userid:dt.datetime.now().__str__()})
                    open("./todayMorningd.json","w+",encoding="utf-8").write(str(morningd))
                    msg += f"\n    - 当前积分: {user.getScore()}"
                    user.save()
                    await qiandao_eventer.finish(msg)
            elif morningd_time.year < now.year:
                if userid in score_plus.keys():
                    msg += "\n签到 v1.0.0"
                    msg += "\n    - 签到中..."
                    msg += "\n    - 签到成功!"
                    useridr: int | None = score_plus.get(userid)
                    score = random.randint(1,100) * useridr
                    msg += f"\n    - 获得 {score} 积分"
                    userid = event.get_user_id()
                    user = User(userid)
                    user.addScore(score * score_plus.get(userid))
                    msg += f"\n    - 当前积分: {user.getScore()}"
                    morningd.update({userid:dt.datetime.now().__str__()})
                    open("./todayMorningd.json","w+",encoding="utf-8").write(str(morningd))
                    user.save()
                    await qiandao_eventer.finish(msg)
                else:
                    msg += "\n签到 v1.0.0"
                    msg += "\n    - 签到中..."
                    msg += "\n    - 签到成功!"
                    score = random.randint(1,100)
                    msg += f"\n    - 获得 {score} 积分"
                    userid = event.get_user_id()
                    user = User(userid)
                    user.addScore(score)
                    morningd.update({userid:dt.datetime.now().__str__()})
                    open("./todayMorningd.json","w+",encoding="utf-8").write(str(morningd))
                    msg += f"\n    - 当前积分: {user.getScore()}"
                    user.save()
                    await qiandao_eventer.finish(msg)
            else:
                msg += "\n签到 v1.0.0"
                msg += "\n    - 您今天已经签到过了，请明天再来。"
                await qiandao_eventer.finish(msg)
        else:
            if userid in score_plus.keys():
                msg += "\n签到 v1.0.0"
                msg += "\n    - 签到中..."
                msg += "\n    - 签到成功!"
                useridr: int | None = score_plus.get(userid)
                score = random.randint(1,100) * useridr
                msg += f"\n    - 获得 {score} 积分"
                userid = event.get_user_id()
                user = User(userid)
                user.addScore(score * score_plus.get(userid))
                msg += f"\n    - 当前积分: {user.getScore()}"
                morningd.update({userid:dt.datetime.now().__str__()})
                open("./todayMorningd.json","w+",encoding="utf-8").write(str(morningd))
                user.save()
                await qiandao_eventer.finish(msg)
            else:
                msg += "\n签到 v1.0.0"
                msg += "\n    - 签到中..."
                msg += "\n    - 签到成功!"
                score = random.randint(1,100)
                msg += f"\n    - 获得 {score} 积分"
                userid = event.get_user_id()
                user = User(userid)
                user.addScore(score)
                morningd.update({userid:dt.datetime.now().__str__()})
                open("./todayMorningd.json","w+",encoding="utf-8").write(str(morningd))
                msg += f"\n    - 当前积分: {user.getScore()}"
                user.save()
                await qiandao_eventer.finish(msg)
    else:
        msg += "\n签到 v1.0.0"
        msg += "\n    - 您已被禁用签到，请联系管理员。"
        await qiandao_eventer.finish(msg)


info_eventer = on_command("info", aliases={"积分", "积分功能"}, priority=5)

@info_eventer.handle()
async def _(event:GroupMessageEvent | PrivateMessageEvent,arg: Message = CommandArg()):
    user = User(event.get_user_id())
    if not user.isbanned():
        msg = ""
        msg += "\n用户面板 User Panel"
        
        userid = event.get_user_id()
        user = User(userid)
        
        msg += f"\n    - 用户ID(即QQ号): {user.getId()}"
        
        msg += f"\n    - 用户积分: {user.getScore()}"
        await qiandao_eventer.finish(msg)
    else:
        msg = ""
        msg += "\n用户面板 User Panel"
        
        userid = event.get_user_id()
        user = User(userid)
        
        msg += "\n    - 您已被禁用 USER PANEL 功能，请联系管理员。"
        await qiandao_eventer.finish(msg)
    
setinfo_eventer = on_command("setinfo", aliases={"设置信息", "信息设置"}, permission=SUPERUSER, priority=5)

@setinfo_eventer.handle()
async def _(event:GroupMessageEvent | PrivateMessageEvent,arg: Message = CommandArg()):
    msg = ""
    if arg.extract_plain_text().split(" ")[0] == "":
        
        msg += "\n设置用户信息 Set User Info"
        
        msg += "\n    - 执行 *setinfo [userid] [action] 以设置"
    else:
        userid = arg.extract_plain_text().split(" ")[0]
        user = User(userid)
        if arg.extract_plain_text().split(" ")[1] == "name":
            user.resetName(arg.extract_plain_text().split(" ")[2])
            msg += f"\n    - 用户名已设置为 {user.getName()}"
        elif arg.extract_plain_text().split(" ")[1] == "id":
            user.rebindId(arg.extract_plain_text().split(" ")[2])
            msg += f"\n    - 用户ID已设置为 {user.getId()}"
        elif arg.extract_plain_text().split(" ")[1] == "score":
            user.setscore(int(arg.extract_plain_text().split(" ")[2]))
            msg += f"\n    - 用户积分已设置为 {user.getScore()}"
        else:
            msg += "\n    - 无效的指令"
        user.save()
    await qiandao_eventer.finish(msg)

buy_eventer = on_command("buy", aliases={"购买", "购买功能"}, priority=5)

@buy_eventer.handle()
async def _(event:GroupMessageEvent | PrivateMessageEvent,arg: Message = CommandArg()):
    msg = ""
    user = User(event.get_user_id())
    if not user.isbanned():
        if arg.extract_plain_text().split(" ")[0] == "":
            name:str
            money:str
            msg += f"\nToolsbot 小商店"
            
            msg += f"\n商品列表："
            
            for name,money in eval(open("./buyList.json","r",encoding="utf-8").read()).items():
                msg += f"\n    - 商品名: {name}"
                
                msg += f"\n    - 商品价格: {money}"
            msg += f"\n    - 输入 *buy [商品名] [数量 = 1] 以购买"
        elif arg.extract_plain_text().split(" ")[0] != "use":
            name = arg.extract_plain_text().split(" ")[0]
            try:
                const = arg.extract_plain_text().split(" ")[1]
            except:
                const = ""
            
            if const == "":
                const = 1
            else:
                const = int(const)
                
            money = eval(open("./buyList.json","r",encoding="utf-8").read())[name]
            if money == "INFINITY":
                await buy_eventer.finish("    - 该商品为无限价值商品，无法购买")

            money_int = int(money)

            userid = event.get_user_id()
            user = User(userid)
            if user.getScore() >= money_int and money_int > 0:
                user.addScore(- (money_int * const))
            
                for i in range(const):
                    user.buyItem(name)

                msg += f"\n    - 购买成功 数量 {const}"
                user.save()
                msg += f"\n    - 当前用户积分: {user.getScore()}"
                
                msg += f"\n    - 扣除积分：{money}"
                msg += f"\n    - 使用 *buy use {name} {const} (可不填，若你只买了一个) 以使用"
            else:
                msg += "\n     - 购买失败"
                msg += "\n     - 你他妈没钱还来买东西？"
        else:
            name = arg.extract_plain_text().split(" ")[1]
            
            try:
                const = int(arg.extract_plain_text().split(" ") [2])
            except:
                const = 1
                
            userid = event.get_user_id()
            user = User(userid)
            if not name in user.getBuied():
                msg += f"\n    - 用户没有该物品"
            else:
                for i in range(const):
                    msg += "\n" + user.useItem(name)
                msg += f"\n    - 物品已使用"
                msg += f"\n    - 当前用户积分: {user.getScore()}"
            user.save()
        await qiandao_eventer.finish(msg)
    else:
        await buy_eventer.finish("ToolsBot小商店\n    - 您的账户已被封禁。")

usecode_eventer = on_command("usecode", aliases={"使用兑换码", "兑换"}, priority=5)

@usecode_eventer.handle()
async def _(event:GroupMessageEvent | PrivateMessageEvent,msgr: Message = CommandArg()):
    msg = ""
    user = User(event.get_user_id())
    if not user.isbanned():
        if msgr.extract_plain_text().split(" ")[0] == "":
            msg += f"\nToolsbot 兑换码兑换"
            msg += f"\n    - 输入 *usecode [兑换码] 以兑换"
        else:
            msg += f"\nToolsbot 兑换码兑换"
            present_code_dict = eval(open("./codes.json","r").read())
            present_codes = list(present_code_dict.keys())
            code = msgr.extract_plain_text().split(" ")[0]
            if code in present_codes:
                userid = event.get_user_id()
                user = User(userid)
                user.addScore(int(present_code_dict[code]))
                user.save()
                msg += "\n    - 兑换成功"
                msg += f"\n    - 当前用户积分: {user.getScore()}"
                msg += "\n    - 兑换码: " + code
                msg += "\n    - 兑换积分: " + present_code_dict[code]
                del present_code_dict [code]
                open("./codes.json","w+").write(str(present_code_dict))
                await usecode_eventer.finish(msg)
            else:
                msg += "\n    - 兑换失败: 兑换码无效"
                msg += "\n    - 兑换码: " + code.replace("\nToolsBot","")
                msg += "\n    - 兑换积分: 0"
                await usecode_eventer.finish(msg)
    else:
        msg += "\nToolsbot 兑换码兑换"
        msg += "\n    - 您的账户已被封禁。\n"
        await usecode_eventer.finish(msg)

def At(data: str):
    """
    检测at了谁，返回[qq, qq, qq,...]
    包含全体成员直接返回['all']
    如果没有at任何人，返回[]
    :param data: event.json
    :return: list
    """
    try:
        qq_list: list = []
        data_: dict = json.loads(data)
        for msg in data_["message"]:
            if msg["type"] == "at":
                if 'all' not in str(msg):
                    qq_list.append(msg["data"]["qq"])
                else:
                    return ['all']
        return qq_list
    except KeyError:
        return []
    
pay_eventer = on_command("pay", aliases={"交易", "向对方转钱"}, priority=5)

@pay_eventer.handle()
async def _(bot:Bot,event:GroupMessageEvent | PrivateMessageEvent,args: Message = CommandArg()):
    msg = ""
    text = args.extract_plain_text()
    user = User(event.get_user_id())
    if not user.isbanned():
        if text == "":
            msg += f"\nToolsbot 交易"
            msg += f"\n    - 输入 *pay [@对方] [金额] 以交易"
        else:
            msg += f"\nToolsbot 交易"
            userid = event.get_user_id()
            user = User(userid)
            try:
                toUserId = At(event.json()) [0]
                toUser = User(toUserId)
                if toUser == User("1792443798"):
                    await pay_eventer.finish("你他妈自己给自己付钱？")
                if userid == toUserId :
                    await pay_eventer.finish("你他妈自己给自己付钱？")
                money = text.split(" ")[1]
                if user.id == "3085132801":
                    msg += "\n    - 交易失败: 您的账号已被封禁"
                    await pay_eventer.finish(msg)
            except Exception:
                await pay_eventer.finish("他妈的你语法错了，不要用 qq 号，用 @! at!")

            if user.getScore() >= int(money) and int(money) > 0:
                user.addScore(-int(money))
                user.save()
                toUser.addScore(int(money))
                toUser.save()
                msg += "\n    - 交易成功"
                msg += f"\n    - 当前用户积分: {user.getScore()}"
                msg += f"\n    - 对方用户积分: {toUser.getScore()}"
            else:
                msg += "\n    - 交易失败: 积分不足 / 你给对方转负数"
                msg += f"\n    - 当前用户积分: {user.getScore()}"
                msg += f"\n    - 对方用户积分: {toUser.getScore()}"
        await pay_eventer.finish(msg)
    else:
        msg += "Toolsbot交易\n    - 交易失败: 您的账号已被封禁"
        await pay_eventer.finish(msg)

echo_eventer = on_command("echo", aliases={"说"}, priority=5)

@echo_eventer.handle()
async def _(bot:Bot,event:GroupMessageEvent | PrivateMessageEvent,args: Message = CommandArg()):
    msg = ""
    text = args.extract_plain_text()
    user = User(event.get_user_id())
    if not user.isbanned():
        await echo_eventer.finish(text)
    else:
        await echo_eventer.finish("ToolsBot ECHO\b   - 乐，没想到吧，你被封禁了连 echo 都用不了")
        
wasteTaker_event = on_command("cleanwaste", aliases={"捡垃圾"}, priority=5)

@wasteTaker_event.handle()
async def _ (bot: Bot, event: GroupMessageEvent | PrivateMessageEvent, args: Message = CommandArg()):
    wastes = ["普通", "普通","普通","普通","垃圾","垃圾","垃圾","垃圾","垃圾","垃圾","垃圾","垃圾","中级", "高级", "黄金", "钻石"]
    
    waste = [
        1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 10, 100, 10000
    ]
    
    __waste =  wastes.index(random.choice(wastes))
    waste_name = wastes [__waste]
    waste_money = waste [__waste]
    
    msg = "ToolsBot - 捡垃圾"
    msg += "\n    - 你没钱了，你来捡垃圾。"
    msg += f"\n   - 垃圾属性："
    msg += f"\n       类型： {waste_name}"
    msg += f"\n       赚了： {waste_money}"
    
    user = User(event.get_user_id())
    
    if not user.isbanned():
        user.addScore (waste_money)
        await wasteTaker_event.finish(msg)
    else:
        await wasteTaker_event.finish("ToolsBot - 捡垃圾\n    - 你被城管抓住了，你别想捡垃圾了。")