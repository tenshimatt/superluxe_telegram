#!/usr/bin/env python3
"""
SUPERLUXE Art Migration Script
Populates the Telegram bot database with SUPERLUXE art collections and content
"""

import sqlite3
import requests
import os
from io import BytesIO


def create_superluxe_data():
    """Create SUPERLUXE categories and artwork data based on real WordPress site"""

    # SUPERLUXE art collections from the actual website
    categories = [
        ("below-surface", "Below Surface"),
        ("oasis", "OASIS"),
        ("george-best", "GEORGE BEST"),
        ("escobar", "Escobar"),
        ("inured", "INURED"),
        ("bank-of-metin", "BANK OF METIN"),
        ("kate-moss", "Kate Moss"),
        ("stony", "Stony"),
        ("bullets", "Bullets"),
        ("vol-f", "Vol.F"),
        ("pencils", "Pencils"),
        ("blooms", "B(L)OOMS"),
        ("wonder", "Wonder"),
        ("minds-eye", "Mind's Eye"),
        ("echo-chamber", "Echo Chamber"),
        ("cat-faces", "Cat Faces"),
        ("duct-tape", "DUCT TAPE XXXX"),
        ("deep", "DEEP"),
        ("chess-art", "Chess Art"),
        ("eternity", "ETERNITY"),
        ("inner", "Inner"),
        ("wall-of-fame", "Wall of Fame"),
        ("funky-zoo", "Funky Zoo"),
        ("pets-rock", "Pets Rock"),
        ("icons", "ICONS"),
        ("chrome", "Chrome"),
        ("ozzy", "Ozzy"),
        ("streetview", "StreetView"),
        ("urban-collage", "Urban Collage"),
    ]

    # Real artworks with pricing from WordPress site (converted from GBP to USD roughly)
    artworks = [
        # OASIS Collection by Aiden Phelan - Based on real product data
        (
            "oasis-definitely-maybe-slide-away",
            "OASIS – 'Definitely Maybe' - Slide Away",
            "Iconic artwork from the OASIS collection by Aiden Phelan celebrating the 30th anniversary of 'Definitely Maybe'. Mixed Media on Board, Original 1 of 1.",
            4400,  # £3,500 converted to USD
            "oasis",
        ),
        (
            "oasis-definitely-maybe-shakermaker",
            "OASIS – 'Definitely Maybe' - Shakermaker",
            "Vibrant piece from Aiden Phelan's OASIS collection, capturing the rebellious spirit of the iconic band's era-defining album.",
            4400,
            "oasis",
        ),
        (
            "oasis-definitely-maybe-married-with-children",
            "OASIS – 'Definitely Maybe' - Married With Children",
            "Bold pop-art aesthetic from contemporary British artist Aidan Phelan, exploring modern culture through vivid color.",
            4400,
            "oasis",
        ),
        # GEORGE BEST Collection by Aiden Phelan
        (
            "george-best-legendary",
            "GEORGE BEST - Legendary Portrait",
            "Legendary George Best portrait by Aiden Phelan, capturing the essence of the football icon through distinctive visual language.",
            5000,
            "george-best",
        ),
        # Escobar Collection by Roberto Sendoya Escobar
        (
            "escobar-portrait-two",
            "Escobar - Portrait Two",
            "Powerful artwork from the Escobar collection by Roberto Sendoya Escobar, exploring themes of power and legacy.",
            5600,
            "escobar",
        ),
        # INURED Collection by Empirical Malum
        (
            "inured-pandora",
            "INURED - Pandora",
            "Thought-provoking piece from Empirical Malum's INURED collection, exploring contemporary social themes.",
            3600,
            "inured",
        ),
        # BANK OF METIN by Metin Salih
        (
            "bank-metin-ziggy",
            "BANK OF METIN - Ziggy Note",
            "Bold artwork from Metin Salih's BANK OF METIN collection, featuring distinctive artistic style and social commentary.",
            3900,
            "bank-of-metin",
        ),
        # Kate Moss by Tony Briggs
        (
            "kate-moss-portrait",
            "Kate Moss - Contemporary Portrait",
            "Stunning Kate Moss portrait by Tony Briggs, capturing the iconic supermodel through contemporary artistic vision.",
            5000,
            "kate-moss",
        ),
        # Stony by Antonio Russo
        (
            "stony-collection",
            "Stony - Bold Collection Piece",
            "Bold Stony collection piece by Antonio Russo, featuring distinctive artistic style and powerful visual impact.",
            2500,
            "stony",
        ),
        # Bullets by Federico Uribe
        (
            "bullets-lion-head",
            "Bullets - Lion Head Duck Nest",
            "Unique artwork from Federico Uribe's Bullets collection, creating powerful imagery through unconventional materials.",
            4100,
            "bullets",
        ),
        # Vol.F by Forist Amber
        (
            "vol-f-digital",
            "Vol.F - Digital Artwork",
            "Contemporary digital artwork from Forist Amber's Vol.F collection, pushing boundaries of digital artistic expression.",
            2200,
            "vol-f",
        ),
        # Pencils by Federico Uribe
        (
            "pencils-portrait-blue",
            "Pencils - Portrait Blue Hair",
            "Creative masterpiece from Federico Uribe's Pencils collection, showcasing incredible detail and artistic skill.",
            3200,
            "pencils",
        ),
        # B(L)OOMS by Nigel Stefani
        (
            "blooms-collection",
            "B(L)OOMS - Vibrant Artwork",
            "Vibrant artwork from Nigel Stefani's B(L)OOMS collection, featuring explosive color and dynamic composition.",
            2800,
            "blooms",
        ),
        # Wonder by Tom Lawton
        (
            "wonder-camp-kerala",
            "Wonder - Big Wonder Camp Kerala",
            "Intriguing piece from Tom Lawton's Wonder collection, exploring themes of discovery and imagination.",
            3000,
            "wonder",
        ),
        # Mind's Eye by Glen Fox
        (
            "minds-eye-erupt",
            "Mind's Eye - ERUPT",
            "Visionary artwork from Glen Fox's Mind's Eye collection, featuring explosive creativity and artistic vision.",
            3600,
            "minds-eye",
        ),
        # Echo Chamber by Bstract Jay
        (
            "echo-chamber-hidden-heart",
            "Echo Chamber - Hidden Heart",
            "Thought-provoking artwork from Bstract Jay's Echo Chamber collection, exploring themes of connection and isolation.",
            2500,
            "echo-chamber",
        ),
        # Cat Faces by Todd Goldman
        (
            "cat-faces-collection",
            "Cat Faces - Playful Collection",
            "Playful and whimsical artwork from Todd Goldman's Cat Faces collection, bringing feline charm to contemporary art.",
            2300,
            "cat-faces",
        ),
        # DUCT TAPE XXXX by Todd Goldman
        (
            "duct-tape-banana",
            "DUCT TAPE XXXX - Banana",
            "Edgy and unconventional artwork from Todd Goldman's DUCT TAPE XXXX collection, pushing artistic boundaries.",
            2600,
            "duct-tape",
        ),
        # DEEP by David Prescott
        (
            "deep-messi-glass",
            "DEEP - Messi Glass",
            "Profound artwork from David Prescott's DEEP collection, featuring Curtisium AROI Glass technology.",
            4600,
            "deep",
        ),
        # Chess Art by Matt Perchard
        (
            "chess-art-game-century",
            "Chess Art - Game of the Century",
            "Strategic masterpiece from Matt Perchard's Chess Art collection, combining intellectual depth with artistic beauty.",
            2600,
            "chess-art",
        ),
        # ETERNITY by Jocke Larsson
        (
            "eternity-freedom",
            "ETERNITY - Freedom",
            "Mesmerizing artwork from Jocke Larsson's ETERNITY collection, exploring themes of time and infinity.",
            4400,
            "eternity",
        ),
        # Inner by Jocke Larsson
        (
            "inner-shadow",
            "Inner - Shadow",
            "Introspective artwork from Jocke Larsson's Inner collection, exploring the depths of human consciousness.",
            3500,
            "inner",
        ),
        # Wall of Fame by Mark Holley
        (
            "wall-fame-frida-kahlo",
            "Wall of Fame - Frida Kahlo",
            "Iconic portrait from Mark Holley's Wall of Fame collection, celebrating legendary figures through artistic vision.",
            2700,
            "wall-of-fame",
        ),
        # Funky Zoo by Susan Lintell
        (
            "funky-zoo-collection",
            "Funky Zoo - Whimsical Collection",
            "Whimsical and playful artwork from Susan Lintell's Funky Zoo collection, bringing animal charm to contemporary art.",
            2100,
            "funky-zoo",
        ),
        # Pets Rock by Polybank
        (
            "pets-rock-insitu",
            "Pets Rock - In Situ Collection",
            "Fun and contemporary artwork from Polybank's Pets Rock collection, featuring beloved pets in artistic settings.",
            1900,
            "pets-rock",
        ),
        # ICONS by Dullal Miah
        (
            "icons-zendaya",
            "ICONS - Zendaya",
            "Modern artwork from Dullal Miah's ICONS collection, celebrating contemporary icons through artistic vision.",
            3100,
            "icons",
        ),
        # Chrome by Dullal Miah
        (
            "chrome-collection",
            "Chrome - Sleek Masterpiece",
            "Sleek and contemporary artwork from Dullal Miah's Chrome collection, featuring modern artistic techniques.",
            3500,
            "chrome",
        ),
        # Ozzy by Susan Lintell
        (
            "ozzy-character",
            "Ozzy - Characterful Artwork",
            "Characterful artwork from Susan Lintell's Ozzy collection, capturing distinctive personality through art.",
            2000,
            "ozzy",
        ),
        # StreetView by Eyeeyemouth
        (
            "streetview-barcelona",
            "StreetView - El Raval Barcelona",
            "Urban masterpiece from Eyeeyemouth's StreetView collection, capturing the essence of city life.",
            2700,
            "streetview",
        ),
        # Urban Collage by Eyeeyemouth
        (
            "urban-collage-dynamic",
            "Urban Collage - Dynamic Piece",
            "Dynamic artwork from Eyeeyemouth's Urban Collage collection, exploring contemporary urban themes.",
            3000,
            "urban-collage",
        ),
        # Below Surface by Freds
        (
            "below-surface-collection",
            "Below Surface - Ethereal Artwork",
            "Ethereal artwork from Freds' Below Surface collection, exploring hidden depths and unseen worlds.",
            3300,
            "below-surface",
        ),
    ]

    return categories, artworks


