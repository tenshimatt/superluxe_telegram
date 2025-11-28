#!/usr/bin/env python3
"""
Test script to verify SUPERLUXE bot configuration
"""

import os
import sys
sys.path.append('.')

from data import config
from loader import db

def test_config():
    """Test configuration loading"""
    print("=== Configuration Test ===")

    print(f"BOT_TOKEN present: {'Yes' if config.BOT_TOKEN else 'No'}")
    print(f"ADMINS: {config.ADMINS}")
    print(f"WEBHOOK_URL: {config.WEBHOOK_URL}")
    print(f"RAILWAY_PUBLIC_DOMAIN: {os.environ.get('RAILWAY_PUBLIC_DOMAIN', 'Not set')}")

    return bool(config.BOT_TOKEN)

def test_database():
    """Test database connection"""
    print("\n=== Database Test ===")

    try:
        # Test database tables
        categories = db.fetchall("SELECT * FROM categories")
        products = db.fetchall("SELECT * FROM products")

        print(f"Categories loaded: {len(categories)}")
        print(f"Products loaded: {len(products)}")

        if categories and products:
            print("✅ Database OK")
            return True
        else:
            print("❌ Database empty - run migration first")
            return False

    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def main():
    print("SUPERLUXE Telegram Bot - Configuration Test")
    print("=" * 50)

    config_ok = test_config()
    db_ok = test_database()

    print("\n=== Summary ===")
    print(f"Configuration: {'✅' if config_ok else '❌'}")
    print(f"Database: {'✅' if db_ok else '❌'}")

    if config_ok and db_ok:
        print("\n🎉 Bot is ready to deploy!")
        return 0
    else:
        print("\n❌ Issues found - check configuration")
        return 1

if __name__ == "__main__":
    sys.exit(main())