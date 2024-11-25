# 钱包地址代币价格异动监测服务

## 背景

有的meme代币，买入之后就归零了，但是某个时候可能会突然价值暴涨，如果不能及时查看钱包可能会错失第二次高价卖出的机会，所以我们需要开发一个平台，通过一定方式扫描钱包地址里面持有的代币价格异动。

## 功能设计

- 输入：
  - 钱包地址
  - 监测规则
- 输出：
  - 邮件提醒
  - telegram bot提醒
  - 飞书bot提醒

## 监测扫描规则

- 当前代币价格较上次价格涨幅超过100%则记录并发生提醒
- 每隔15分钟进行一次价格扫描 如有异动则3分钟进行一次价格扫描
- 只扫描钱包持有的代币合约地址对应价格

## 技术栈

- 使用python
- 使用jup api

## 项目架构

```
tree
├── docs/ # 项目文档
├── frontend/ # 前端代码
│ ├── src/
│ ├── public/
│ └── package.json
├── backend/ # 后端代码
│ ├── src/
│ ├── tests/
│ └── requirements.txt
└── README.md
```


## 获取 Telegram Chat ID

1. 首先在 Telegram 中搜索并添加您的机器人
2. 向机器人发送一条消息（比如 `/start`）
3. 执行以下命令获取 chat_id：

```bash
# 安装 jq 工具
yum install -y jq

# 获取 chat_id（替换 YOUR_BOT_TOKEN 为您的机器人 token）
curl https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates | jq '.result[0].message.chat.id'
```

4. 将获取到的 chat_id 填入 `.env` 文件的 `TELEGRAM_CHAT_ID` 字段
```

这部分内容建议插入到 `VPSREADME.md` 的这个位置：

````58:59:VPSREADME.md
# 创建环境变量文件
```



这样可以在创建环境变量文件之前，先指导用户如何获取正确的 chat_id。