def download_image(url):
    """Download image from URL and return as bytes"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"Error downloading image {url}: {e}")
    return None


def get_image_urls():
    """Get actual image URLs from WordPress site"""
    base_url = "http://10.90.10.80/wp-content/uploads/"

    # Map of product IDs to their actual image URLs from the WordPress site
    image_urls = {
        "oasis-definitely-maybe-slide-away": base_url
        + "2025/10/SLIDE-AWAY-600x605.jpg",
        "oasis-definitely-maybe-shakermaker": base_url
        + "2025/10/SHAKERMAKER-300x300.jpg",
        "oasis-definitely-maybe-married-with-children": base_url
        + "2025/10/MARRIED-WITH-CHILDREN-300x300.jpg",
        "george-best-legendary": base_url + "2025/10/AP_BEST-012-1024x1018.jpg",
        "escobar-portrait-two": base_url
        + "2025/07/Portrait-Two_Campaign-Trail-697x1024.jpg",
        "inured-pandora": base_url + "2025/08/9.-PANDORA.jpg",
        "bank-metin-ziggy": base_url + "2025/08/Ziggy1Note_BankOfMetin-1024x536.jpg",
        "kate-moss-portrait": base_url + "2025/01/Kate-NEW-Web-Tile-1024x1006.jpg",
        "stony-collection": base_url + "2024/10/Stony2.jpg",
        "bullets-lion-head": base_url + "2025/03/Lion-Head-Duck-Nest-6-1024x683.jpg",
        "vol-f-digital": base_url
        + "2025/07/Forist-Amber-Digital-Assst-2-780x1024.jpeg",
        "pencils-portrait-blue": base_url + "2025/03/Portrait-Blue-Hair-2-1024x683.jpg",
        "blooms-collection": base_url + "2025/02/PPK-1024x724.jpg",
        "wonder-camp-kerala": base_url
        + "2025/04/Big_Wonder_Camp_Kerala_Small-683x1024.jpg",
        "minds-eye-erupt": base_url + "2025/03/ERUPT-reduced-809x1024.jpg",
        "echo-chamber-hidden-heart": base_url + "2025/03/8.-Hidden-Heart--771x1024.png",
        "cat-faces-collection": base_url + "2024/12/cat_faces_16-min-min.png",
        "duct-tape-banana": base_url + "2024/12/todd_goldman_DUCT-TAPE-BANANA-min.png",
        "deep-messi-glass": base_url + "2025/02/Messi-Glass-819x1024.png",
        "chess-art-game-century": base_url
        + "2024/11/ChessArt-Famous-games_Game-of-The-Century-White_Board-Reduced-1-1024x706.jpeg",
        "eternity-freedom": base_url + "2024/10/Freedom-1024x717.png",
        "inner-shadow": base_url + "2025/02/IINER-SHADOW-1024x1024.jpg",
        "wall-fame-frida-kahlo": base_url + "2025/01/Frida-Kahlo-1024x1015.jpg",
        "funky-zoo-collection": base_url + "2025/01/IMG_3101-3-740x1024.jpg",
        "pets-rock-insitu": base_url + "2024/11/INSITU_2-1024x724.jpeg",
        "icons-zendaya": base_url + "2024/10/Zendaya-717x1024.png",
        "chrome-collection": base_url
        + "2025/01/Copy-of-20240830-IMG_0756-Edited_240830_182645_240830_182732-797x1024.jpg",
        "ozzy-character": base_url + "2025/09/Ozzie.png",
        "streetview-barcelona": base_url + "2025/09/El-Raval-Barcelona-AW-771x1024.jpg",
        "urban-collage-dynamic": base_url + "2025/09/57-716x1024.jpg",
        "below-surface-collection": base_url + "2025/10/IMG_6370-768x1024.jpeg",
    }

    return image_urls


def migrate_database():
    """Migrate database with SUPERLUXE content"""

    # Connect to database
    db_path = "data/database.db"
    if not os.path.exists("data"):
        os.makedirs("data")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create tables if they don't exist
    cursor.execute("CREATE TABLE IF NOT EXISTS categories (idx text, title text)")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS products (idx text, title text, body text, photo blob, price int, tag text)"
    )
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS orders (cid int, usr_name text, usr_address text, products text)"
    )
    cursor.execute("CREATE TABLE IF NOT EXISTS cart (cid int, idx text, quantity int)")
    cursor.execute("CREATE TABLE IF NOT EXISTS wallet (cid int, balance real)")
    cursor.execute("CREATE TABLE IF NOT EXISTS questions (cid int, question text)")

    # Clear existing data
    cursor.execute("DELETE FROM categories")
    cursor.execute("DELETE FROM products")

    # Get SUPERLUXE data
    categories, artworks = create_superluxe_data()

    # Insert categories
    print("Inserting SUPERLUXE categories...")
    for idx, title in categories:
        cursor.execute(
            "INSERT INTO categories (idx, title) VALUES (?, ?)", (idx, title)
        )

    # Insert artworks
    print("Inserting SUPERLUXE artworks...")
    image_urls = get_image_urls()

    for idx, title, body, price, category in artworks:
        # Download actual image from WordPress site
        image_url = image_urls.get(idx, None)
        product_image = None

        if image_url:
            print(f"Downloading image for {idx} from {image_url}")
            product_image = download_image(image_url)
            if product_image:
                print(f"Successfully downloaded image for {idx}")
            else:
                print(f"Failed to download image for {idx}")
        else:
            print(f"No image URL found for {idx}")

        cursor.execute(
            """
            INSERT INTO products (idx, title, body, photo, price, tag) 
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (idx, title, body, product_image, price, category),
        )

    # Commit changes
    conn.commit()
    conn.close()

    print(
        f"✅ Successfully migrated {len(categories)} categories and {len(artworks)} artworks"
    )
    print("🎨 SUPERLUXE Telegram Bot is ready!")


if __name__ == "__main__":
    migrate_database()
