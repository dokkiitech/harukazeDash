from discord.ext import commands
from supabase_access import get_user_data, save_user_data
import random

def handle_dash(user_id):
    user_data = get_user_data(user_id) # ユーザーデータを取得または初期化

    # 成功か失敗をランダムに決定
    success = random.random() < 0.5  # 50% 成功

    if success:
        success = 1
        user_data['coins'] += 10
        user_data['dash_success'] += 1
    else:
        user_data['coins'] -= 5
    
    user_data['dash_count'] += 1

    # supabaseに保存
    save_user_data(user_id, user_data)

    return success, user_data['coins']