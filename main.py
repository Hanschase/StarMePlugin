import asyncio
from pkg.plugin.context import register, handler, llm_func, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *  # 导入事件类
import os
import json
import datetime
# 注册插件
@register(name="StarMe", description="自动点赞插件，可通过!starme指令注册，!letstar启动自动任务", version="0.1", author="Hanschase")
class MyPlugin(BasePlugin):

    # 插件加载时触发
    def __init__(self, host: APIHost):
        self.data = {
                    "like_flag": 0,
                    "group_ids":[]
        }
        if not os.path.exists("data/plugins/Starme"):
            os.makedirs("data/plugins/Starme")
        if not os.path.exists("data/plugins/Starme/user.json"):
            with open("data/plugins/Starme/user.json", "w") as f:
                json.dump(self.data, f, indent=4)
        else:
            try:
                with open("data/plugins/Starme/user.json", "r") as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self.ap.logger.error("user.json decoding failed,please check the data/plugins/Starme/user.json or delete it")

    # 异步初始化
    async def initialize(self):
        pass

    # 写入json
    def write_json(self):
        with open("data/plugins/Starme/user.json", "w") as f:
            json.dump(self.data, f, indent=4)

    @handler(GroupCommandSent)
    async def func(self, ctx: EventContext):
        command = ctx.event.command
        group_id = str(ctx.event.launcher_id)
        person_id = str(ctx.event.sender_id)
        if command == "starme":
            ctx.prevent_default()
            if self.check_star(group_id, person_id):
                await ctx.reply([f"您已经在群{group_id}中注册了定时点赞服务，如需取消注册，请发送!cancelstar"])
            else:
                self.apply_star(group_id, person_id)
                await ctx.reply(["成功订阅了点赞服务，我会每天10：00为您点赞"])
                like_counts = 0
                while True:
                    try:
                        await ctx.event.query.adapter.bot.send_like(user_id=int(person_id), times=10)
                        like_counts += 10
                    except Exception as e:
                        break
                await ctx.reply([f"已为您点赞了{like_counts}次"])
        elif command == "cancelstar":
            ctx.prevent_default()
            self.del_star(group_id, person_id)
            await ctx.reply(["已为您取消定时点赞服务！"])
        elif command == "letstar":
            ctx.prevent_default()
            if hasattr(self, 'run_task') and not self.run_task.done():
                await ctx.reply(["定时点赞任务正在执行中，请不要重复发送此命令"])
                return
            try:
                self.run_task = asyncio.create_task(self.run(ctx))
                await ctx.reply(["定时点赞任务开始执行"])
            except Exception as e:
                self.ap.logger.error(f"Error starting task: {e}")


    # 任务执行
    async def run(self,ctx:EventContext):
        while True:
            if self.data["like_flag"] == 1 and self.check_time(10, "<"):
                self.data["like_flag"] = 0
            if self.data["like_flag"] == 0 and self.check_time(10, ">"):
                self.data["like_flag"] = 1
                self.ap.logger.info("开始执行点赞任务")
                for group_id in self.data["group_ids"]:
                    for person_id in self.data[group_id]["person_ids"]:
                        like_counts = 0
                        while True:
                            try:
                                await ctx.event.query.adapter.bot.send_like(user_id=int(person_id), times=10)
                                like_counts += 10
                            except Exception as e:
                                break
                        self.ap.logger.info(f"为在群{group_id}中用户{person_id}点赞了{like_counts}次")
                for group_id in self.data["group_ids"]:
                    await ctx.send_message("group", group_id, ["已经执行了点赞任务！快说谢谢猫猫！"])
            self.write_json()
            await asyncio.sleep(60)

    # 判断时间
    def check_time(self, hour: int, cmp: str):
        now = datetime.datetime.now()
        check_am = now.replace(hour=hour, minute=0, second=0, microsecond=0)
        if cmp == ">":
            if now > check_am:
                return True
            else:
                return False
        elif cmp == "<":
            if now < check_am:
                return True
            else:
                return False

    # 写入注册信息
    def apply_star(self, group_id, person_id):
        if group_id not in self.data["group_ids"]:
            self.data["group_ids"].append(group_id)
            self.data[group_id] = {
                "person_ids": []
            }
        if person_id not in self.data[group_id]["person_ids"]:
            self.data[group_id]["person_ids"].append(person_id)
            try:
                self.write_json()
            except Exception as e:
                raise e
            return True
        else:
            return False

    # 检测是否注册
    def check_star(self, group_id, person_id):
        if group_id in self.data["group_ids"]:
            if person_id in self.data[group_id]["person_ids"]:
                return True
            else:
                return False
        else:
            return False

    # 取消注册
    def del_star(self, group_id, person_id):
        if self.check_star(group_id, person_id):
            self.data[group_id]["person_ids"].remove(person_id)
            if len(self.data[group_id]["person_ids"]) == 0:
                self.data["group_ids"].remove(group_id)
                del self.data[group_id]
            try:
                self.write_json()
            except Exception as e:
                raise e

    # 插件卸载时触发
    def __del__(self):
        pass
