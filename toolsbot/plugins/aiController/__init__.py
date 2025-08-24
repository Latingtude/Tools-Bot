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

ai_eventer = on_command("ai", aliases={"人工智能"}, priority=5)

@ai_eventer.handle()
async def _(event: GroupMessageEvent, arg: Message = CommandArg()):
    # API Key, 硅基流动
    api_key = "sk-quhtfffmcbqsmlfsrpjgpowkkhprnkrqrpwqnyqzjybfuxzn"
    
    user = dc.User(event.get_user_id())
    
    if not user.isbanned():
        text = arg.extract_plain_text()
        msg = ""
        msg += "ToolsBot AI"
        if text == "":
            await ai_eventer.finish("ToolsBot AI\n    - 使用 *ai [内容] 来进行聊天。(注：不会保留上下文)")
            
        payload = {
            "model": "Qwen/Qwen3-8B",
            "messages": [
                {
                    "role": "system",
                    "content": "你是一个名叫 ToolsBot 的 Bot。现在是 2025 年。接下来用户会给你发送消息，请直接发送结果并使用简洁的语言。若对方向你询问成人内容，请直接输出 18Disabled。若不是类似内容，请不要想这些内容。"
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        }
        
        headers = {
            "Authorization": "Bearer " + api_key,
            "Content-Type": "application/json"
        }
        
        await ai_eventer.send("ToolsBot AI 提示：\n    - 请稍等，AI 正在生成")
        
        response = requests.post("https://api.siliconflow.cn/v1/chat/completions", json=payload, headers=headers).content
        # 获取返回的内容
        js_resp = json.loads(response)
        
        # choices
        choices = js_resp.get("choices")
        
        # message
        messag_ = choices [0].get("message")
        
        # content
        ctnt = messag_.get("content").replace("\n", "")
        
        # reasoning_content
        rea_ctnt = messag_.get("reasoning_content").replace("\n", "")

        # usage
        usage = js_resp.get("usage")
        
        # total token
        total_token = usage.get("total_tokens")

        msg = f"""ToolsBot AI
        - 模型:
            Qwen\\Qwen3-8B
        - 思考内容
            {rea_ctnt}
        - 回复内容：
            {ctnt}
        - 此次扣除金额：
            {total_token}
    """
        
        if ctnt == "18Disabled":
            msg = f"""ToolsBot AI
        - 模型：
            Qwen\\Qwen3-8B
        - 提示：
            请勿询问此种内容。
        """

        if user.getScore() < int(total_token):
            msg = f"""ToolsBot AI
        - 模型：
            Qwen\\Qwen3-8B
        - 提示：
            您的积分不够。目前已追加欠款。请早日还清。
            """
            
        user.addScore(- (int(total_token) * 1))
        user.save()
        await ai_eventer.finish(msg)
        
    else:
        await ai_eventer.finish("ToolsBot AI\n    - 您的账号已被封禁。无法使用该功能。")   