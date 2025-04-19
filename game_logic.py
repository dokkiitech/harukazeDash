from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

from discord.ext import commands
from supabase_access import get_user_data, save_user_data
import random

def handle_dash(user_id):
    user = get_user_data(user_id) # ユーザーデータを取得または初期化

    # 成功か失敗をランダムに決定
    success = random.random() < 0.5  # 50% 成功

    if success:
        success = 1
        user['coins'] += 10
        user['dash_success'] += 1
    else:
        user['coins'] -= 5
    
    user['dash_count'] += 1

    # supabaseに保存
    save_user_data(user)

    return success, user['coins']