<div align="center">

![Epic Games](https://raw.githubusercontent.com/ilhmtfmlt2/Epic-Games/main/img/Epic.jpg)

# Epic-Games

![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/ilhmtfmlt2/Epic-Games?label=version)
![Python](https://img.shields.io/badge/Python-3.9%7C3.8-blue)
![GitHub](https://img.shields.io/github/license/ilhmtfmlt2/Epic-Games)
[![GitHub Issues](https://img.shields.io/github/issues/ilhmtfmlt2/Epic-Games?style=flat-square)](https://github.com/ilhmtfmlt2/Epic-Games/issues)
[![GitHub Forks](https://img.shields.io/github/forks/ilhmtfmlt2/Epic-Games?style=flat-square)](https://github.com/ilhmtfmlt2/Epic-Games/network)
[![GitHub Stars](https://img.shields.io/github/stars/ilhmtfmlt2/Epic-Games?style=flat-square)](https://github.com/ilhmtfmlt2/Epic-Games/stargazers)

</div>

---

# Epic-Games

🚀 **Epic-Games** 用于自动获取 Epic Games 商店的每周限免游戏信息，邮件推送给。获取本周和下周即将限免的游戏。

## ✨ 功能

- **自动获取限免游戏信息**：包括标题、发行商、原价、限免时间等。
- **精美 HTML 邮件生成**：支持游戏图片展示和领取链接跳转。
- **本周限免/下周限免游戏分类显示**。
- 一键发送邮件至多个收件人。

## 📦 使用方法

### 1. 安装依赖

确保安装 Python 3.8+，并运行以下命令安装依赖：
```bash
pip install requests
```

### 2. 配置 `config.json`

创建 `config.json` 文件，并填写邮件服务器和接收者信息：
```json
{
  "email": {
    "smtp_server": "smtp.example.com",
    "port": 465,
    "sender_email": "your_email@example.com",
    "password": "your_email_password",
    "receiver_email": [
      "receiver1@example.com",
      "receiver2@example.com"
    ]
  }
}

```

### 3. 运行脚本

执行以下命令获取限免游戏并发送邮件：
```bash
python main.py
```

## 🛠️ 主要文件

- **`main.py`**: 核心脚本，包含限免游戏获取、HTML生成和邮件发送逻辑。
- **`config.json`**: 配置文件，用于设置邮件服务信息。

## 🎯 工作流程

1. 调用 **Epic Games API** 获取限免游戏数据。
2. 格式化游戏信息（包括时间、图片、描述等）。
3. 生成带有领取链接的 HTML 邮件。
4. 通过 SMTP 服务发送邮件。

## 🎨 示例邮件预览

![邮件预览](https://raw.githubusercontent.com/ilhmtfmlt2/Epic-Games/refs/heads/main/img/main.jpg)

## 🔧 自定义

- 修改 HTML 邮件样式（`format_email_content` 函数）。
- 根据需要调整收件人列表和 Epic API 的国家/地区参数。

## 📌 注意事项

- 确保启用了 SMTP 服务，建议使用应用专用密码以保证安全。
- 由于 API 响应结构可能会变化，请定期更新代码。

---

<div align="center">

## 🌟 Stargazers

[![Stargazers repo roster for @ilhmtfmlt2/Epic-Games](https://reporoster.com/stars/ilhmtfmlt2/Epic-Games)](https://github.com/ilhmtfmlt2/Epic-Games/stargazers)

![Stats](https://github-readme-stats.vercel.app/api?username=ilhmtfmlt2&show_icons=true&theme=merko)

</div>

---

## 📄 许可证

项目基于 [MIT License](LICENSE) 开源，欢迎自由使用和贡献！

💌 如果有任何问题或建议，请提交 [Issues](https://github.com/ilhmtfmlt2/Epic-Games/issues) 或贡献代码。
```

### 更新内容
1. 优化标题与段落之间的层次。
2. 为链接、徽标和描述添加了统一格式。
3. 将示例代码和输出预览做了精简。
4. 包括了 Stargazers 和统计卡片。
5. 去掉了冗余信息。
