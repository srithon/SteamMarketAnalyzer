import requests

s = requests.Session()

proxy_list = ['104.221.131.27:3128']

item_list = [
'Decal Tool',
'Unleash the Beast Cosmetic Case #108',
'Abominable Cosmetic Case #107',
'Blue Moon Cosmetic Case #119',
'Mayflower Cosmetic Case #102',
'Rainy Day Cosmetic Case #106']
#'Unleash the Beast Cosmetic Case #108',
#'Winter 2017 Cosmetic Case #117',
#'Mann Co. Stockpile Crate',
#'Winter 2018 Cosmetic Case #122',
#'Scream Fortress X War Paint Case #121',
#'Reinforced Robot Bomb Stabilizer'

for proxy in proxy_list:
    print(f'Proxy: {proxy}')
    for index,item in enumerate(item_list):
        try:
            print(s.get('https://steamcommunity.com/market/priceoverview/?country=US&currency=1&appid=440&market_hash_name={item}', proxies={'https': proxy}).json())
        except Exception as e:
            print(f'{index}: Exception')