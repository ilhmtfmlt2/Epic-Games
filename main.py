import json
import requests
from datetime import datetime


def get_free_games() -> dict:
    timestamp = datetime.timestamp(datetime.now())
    games = {'timestamp': timestamp, 'free_now': [], 'free_next': []}
    base_store_url = 'https://store.epicgames.com'
    api_url = 'https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?country=CN'
    resp = requests.get(api_url)
    for element in resp.json()['data']['Catalog']['searchStore']['elements']:
        if promotions := element['promotions']:
            game = {}
            game['title'] = element['title']
            game['images'] = element['keyImages']
            game['origin_price'] = element['price']['totalPrice']['fmtPrice']['originalPrice']
            game['discount_price'] = element['price']['totalPrice']['fmtPrice']['discountPrice']
            game['store_url'] = f"{base_store_url}/p/{element['catalogNs']['mappings'][0]['pageSlug']}" if element['catalogNs']['mappings'] else base_store_url
            if offers := promotions['promotionalOffers']:
                game['start_date'] = offers[0]['promotionalOffers'][0]['startDate']
                game['end_date'] = offers[0]['promotionalOffers'][0]['endDate']
                games['free_now'].append(game)
            if offers := promotions['upcomingPromotionalOffers']:
                game['start_date'] = offers[0]['promotionalOffers'][0]['startDate']
                game['end_date'] = offers[0]['promotionalOffers'][0]['endDate']
                games['free_next'].append(game)
    return games


def generate_json(games: dict, filename: str):
    with open(filename, 'w') as f:
        json.dump(games, f)
        # json.dump(obj=games, fp=f, ensure_ascii=False, indent=4)


def generate_markdown(games: dict, filename: str):
    images = {}
    data = games['free_now'] + games['free_next']
    for game in data:
        for image in game['images']:
            if image['type'] in ['OfferImageWide', 'DieselStoreFrontWide']:
                images[game['title']] = image['url']
                break

    content = '''# Epic ????????????

- ## ????????????

'''

    for game in games['free_now']:
        content += f'''
  - ### [{game['title']}]

    ??????: {game['origin_price']}

    ????????????: [{game['store_url']}]

'''

    content += f'''
- ## ????????????

'''

    for game in games['free_next']:
        content += f'''
  - ### [{game['title']}]

    ??????: {game['origin_price']}

    ????????????: [{game['store_url']}]

'''

    with open(filename, 'w') as f:
        f.write(content)


if __name__ == '__main__':
    games = get_free_games()
    generate_json(games, './config.json')
    generate_markdown(games, './config.txt')
