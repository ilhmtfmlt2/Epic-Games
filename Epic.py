import requests

url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?country=CN"

response = requests.get(url)
data = response.json()

# 提取游戏信息
free_games = data["data"]["Catalog"]["searchStore"]["elements"]

# 输出游戏信息
for index, game in enumerate(free_games, start=1):
    game_name = game.get("title", "")
    game_publisher = game["seller"].get("name", "")
    game_price = game["price"]["totalPrice"].get("originalPrice", "")

    if "promotions" in game and game["promotions"] is not None and "upcomingPromotionalOffers" in game["promotions"]:
        promotional_offers = game["promotions"]["upcomingPromotionalOffers"]
        if promotional_offers is not None and promotional_offers:
            promotional_offer = promotional_offers[0]["promotionalOffers"]
            if promotional_offer is not None and promotional_offer:
                game_start_date = promotional_offer[0].get("startDate", "")
                game_end_date = promotional_offer[0].get("endDate", "")
                status = "正在进行"
            else:
                game_start_date = "还未开始"
                game_end_date = "还未开始"
                status = "还未开始"
        else:
            game_start_date = "还未开始"
            game_end_date = "还未开始"
            status = "还未开始"
    else:
        game_start_date = "还未开始"
        game_end_date = "还未开始"
        status = "还未开始"

    game_cover_image = game["keyImages"][0].get("url", "")

    if "catalogNs" in game and "mappings" in game["catalogNs"] and game["catalogNs"]["mappings"]:
        game_page_slug = game["catalogNs"]["mappings"][0].get("pageSlug", "")
        game_link = f"https://store.epicgames.com/p/{game_page_slug}"
    else:
        game_page_slug = ""
        game_link = ""

    print(f"{status}")
    print(f"[{index}]")
    print(f"游戏名：{game_name}")
    print(f"发售商：{game_publisher}")
    print(f"原价：{game_price}")
    print(f"白嫖开始日期：{game_start_date}")
    print(f"白嫖结束日期：{game_end_date}")
    print(f"封面：{game_cover_image}")
    print(f"游戏链接：{game_link if game_link else ''} ({status})")
    print()
