from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import *
from nonebot.permission import SUPERUSER
import nonebot,random
from time import sleep as wait
from random import uniform as wrd
import os

class Database:
    def __init__(self, db_name, id):
        self.db_name = db_name
        self.position = "./database"
        self.id = id
    
    def write(self, data:str):
        open(self.position + "/" + self.id,"w").write(data)
    
    def read(self) -> str | None:
        if os.path.exists(self.position + "/" + self.id):
            return open(self.position + "/" + self.id,"r").read()
        else:
            return None
    
    def delete(self):
        if os.path.exists(self.position + "/" + self.id):
            os.remove(self.position + "/" + self.id)
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
        if (self.objectDatabase.find(id)):
            self.load(id)
        else:
            self.objectDatabase.write(str(self))
    
    def load(self,userid:str):
        self.objectDatabase: Database
        self.id = self.objectDatabase.read().split(":")[0]
        self.name = self.objectDatabase.read().split(":")[1].split(",")[0]
        self.score = int(self.objectDatabase.read().split(":")[1].split(",")[1])
        self.buied = eval(self.objectDatabase.read().split(":")[1].split(",")[2])

    def addScore(self,score:int):
        self.score += score
    
    def getScore(self):
        return self.score
    
    def getName(self):
        return self.name
    
    def getId(self):
        return self.id
    
    def resetName(self,name:str):
        self.name = name
    
    def rebindId(self,id:str):
        self.id = id
    
    def save(self):
        Database("maindb",self.id).write(str(self))
    
    def setscore(self,score:int):
        self.score = score
    
    def buyItem(self,item:str):
        self.buied.append(item)
    
    def useItem(self,item:str):
        howcando:dict = eval(open("./howCanDo.json","r",encoding="utf-8").read())
        for name in self.buied:
            for namer,do in howcando.items():
                if name == namer:
                    return self.do(do)
        return "    - 无效的物品"
    
    def do(self,action:str) -> str:
        if "morning.score.x" in action:
            add_x = int(action.replace("morning.score.x",""))
            todayScorePlus:dict = eval(open("./todayScorePlus.json","r",encoding="utf-8").read())
            todayScorePlus.update({self.id:add_x})
            open("./todayScorePlus.json","w",encoding="utf-8").write(str(todayScorePlus))
            return "    - 使用成功，如果您今天没有 /morning，使用 /morning 即可获得积分。"
        elif "guess.money.try" in action:
            cp_money = random.randint(10,10000000)
            if cp_money == 10:
                self.addScore(100000)
                return "    - 恭喜你，中奖了！获得 10,0000 积分"
            else:
                anwei = random.randint(0,5)
                self.addScore(anwei)
                return f"    - 很遗憾，没有中奖。但获得 {anwei} 积分"

    def getBuied(self):
        return self.buied
    
    def __str__(self) -> str:
        return f"{self.id}:{self.name},{self.score},{self.buied}"
    
qiandao_eventer = on_command("morning", aliases={"签到", "签到功能"}, priority=5)

@qiandao_eventer.handle()
async def _(event:GroupMessageEvent | PrivateMessageEvent,msg: Message = CommandArg()):
    morningd:dict = eval(open("./todayMorningd.json","r",encoding="utf-8").read())
    score_plus:dict = eval(open("./todayScorePlus.json","r",encoding="utf-8").read())
    userid = event.get_user_id()
    if userid in morningd.keys():
        msg += "\n签到 v1.0.0"
        msg += "\n    - 您今天已经签到过了，请明天再来。"
        await qiandao_eventer.finish(msg)
    else:
        if userid in morningd.keys():
            msg += "\n签到 v1.0.0"
            msg += "\n    - 签到中..."
            msg += "\n    - 签到成功!"
            score = random.randint(1,100) * score_plus.get(userid)
            msg += f"\n    - 获得 {score} 积分"
            userid = event.get_user_id()
            user = User(userid)
            user.addScore(score * score_plus.get(userid))
            msg += f"\n    - 当前积分: {user.getScore()}"
            morningd.update({userid:True})
            open("./todayMorningd.json","w",encoding="utf-8").write(str(morningd))
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
            morningd.update({userid:True})
            open("./todayMorningd.json","w",encoding="utf-8").write(str(morningd))
            msg += f"\n    - 当前积分: {user.getScore()}"
            user.save()
            await qiandao_eventer.finish(msg)


info_eventer = on_command("info", aliases={"积分", "积分功能"}, priority=5)

@info_eventer.handle()
async def _(event:GroupMessageEvent | PrivateMessageEvent,msg: Message = CommandArg()):
    
    msg += "\n用户面板 User Panel"
    
    userid = event.get_user_id()
    user = User(userid)
    
    msg += f"\n    - 用户ID(即QQ号): {user.getId()}"
    
    msg += f"\n    - 用户积分: {user.getScore()}"
    await qiandao_eventer.finish(msg)
    
setinfo_eventer = on_command("setinfo", aliases={"设置信息", "信息设置"}, permission=SUPERUSER, priority=5)

@setinfo_eventer.handle()
async def _(event:GroupMessageEvent | PrivateMessageEvent,msg: Message = CommandArg()):
    if msg.extract_plain_text().split(" ")[0] == "":
        
        msg += "\n设置用户信息 Set User Info"
        
        msg += "\n    - 执行 *setinfo [userid] [action] 以设置"
    else:
        userid = msg.extract_plain_text().split(" ")[0]
        user = User(userid)
        if msg.extract_plain_text().split(" ")[1] == "name":
            user.resetName(msg.extract_plain_text().split(" ")[2])
            msg += f"\n    - 用户名已设置为 {user.getName()}"
        elif msg.extract_plain_text().split(" ")[1] == "id":
            user.rebindId(msg.extract_plain_text().split(" ")[2])
            msg += f"\n    - 用户ID已设置为 {user.getId()}"
        elif msg.extract_plain_text().split(" ")[1] == "score":
            user.setscore(int(msg.extract_plain_text().split(" ")[2]))
            msg += f"\n    - 用户积分已设置为 {user.getScore()}"
        else:
            msg += "\n    - 无效的指令"
        user.save()
    await qiandao_eventer.finish(msg)

buy_eventer = on_command("buy", aliases={"购买", "购买功能"}, priority=5)

@buy_eventer.handle()
async def _(event:GroupMessageEvent | PrivateMessageEvent,msg: Message = CommandArg()):
    if msg.extract_plain_text().split(" ")[0] == "":
        name:str
        money:str
        msg += f"\nToolsbot 小商店"
        
        msg += f"\n商品列表："
        
        for name,money in eval(open("./buyList.json","r",encoding="utf-8").read()).items():
            msg += f"\n    - 商品名: {name}"
            
            msg += f"\n    - 商品价格: {money}"
        msg += f"\n    - 输入 *buy [商品名] 以购买"
    else:
        name = msg.extract_plain_text().split(" ")[0]
        money = open("./buyList.json","r",encoding="utf-8").read()[name]
        if money == "INFINITY":
            await buy_eventer.finish("    - 该商品为无限价值商品，无法购买")

        money_int = int(money)

        userid = event.get_user_id()
        user = User(userid)
        if user.getScore() >= money_int:
            user.addScore(-money_int)
        
        user.buyItem(name)

        msg += f"\n    - 购买成功"
        user.save()
        msg += f"\n    - 当前用户积分: {user.getScore()}"
        
        msg += f"\n    - 扣除积分：{money}"
    await qiandao_eventer.finish(msg)
