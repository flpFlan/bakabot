BakaBot
==========
前置需求
----------
- python >=3.11
- poetry
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

命令行里运行
```
poetry install
```

配置
-----------
在[config.ini](config.ini)里修改参数

```ini
[Bot]
# bot昵称(与qq昵称无关，仅作代号使用)
name = BAKA
# QQ号
qq = 123456789
# bot所有者，最好填你自己的QQ
superuser = 987654321
# bot管理员，可以填多位，但必须填上你自己
administrators = [987654321]

[Bot.Adapter]
# 与go-cqhttp配置相同, 注意使用正向websocket通信
endpoint = localhost:2333 
```

运行
-----------
1. 首先运行 [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)

2. 命令行里运行

```shell
poetry run python ./start_bot.py
```

Go-CQHTTP
==========
config.yml
----------
配置参考:

```
# go-cqhttp 默认配置文件

account: # 账号相关
  uin: 0 # QQ账号
  password: '' # 密码为空时使用扫码登录
  encrypt: false  # 是否开启密码加密
  status: 0      # 在线状态 请参考 https://docs.go-cqhttp.org/guide/config.html#在线状态
  relogin: # 重连设置
    delay: 3   # 首次重连延迟, 单位秒
    interval: 3   # 重连间隔
    max-times: 0  # 最大重连次数, 0为无限制

  # 是否使用服务器下发的新地址进行重连
  # 注意, 此设置可能导致在海外服务器上连接情况更差
  use-sso-address: true
  # 是否允许发送临时会话消息
  allow-temp-session: false

heartbeat:
  # 心跳频率, 单位秒
  # -1 为关闭心跳
  interval: 5

message:
  # 上报数据类型
  # 可选: string,array
  post-format: string
  # 是否忽略无效的CQ码, 如果为假将原样发送
  ignore-invalid-cqcode: false
  # 是否强制分片发送消息
  # 分片发送将会带来更快的速度
  # 但是兼容性会有些问题
  force-fragment: false
  # 是否将url分片发送
  fix-url: false
  # 下载图片等请求网络代理
  proxy-rewrite: ''
  # 是否上报自身消息
  report-self-message: false
  # 移除服务端的Reply附带的At
  remove-reply-at: false
  # 为Reply附加更多信息
  extra-reply-data: false
  # 跳过 Mime 扫描, 忽略错误数据
  skip-mime-scan: false
  # 是否自动转换 WebP 图片
  convert-webp-image: false

output:
  # 日志等级 trace,debug,info,warn,error
  log-level: warn
  # 日志时效 单位天. 超过这个时间之前的日志将会被自动删除. 设置为 0 表示永久保留.
  log-aging: 15
  # 是否在每次启动时强制创建全新的文件储存日志. 为 false 的情况下将会在上次启动时创建的日志文件续写
  log-force-new: true
  # 是否启用日志颜色
  log-colorful: true
  # 是否启用 DEBUG
  debug: false # 开启调试模式

# 默认中间件锚点
default-middlewares: &default
  # 访问密钥, 强烈推荐在公网的服务器设置
  access-token: ''
  # 事件过滤器文件目录
  filter: ''
  # API限速设置
  # 该设置为全局生效
  # 原 cqhttp 虽然启用了 rate_limit 后缀, 但是基本没插件适配
  # 目前该限速设置为令牌桶算法, 请参考:
  # https://baike.baidu.com/item/%E4%BB%A4%E7%89%8C%E6%A1%B6%E7%AE%97%E6%B3%95/6597000?fr=aladdin
  rate-limit:
    enabled: false # 是否启用限速
    frequency: 1  # 令牌回复频率, 单位秒
    bucket: 1     # 令牌桶大小

database: # 数据库相关设置
  leveldb:
    # 是否启用内置leveldb数据库
    # 启用将会增加10-20MB的内存占用和一定的磁盘空间
    # 关闭将无法使用 撤回 回复 get_msg 等上下文相关功能
    enable: true
  sqlite3:
    # 是否启用内置sqlite3数据库
    # 启用将会增加一定的内存占用和一定的磁盘空间
    # 关闭将无法使用 撤回 回复 get_msg 等上下文相关功能
    enable: false
    cachettl: 3600000000000 # 1h

# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器
  # 正向WS设置
  - ws:
      # 正向WS服务器监听地址
      address: 0.0.0.0:2333
      middlewares:
        <<: *default # 引用默认中间件
```

主要功能
========

Services
--------

- [x] 点歌
- [x] 油库里
- [x] B站封面获取
- [x] 随机东方
- [x] 随机图片
- [x] 搜图
- [x] 读懂世界
- [x] 青年大学习截图生成
- [x] pid
- [x] emoji合成
- [x] bv号转换
- [x] av号转换
- [x] 每日运势
- [x] 每日CP
- [ ] 查成分
- [ ] 翻译
- [x] [发电](https://github.com/xipesoy/zhenxun_plugin_meiriyiju)
- [ ] 查询thb
- [x] 选择...还是...
- [ ] 迷你英文
- [x] [疯狂星期四文案生成](https://github.com/whitescent/KFC-Crazy-Thursday)
- [x] 掷骰
- [ ] 聊天
- [x] 入群欢迎
- [x] 复读

Games
--------
用例: /game + 关键词:

```
/game Akinator
```

- [x] 俄罗斯轮盘
- [ ] 五子棋
- [ ] 扫雷
- [x] [Akinator](https://github.com/Infiniticity/akinator.py)

扩展
--------
用例

```python
from services.base import Service, ServiceBehavior, OnEvent
from cqhttp.events.message import GroupMessage
from cqhttp.api.message.SendGroupMsg import SendGroupMsg

class Foo(Service):
  pass

class Bar(ServiceBehavior[Foo]):

  @OnEvent[GroupMessage.add_listener]
  async def bar(evt:GroupMessage):
    if evt.message == "Hello"
      await SendGroupMsg(evt.group_id, "World!").do()
      # 可选的非阻塞形式:
      # SendGroupMsg(evt.group_id, "World!").forget()
```

具体可参考services目录下任一service