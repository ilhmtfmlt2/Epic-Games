import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from datetime import datetime
import json


def format_date(date_str: str) -> str:
    """将 ISO 8601 时间格式转换为中文格式"""
    try:
        date = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        return date.strftime('%Y年%m月%d日 %H:%M')
    except Exception:
        return date_str


def get_free_games() -> dict:
    """获取 Epic 限免游戏信息，过滤非免费游戏"""
    games = {'free_now': [], 'free_next': []}
    base_store_url = 'https://store.epicgames.com'
    api_url = 'https://store-site-backend-static-ipv4.ak.epicgames.com/freeGamesPromotions?locale=zh-CN&country=CN&allowCountries=CN'
    resp = requests.get(api_url)
    for element in resp.json()['data']['Catalog']['searchStore']['elements']:
        if promotions := element.get('promotions'):
            # 基本游戏信息
            game = {
                'title': element['title'],
                'publisher': element.get('seller', {}).get('name', '未知发行商'),
                'images': element.get('keyImages', []),
                'origin_price': element['price']['totalPrice']['fmtPrice']['originalPrice'],
                'store_url': f"{base_store_url}/p/{element['catalogNs']['mappings'][0]['pageSlug']}" if element['catalogNs']['mappings'] else base_store_url,
            }

            # 当前促销（本周限免）
            if offers := promotions.get('promotionalOffers'):
                discount_price = element['price']['totalPrice']['fmtPrice']['discountPrice']
                # 仅当价格为零时，添加到本周限免
                if discount_price == '0':
                    game.update({
                        'start_date': format_date(offers[0]['promotionalOffers'][0]['startDate']),
                        'end_date': format_date(offers[0]['promotionalOffers'][0]['endDate']),
                    })
                    games['free_now'].append(game)

            # 即将促销（下周限免）
            if offers := promotions.get('upcomingPromotionalOffers'):
                game.update({
                    'start_date': format_date(offers[0]['promotionalOffers'][0]['startDate']),
                    'end_date': format_date(offers[0]['promotionalOffers'][0]['endDate']),
                })
                games['free_next'].append(game)

    return games


def format_email_content(games: dict) -> str:
    """生成 HTML 格式的邮件内容"""
    content = '''
    <html>
    <head>
        <style>
            body { font-family: '微软雅黑', sans-serif; margin: 20px; background-color: #f8f9fa; color: #333; }
            h2 { color: #333; text-align: center; }
            .game { margin-bottom: 20px; padding: 20px; border: 1px solid #ddd; border-radius: 8px; background: #fff; }
            .title { font-size: 20px; font-weight: bold; color: #0056b3; }
            .price { color: #555; font-size: 14px; margin: 10px 0; }
            .publisher { font-size: 14px; color: #777; }
            .time { margin: 10px 0; font-size: 14px; }
            .image { text-align: center; margin: 15px 0; }
            .image img { max-width: 100%; height: auto; border-radius: 8px; }
            .button { text-align: center; margin-top: 10px; }
            .btn { padding: 10px 20px; background-color: #28a745; color: white; text-decoration: none; border-radius: 4px; font-size: 16px; }
            .btn:hover { background-color: #218838; }
            .btn-secondary { background-color: #007bff; }
            .btn-secondary:hover { background-color: #0056b3; }
        </style>
    </head>
    <body>
        <h2>Epic 每周限免游戏</h2>
    '''

    def format_now_game_block(game):
        return f'''
        <div class="game">
            <div class="title">{game['title']}</div>
            <div class="price">原价: {game['origin_price']}</div>
            <div class="time">限免时间:<br>从 {game['start_date']}<br>到 {game['end_date']}</div>
            <div class="publisher">发行商: {game['publisher']}</div>
            <div class="image"><img src="{game['images'][0]['url']}" alt="{game['title']}"></div>
            <div class="button"><a class="btn" href="{game['store_url']}">领取游戏</a></div>
        </div>
        '''

    def format_next_game_block(game):
        return f'''
        <div class="game">
            <div class="title">{game['title']}</div>
            <div class="price">原价: {game['origin_price']}</div>
            <div class="time">限免时间:<br>从 {game['start_date']}<br>到 {game['end_date']}</div>
            <div class="publisher">发行商: {game['publisher']}</div>
            <div class="image"><img src="{game['images'][0]['url']}" alt="{game['title']}"></div>
            <div class="button"><a class="btn btn-secondary" href="{game['store_url']}">了解更多</a></div>
        </div>
        '''

    content += '<h3>本周限免</h3>'
    for game in games['free_now']:
        content += format_now_game_block(game)

    content += '<h3>下周限免</h3>'
    for game in games['free_next']:
        content += format_next_game_block(game)

    content += '</body></html>'
    return content



def load_config(filename: str) -> dict:
    """从本地 JSON 文件加载配置"""
    with open(filename, 'r') as file:
        return json.load(file)


def send_email(subject: str, content: str, email_config: dict):
    """发送邮件"""
    msg = MIMEMultipart()
    msg['From'] = email_config['email']['sender_email']
    msg['To'] = ", ".join(email_config['email']['receiver_email'])
    msg['Subject'] = subject
    msg.attach(MIMEText(content, 'html'))

    try:
        with smtplib.SMTP_SSL(email_config['email']['smtp_server'], email_config['email']['port']) as server:
            server.login(email_config['email']['sender_email'], email_config['email']['password'])
            server.send_message(msg)
        print("邮件发送成功！")
    except Exception as e:
        print(f"邮件发送异常: {e}")


def log_games_info(games: dict):
    """日志输出限免游戏信息"""
    print("\n===== 本周限免游戏 =====")
    for game in games['free_now']:
        print(f"{game['title']}\n原价: {game['origin_price']}\n限免时间:\n从 {game['start_date']}\n到 {game['end_date']}\n发行商: {game['publisher']}\n")
    print("\n===== 下周限免游戏 =====")
    for game in games['free_next']:
        print(f"{game['title']}\n原价: {game['origin_price']}\n限免时间:\n从 {game['start_date']}\n到 {game['end_date']}\n发行商: {game['publisher']}\n")


if __name__ == '__main__':
    # 从 config2.json 加载配置
    config_file = 'config2.json'
    email_config = load_config(config_file)

    # 获取限免游戏数据
    games = get_free_games()

    # 在日志中输出限免游戏信息
    log_games_info(games)

    # 生成邮件内容
    email_content = format_email_content(games)

    # 发送邮件
    send_email("Epic 每周限免游戏更新", email_content, email_config)

