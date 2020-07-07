card_designs = {
    "Blizzard": {
        "Blizzard 1": {
            "design": "blizzard",
            "gacha": "Winter Special",
            "rarity": "Rare"
        },
    },
    "Razer": {
        "Razer Gift Card": {
            "design": "gift-cards-landingpg-OG-v2",
            "gacha": "Regular Gacha",
            "rarity": "Very Common"
        }
    },
    "Mobile Legends": {
        "Mobile Legends": {
            "design": "mobilelegends",
            "gacha": "Summer Special",
            "rarity": "Rare"
        },
    },
    "PlayerUnknown's Battlegrounds": {
        "PUBG": {
            "design": "pubg",
            "gacha": "Regular Gacha",
            "rarity": "Common"
        },
    },
    "Bigo Live": {
        "Bigo Live": {
            "design": "bigo",
            "gacha": "Winter Special",
            "rarity": "Very Rare"
        },
    },
    "MyCard Singapore": {
        "MyCard": {
            "design": "@cash",
            "gacha": "Anniversary Special",
            "rarity": "Very Common"
        },
    },
    "Dragon Nest": {
        "Dragon Nest": {
            "design": "dragon nest",
            "gacha": "Winter Special",
            "rarity": "Extremely Rare"
        },
    },
    "Gash": {
        "Gash": {
            "design": "gash",
            "gacha": "Regular Gacha",
            "rarity": "Common"
        },
    },
    "Nintendo": {
        "Nintendo": {
            "design": "nintendo",
            "gacha": "Autumn Special",
            "rarity": "Extremely Rare"
        },
    },
    "PlayStation Network": {
        "PlayStation": {
            "design": "pubg",
            "gacha": "Spring Special",
            "rarity": "Rare"
        },
    },
    "QQ Coin": {
        "QQ Coin": {
            "design": "QQ Coin",
            "gacha": "Regular Gacha",
            "rarity": "Common"
        },
    },
    "Ragnarok M: Eternal Love": {
        "Ragnarok M: Eternal Love": {
            "design": "ragnarok",
            "gacha": "Summer Special",
            "rarity": "Extremely Rare"
        },
    },
    "@Cash": {
        "@Cash": {
            "design": "@Cash",
            "gacha": "Regular Gacha",
            "rarity": "Very Common"
        },
    },
}


def fetch_card_design_names(game_name):
    return card_designs.get(game_name, {})