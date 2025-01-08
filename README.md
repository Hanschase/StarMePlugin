# Starme

<!--
## 插件开发者详阅

### 开始

此仓库是 LangBot 插件模板，您可以直接在 GitHub 仓库中点击右上角的 "Use this template" 以创建你的插件。  
接下来按照以下步骤修改模板代码：

#### 修改模板代码

- 修改此文档顶部插件名称信息
- 将此文档下方的`<插件发布仓库地址>`改为你的插件在 GitHub· 上的地址
- 补充下方的`使用`章节内容
- 修改`main.py`中的`@register`中的插件 名称、描述、版本、作者 等信息
- 修改`main.py`中的`MyPlugin`类名为你的插件类名
- 将插件所需依赖库写到`requirements.txt`中
- 根据[插件开发教程](https://docs.langbot.app/plugin/dev/tutor.html)编写插件代码
- 删除 README.md 中的注释内容


#### 发布插件

推荐将插件上传到 GitHub 代码仓库，以便用户通过下方方式安装。   
欢迎[提issue](https://github.com/RockChinQ/LangBot/issues/new?assignees=&labels=%E7%8B%AC%E7%AB%8B%E6%8F%92%E4%BB%B6&projects=&template=submit-plugin.yml&title=%5BPlugin%5D%3A+%E8%AF%B7%E6%B1%82%E7%99%BB%E8%AE%B0%E6%96%B0%E6%8F%92%E4%BB%B6)，将您的插件提交到[插件列表](https://github.com/stars/RockChinQ/lists/qchatgpt-%E6%8F%92%E4%BB%B6)

下方是给用户看的内容，按需修改
-->

## 安装

配置完成 [LangBot](https://github.com/RockChinQ/LangBot) 主程序后使用管理员账号向机器人发送命令即可安装：

```
!plugin get (https://github.com/Hanschase/StarMePlugin)
```
或查看详细的[插件安装说明](https://docs.langbot.app/plugin/plugin-intro.html#%E6%8F%92%E4%BB%B6%E7%94%A8%E6%B3%95)

## 使用
注：目前仅限在群里使用！<br>
1.通过!starme注册点赞 <br>
2.通过!letstar开始点赞任务（每次重启bot都需要的指令） <br>
3.通过!cancelstar取消注册 <br>

## 一些碎碎念
目前是固定的每天上午十点进行点赞，如果有人又需要可以催我更下指令更改时间=- =，并且只能运用于aiocqhttp的消息平台 <br>

Q:为啥叫starme？
A:因为我觉得比send like好听

Q:为什么要通过指令启动点赞任务？ <br>
A:问就是项目不支持初始化主动发送消息，等更新了新事件进行修改 <br>

Q:为什么不能通过私聊注册？ <br>
A:太懒了，有人需要的话我再做吧，或者来个大佬直接pr也行啊 <br>

<!-- 插件开发者自行填写插件使用说明 -->
