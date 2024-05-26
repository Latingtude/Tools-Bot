from nonebot import on_command
from nonebot.adapters import Message
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11 import *
from nonebot.permission import SUPERUSER
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
        open(f"./database/{self.id}","w+").write(data)
    
    def read(self) -> str:
        if os.path.exists(f"./database/{self.id}"):
            return open(f"./database/{self.id}","r").read()
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
            self.objectDatabase.write(str(self))
    
    def load(self,userid:str): 
        self.objectDatabase: Database
        self.name = self.objectDatabase.read().split(":")[1].split(",")[0]
        self.score = int(self.objectDatabase.read().split(":")[1].split(",")[1])
        self.buied = eval(self.objectDatabase.read().split(":")[1].split(",")[2])
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
        Database("maindb",self.id).write(str(self))
    
    def setscore(self,score:int):
        self.score = score
    
    def buyItem(self,item:str):
        if not self.banned:
            self.buied.append(item)
    
    def useItem(self,item:str):
        howcando:dict = eval(open("./howCanDo.json","r",encoding="utf-8").read())
        for name in self.buied:
            for namer,do in howcando.items():
                if item == namer:
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
    
    def __str__(self) -> str:
        return f"{self.id}:{self.name},{str(self.score)},{self.buied}"