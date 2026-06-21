# ============================================================
# 🎵 YuanZe IEM 音樂版：靈魂調音師 (豐富色彩區分升級版)
# ============================================================
import os
import threading
import time
import json
import random
import urllib.parse
import re
import subprocess
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template_string
from werkzeug.serving import make_server
from sklearn.metrics.pairwise import euclidean_distances
import warnings
warnings.filterwarnings('ignore')

os.system("fuser -k 8889/tcp >/dev/null 2>&1")
time.sleep(1)

REAL_SONGS_CONFIG = {
    "華語": [
        ("七里香", "周杰倫"), ("晴天", "周杰倫"), ("告白氣球", "周杰倫"), ("稻香", "周杰倫"), ("愛在西元前", "周杰倫"),
        ("夜曲", "周杰倫"), ("半島鐵盒", "周杰倫"), ("安靜", "周杰倫"), ("說好不哭", "周杰倫"), ("擱淺", "周杰倫"),
        ("刻在我心底的名字", "盧廣仲"), ("魚仔", "盧廣仲"), ("幾分之幾", "盧廣仲"), ("狂迪", "盧廣仲"), ("明亮", "盧廣仲"),
        ("愛人錯過", "告五人"), ("好不容易", "告五人"), ("在這座城市遺失了你", "告五人"), ("唯一", "告五人"), ("披星戴月的想你", "告五人"),
        ("不是因為天氣晴朗才愛你", "理想混蛋"), ("愚者", "理想混蛋"), ("行星", "理想混蛋"), ("我還年輕 我還年輕", "老王樂隊"), ("安九", "老王樂隊"),
        ("山海", "草東沒有派對"), ("大風吹", "草東沒有派對"), ("浪子回頭", "茄子蛋"), ("愛情你比我想的閣較偉大", "茄子蛋"), ("捲菸", "美秀集團"),
        ("想和你看五月的晚霞", "陳華"), ("Without You", "高爾宣"), ("最後一次", "高爾宣"), ("怎麼了", "周興哲"), ("你，好不好？", "周興哲"),
        ("如果可以", "韋禮安"), ("女孩", "韋禮安"), ("一直都在", "韋禮安"), ("有一種悲傷", "A-Lin"), ("摯友", "A-Lin"),
        ("言不由衷", "徐佳瑩"), ("兜圈", "林宥嘉"), ("少女", "林宥嘉"), ("天真有邪", "林宥嘉"), ("孤勇者", "陳奕迅"), ("愛情轉移", "陳奕迅"),
        ("烏梅子醬", "李榮浩"), ("年少有為", "李榮浩"), ("不將就", "李榮浩"), ("嘉賓", "張遠"), ("星辰大海", "黃霄雲"),
        ("句號", "鄧紫棋"), ("倒數", "鄧紫棋"), ("差不多姑娘", "鄧紫棋"), ("光年之外", "鄧紫棋"),
        ("慢慢喜歡你", "莫文蔚"), ("連名帶姓", "張惠妹"), ("人質", "張惠妹"), ("慢冷", "梁靜茹"), ("情歌", "梁靜茹"),
        ("玫瑰少年", "蔡依林"), ("大眠", "王心凌"), ("小巨蛋", "田馥甄"), ("小幸運", "田馥甄"), ("無人知曉", "田馥甄"),
        ("突然好想你", "五月天"), ("溫柔", "五月天"), ("我不願讓你一個人", "五月天"), ("星空", "五月天"), ("知足", "五月天"),
        ("修煉愛情", "林俊傑"), ("那些你很冒險的夢", "林俊傑"), ("江南", "林俊傑"), ("不為誰而作的歌", "林俊傑"),
        ("無與倫比的美麗", "蘇打綠"), ("小情歌", "蘇打綠"), ("我好想你", "蘇打綠"), ("挪威的森林", "伍佰"), ("Last Dance", "伍佰")
    ],
    "西洋": [
        ("Cruel Summer", "Taylor Swift"), ("Blank Space", "Taylor Swift"), ("Love Story", "Taylor Swift"), ("Anti-Hero", "Taylor Swift"), ("Shake It Off", "Taylor Swift"),
        ("Shape of You", "Ed Sheeran"), ("Perfect", "Ed Sheeran"), ("Bad Habits", "Ed Sheeran"), ("Thinking Out Loud", "Ed Sheeran"), ("Photograph", "Ed Sheeran"),
        ("Blinding Lights", "The Weeknd"), ("Save Your Tears", "The Weeknd"), ("Starboy", "The Weeknd"), ("Die For You", "The Weeknd"), ("As It Was", "Harry Styles"),
        ("Flowers", "Miley Cyrus"), ("Stay", "The Kid LAROI & Justin Bieber"), ("Ghost", "Justin Bieber"), ("Peaches", "Justin Bieber"), ("Love Yourself", "Justin Bieber"),
        ("Bad Guy", "Billie Eilish"), ("Lovely", "Billie Eilish & Khalid"), ("Ocean Eyes", "Billie Eilish"), ("What Was I Made For?", "Billie Eilish"), ("Birds of a Feather", "Billie Eilish"),
        ("Drivers License", "Olivia Rodrigo"), ("Good 4 U", "Olivia Rodrigo"), ("Vampire", "Olivia Rodrigo"), ("Levitating", "Dua Lipa"), ("Don't Start Now", "Dua Lipa"),
        ("Dance The Night", "Dua Lipa"), ("Someone Like You", "Adele"), ("Rolling in the Deep", "Adele"), ("Easy On Me", "Adele"), ("Hello", "Adele"),
        ("Believer", "Imagine Dragons"), ("Thunder", "Imagine Dragons"), ("Radioactive", "Imagine Dragons"), ("Demons", "Imagine Dragons"), ("Counting Stars", "OneRepublic"),
        ("I Ain't Worried", "OneRepublic"), ("Sugar", "Maroon 5"), ("Memories", "Maroon 5"), ("Girls Like You", "Maroon 5"), ("Payphone", "Maroon 5"),
        ("Uptown Funk", "Bruno Mars"), ("Just the Way You Are", "Bruno Mars"), ("24K Magic", "Bruno Mars"), ("Die With A Smile", "Bruno Mars & Lady Gaga"), ("Shallow", "Lady Gaga & Bradley Cooper"),
        ("Yellow", "Coldplay"), ("Viva La Vida", "Coldplay"), ("Something Just Like This", "The Chainsmokers & Coldplay"), ("7 rings", "Ariana Grande"), ("thank u, next", "Ariana Grande"),
        ("Circles", "Post Malone"), ("Sunflower", "Post Malone"), ("Watermelon Sugar", "Harry Styles"), ("Sign of the Times", "Harry Styles"), ("Havana", "Camila Cabello")
    ],
    "日語": [
        ("夜に駆ける", "YOASOBI"), ("アイドル", "YOASOBI"), ("群青", "YOASOBI"), ("怪物", "YOASOBI"), ("勇者", "YOASOBI"),
        ("Lemon", "米津玄師"), ("Kick Back", "米津玄師"), ("Pale Blue", "米津玄師"), ("アイネクライネ", "米津玄師"), ("感電", "米津玄師"),
        ("Dry Flower", "優里"), ("ベテルギウス", "優里"), ("シャッター", "優里"), ("レオ", "優里"), ("ビリミリオン", "優里"),
        ("炎", "LiSA"), ("紅蓮華", "LiSA"), ("Catch the Moment", "LiSA"), ("残響散歌", "Aimer"), ("カタオモイ", "Aimer"),
        ("春を告げる", "yama"), ("怪獣の花唄", "Vaundy"), ("東京フラッシュ", "Vaundy"), ("踊り子", "Vaundy"), ("タイムパラドックス", "Vaundy"),
        ("Subtitle", "Official髭男dism"), ("Pretender", "Official髭男dism"), ("I LOVE...", "Official髭男dism"), ("Mixed Nuts", "Official髭男dism"), ("宿命", "Official髭男dism"),
        ("青のすみか", "キタニタツヤ"), ("打上花火", "DAOKO × 米津玄師"), ("丸の内サディスティック", "椎名林檎"), ("新時代", "Ado"), ("唱", "Ado"),
        ("うっせぇわ", "Ado"), ("ギラギラ", "Ado"), ("踊", "Ado"), ("First Love", "宇多田ヒカル"), ("One Last Kiss", "宇多田ヒカル"),
        ("君はロックを聽かない", "あいみょん"), ("マリーゴールド", "あいみょん"), ("裸の心", "あいみょん"), ("ハルノヒ", "あいみょん"), ("愛を伝えたいだとか", "あいみょん"),
        ("きらり", "藤井風"), ("死ぬのがいいわ", "藤井風"), ("まつり", "藤井風"), ("花", "藤井風"), ("満ちてゆく", "藤井風"),
        ("前前前世", "RADWIMPS"), ("スパークル", "RADWIMPS"), ("なんでもないや", "RADWIMPS"), ("白日", "King Gnu"), ("一途", "King Gnu"),
        ("ただ君に晴れ", "ヨルシカ"), ("春泥棒", "ヨルシカ"), ("だから僕は音楽を辞めた", "ヨルシカ"), ("Wherever you are", "ONE OK ROCK"), ("The Beginning", "ONE OK ROCK")
    ],
    "韓語": [
        ("Ditto", "NewJeans"), ("OMG", "NewJeans"), ("Hype Boy", "NewJeans"), ("Super Shy", "NewJeans"), ("How Sweet", "NewJeans"),
        ("Dynamite", "BTS"), ("Butter", "BTS"), ("Spring Day", "BTS"), ("Boy With Luv", "BTS"), ("Seven", "Jungkook"),
        ("Kill This Love", "BLACKPINK"), ("DDU-DU DDU-DU", "BLACKPINK"), ("How You Like That", "BLACKPINK"), ("Pink Venom", "BLACKPINK"), ("As If It's Your Last", "BLACKPINK"),
        ("SOLO", "JENNIE"), ("You & Me", "JENNIE"), ("Flower", "JISOO"), ("On The Ground", "ROSÉ"),
        ("Love Dive", "IVE"), ("I AM", "IVE"), ("After LIKE", "IVE"), ("Eleven", "IVE"), ("Baddie", "IVE"),
        ("Next Level", "aespa"), ("Spicy", "aespa"), ("Drama", "aespa"), ("Supernova", "aespa"), ("Armageddon", "aespa"),
        ("TOMBOY", "(G)I-DLE"), ("Nxde", "(G)I-DLE"), ("Queencard", "(G)I-DLE"), ("Super Lady", "(G)I-DLE"), ("Klaxon", "(G)I-DLE"),
        ("Love Scenario", "iKON"), ("BBoom BBoom", "MOMOLAND"), ("Cheer Up", "TWICE"), ("TT", "TWICE"),
        ("Fancy", "TWICE"), ("What is Love?", "TWICE"), ("Feel Special", "TWICE"), ("Psycho", "Red Velvet"), ("Bad Boy", "Red Velvet"),
        ("Growl", "EXO"), ("Love Shot", "EXO"), ("Sorry Sorry", "Super Junior"), ("Fantastic Baby", "BIGBANG"), ("BANG BANG BANG", "BIGBANG"),
        ("God's Menu", "Stray Kids"), ("S-Class", "Stray Kids"), ("Super", "SEVENTEEN"), ("Hot", "SEVENTEEN"), ("WANNABE", "ITZY"),
        ("ANTIFRAGILE", "LE SSERAFIM"), ("UNFORGIVEN", "LE SSERAFIM"), ("Perfect Night", "LE SSERAFIM"), ("Cupid", "FIFTY FIFTY"), ("Magnetic", "ILLIT")
    ],
    "純音樂": [
        ("Summer", "久石讓"), ("One Summer's Day", "久石讓"), ("Merry-Go-Round of Life", "久石讓"), ("The Wind Forest", "久石讓"), ("Ashitaka and San", "久石讓"),
        ("River Flows in You", "Yiruma"), ("Kiss the Rain", "Yiruma"), ("Maybe", "Yiruma"), ("Spring Waltz", "Yiruma"), ("Reminiscent", "Yiruma"),
        ("Merry Christmas, Mr. Lawrence", "坂本龍一"), ("Aqua", "坂本龍一"), ("Energy Flow", "坂本龍一"), ("Opus", "坂本龍一"), ("Rain", "坂本龍一"),
        ("Flower Dance", "DJ Okawari"), ("Luv Letter", "DJ Okawari"), ("Represent", "DJ Okawari"), ("Peacock", "DJ Okawari"), ("Bluebird Story", "DJ Okawari"),
        ("Time", "Hans Zimmer"), ("Interstellar Main Theme", "Hans Zimmer"), ("Cornfield Chase", "Hans Zimmer"), ("Experience", "Ludovico Einaudi"), ("Nuvole Bianche", "Ludovico Einaudi"),
        ("Comptine d'un autre été", "Yann Tiersen"), ("The Heart Asks Pleasure First", "Michael Nyman"), ("Sadness and Sorrow", "增田俊郎"), ("Blue Bird (Piano Ver.)", "動漫鋼琴"), ("Sadame", "佐藤直紀"),
        ("Wind Song", "押尾光太郎"), ("Twilight", "押尾光太郎"), ("Fight!", "押尾光太郎"), ("Wings You Are The Hero", "押尾光太郎"), ("Splash", "押尾光太郎"),
        ("Sunburst", "Andrew York"), ("Cavatina", "Stanley Myers"), ("Asturias", "Isaac Albéniz"), ("Canon in D (Piano)", "Johann Pachelbel"), ("Gymnopédie No.1", "Erik Satie"),
        ("Clair de Lune", "Claude Debussy"), ("Nocturne Op.9 No.2", "Frédéric Chopin"), ("Für Elise", "Ludwig van Beethoven"), ("Moonlight Sonata 1st", "Ludwig van Beethoven"), ("River Flows In You (Guitar)", "經典吉他"),
        ("Snowdreams", "Bandari"), ("The Sound of Silence (Pan Flute)", "Leo Rojas"), ("Song from a Secret Garden", "Secret Garden"), ("Reflections", "Ginggi"), ("Always With Me (Piano)", "木村弓"),
        ("Spirited Away Theme", "久石讓"), ("Howl's Moving Castle", "久石讓"), ("Grief and Sorrow", "高梨康治"), ("Divenire", "Ludovico Einaudi"), ("A Model of the Universe", "Jóhann Jóhannsson")
    ]
}
REGIONS_MAP = {"華語": "cpop", "西洋": "western", "日語": "jpop", "韓語": "kpop", "純音樂": "instrumental"}

print("⚙️ [1/2] 正在建構五維音樂特徵矩陣...")
song_list_build = []
for lang_chinese, songs in REAL_SONGS_CONFIG.items():
    region_code = REGIONS_MAP[lang_chinese]
    for title, artist in songs:
        if region_code == "instrumental": bpm, valence, energy, acoustic, instrumental = 65, 0.3, 0.15, 0.95, 0.95
        elif region_code == "kpop": bpm, valence, energy, acoustic, instrumental = 125, 0.75, 0.85, 0.05, 0.0
        else: bpm, valence, energy, acoustic, instrumental = 100, 0.5, 0.55, 0.3, 0.0
        song_list_build.append({ "title": title, "artist": artist, "region": region_code, "region_label": lang_chinese, "bpm": bpm, "valence": valence, "energy": energy, "acoustic": acoustic, "instrumental": instrumental })

np.random.seed(42)
total_target = 10000
needed_count = total_target - len(song_list_build)
languages_keys = list(REAL_SONGS_CONFIG.keys())
mock_bpm = np.random.randint(55, 175, needed_count)
mock_valence = np.random.uniform(0.05, 0.95, needed_count)
mock_energy = np.random.uniform(0.05, 0.95, needed_count)
mock_acoustic = np.random.uniform(0.0, 1.0, needed_count)
mock_instrumental = np.random.uniform(0.0, 1.0, needed_count)

for i in range(needed_count):
    rand_lang = random.choice(languages_keys)
    base_song = random.choice(REAL_SONGS_CONFIG[rand_lang])
    song_list_build.append({
        "title": base_song[0], "artist": base_song[1], "region": REGIONS_MAP[rand_lang], "region_label": rand_lang,
        "bpm": int(mock_bpm[i]), "valence": round(float(mock_valence[i]), 2), "energy": round(float(mock_energy[i]), 2),
        "acoustic": round(float(mock_acoustic[i]), 2), "instrumental": round(float(mock_instrumental[i]), 2)
    })

df_songs = pd.DataFrame(song_list_build)
df_songs['bpm_norm'] = (df_songs['bpm'] - 50) / 130
df_songs['bpm_norm'] = df_songs['bpm_norm'].clip(0, 1)

MUSIC_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YuanZe IEM - Music Board</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Noto+Sans+TC:wght@400;700;900&display=swap');
        body { background-color: #fbfbfb; color: #000; font-family: 'Inter', 'Noto Sans TC', sans-serif; }
        .brutalist-card { background: #ffffff; border: 3px solid #000000; border-radius: 1.5rem; box-shadow: 6px 6px 0px #000000; transition: all 0.3s ease; }
        .custom-select { appearance: none; background-color: #f9f9f9; border: 2px solid #000000; border-radius: 0.75rem; padding: 0.75rem 1rem; font-weight: 700; color: #000; background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%23000' stroke-linecap='round' stroke-linejoin='round' stroke-width='2' d='M6 8l4 4 4-4'/%3e%3c/svg%3e"); background-position: right 0.75rem center; background-repeat: no-repeat; background-size: 1.2em 1.2em; outline: none; transition: border-color 0.2s, box-shadow 0.2s; }
        .custom-select:focus { box-shadow: 3px 3px 0px #cccccc; }

        .btn-purple-gradient { background: linear-gradient(90deg, #7e57c2, #ab47bc); color: #ffffff; border-radius: 12px; font-weight: 900; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(126, 87, 194, 0.4); border: none; }
        .btn-purple-gradient:hover { opacity: 0.9; transform: translateY(-2px); box-shadow: 0 6px 20px rgba(126, 87, 194, 0.6); }

        .song-item { background: #ffffff; border: 1px solid #eaeaea; border-radius: 12px; transition: all 0.2s; }
        .song-item:hover { transform: translateY(-3px); box-shadow: 4px 4px 0px #000000; border-color: transparent;}

        .filter-btn { border: 1px solid #d1d5db; background: #ffffff; color: #4b5563; font-weight: 700; border-radius: 9999px; padding: 6px 18px; font-size: 13px; transition: all 0.2s; }
        .filter-btn:hover { border-color: #9ca3af; background: #f3f4f6; }
        .filter-btn.active { background: #111111; color: #ffffff; border-color: #111111; }

        .feature-bar-bg { background-color: #eeeeee; border-radius: 9999px; height: 8px; overflow: hidden; border: 1px solid #ccc; }
        .feature-bar { height: 100%; transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }
        .no-scrollbar::-webkit-scrollbar { display: none; }
        .no-scrollbar { -ms-overflow-style: none; scrollbar-width: none; }
        .custom-scrollbar::-webkit-scrollbar { width: 6px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: #f1f1f1; border-radius: 8px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #ccc; border-radius: 8px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #000; }
    </style>
</head>
<body class="min-h-screen p-4 md:p-8 relative">

    <div id="music_loading_overlay" class="fixed inset-0 bg-black/70 backdrop-blur-sm z-50 flex flex-col items-center justify-center space-y-6 hidden" style="user-select: none;">
        <div class="flex space-x-3 items-end h-20">
            <div class="w-4 bg-purple-400 rounded-full animate-bounce h-12" style="animation-delay: 0.1s"></div>
            <div class="w-4 bg-pink-400 rounded-full animate-bounce h-16" style="animation-delay: 0.2s"></div>
            <div class="w-4 bg-indigo-400 rounded-full animate-bounce h-10" style="animation-delay: 0.3s"></div>
        </div>
        <p class="text-white font-black text-2xl tracking-widest animate-pulse">✨ 正在為您推薦最佳歌曲...</p>
    </div>

    <div class="max-w-6xl mx-auto">
        <div class="text-center mt-6 mb-12">
            <div class="text-xs text-gray-500 font-bold tracking-[0.3em] mb-3 uppercase">YuanZe IEM // Music Board</div>
            <h1 class="text-6xl md:text-8xl font-black tracking-tighter text-black">MUSIC®</h1>
            <p class="mt-4 font-bold text-gray-400 tracking-widest uppercase text-sm">Soul Tuner 靈魂調音系統</p>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div class="lg:col-span-4 brutalist-card p-6 flex flex-col">
                <h2 class="text-sm font-black mb-6 text-gray-400 border-b-2 border-gray-100 pb-3 uppercase tracking-widest flex items-center">
                    <span class="mr-2 text-black">🔍</span> Context Settings
                </h2>
                <div class="space-y-5 flex-grow">
                    <div class="bg-gray-50 p-4 rounded-2xl border-2 border-transparent hover:border-gray-200 transition">
                        <h3 class="text-xs font-black text-black uppercase tracking-wider mb-3">環境狀態</h3>
                        <div class="grid grid-cols-2 gap-3">
                            <div><label class="block text-xs mb-1 text-gray-500 font-bold">⛅ 天氣</label><select id="env_weather" class="custom-select w-full text-sm"><option value="☀️ 晴天">☀️ 晴天</option><option value="⛅ 陰天">⛅ 陰天</option><option value="🌧️ 雨天">🌧️ 雨天</option><option value="⛈️ 雷陣雨">⛈️ 雷陣雨</option><option value="🍃 起風">🍃 起風</option><option value="❄️ 下雪">❄️ 下雪</option></select></div>
                            <div><label class="block text-xs mb-1 text-gray-500 font-bold">🕰️ 時間</label><select id="env_time" class="custom-select w-full text-sm"><option value="🌅 清晨">🌅 清晨</option><option value="🌄 早上">🌄 早上</option><option value="🕛 正午">🕛 正午</option><option value="🌇 午後">🌇 午後</option><option value="🌆 黃昏">🌆 黃昏</option><option value="🌃 晚上">🌃 晚上</option><option value="🌙 深夜" selected>🌙 深夜</option></select></div>
                        </div>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-2xl border-2 border-transparent hover:border-gray-200 transition">
                        <h3 class="text-xs font-black text-black uppercase tracking-wider mb-3">當下活動</h3>
                        <select id="ctx_activity" class="custom-select w-full text-sm"><option value="📖 讀書/工作" selected>📖 讀書/工作</option><option value="📚 閱讀休閒">📚 閱讀休閒</option><option value="🚌 通勤/移動">🚌 通勤/移動</option><option value="🚗 開車兜風">🚗 開車兜風</option><option value="🏋️ 運動/健身">🏋️ 運動/健身</option><option value="🎮 打遊戲">🎮 打遊戲</option><option value="🎉 派對/聚會">🎉 派對/聚會</option><option value="🍵 發呆/放空">🍵 發呆/放空</option><option value="🛏️ 準備入睡">🛏️ 準備入睡</option></select>
                    </div>
                    <div class="bg-gray-50 p-4 rounded-2xl border-2 border-transparent hover:border-gray-200 transition">
                        <h3 class="text-xs font-black text-black uppercase tracking-wider mb-3">心理期望</h3>
                        <div class="space-y-3">
                            <div><label class="block text-xs mb-1 text-gray-500 font-bold">❤️ 當前心情</label><select id="psy_mood" class="custom-select w-full text-sm"><option value="🧘 平靜">🧘 平靜</option><option value="😰 焦慮/壓力大">😰 焦慮/壓力大</option><option value="😄 愉悅">😄 愉悅</option><option value="🌧️ 低落/憂鬱" selected>🌧️ 低落/憂鬱</option><option value="😡 憤怒/煩躁">😡 憤怒/煩躁</option><option value="🔥 充滿活力">🔥 充滿活力</option></select></div>
                            <div><label class="block text-xs mb-1 text-gray-500 font-bold">✨ 渴望轉換</label><select id="psy_goal" class="custom-select w-full text-sm"><option value="🩹 想被治癒/陪伴" selected>🩹 想被治癒/陪伴</option><option value="⚡ 想提振精神">⚡ 想提振精神</option><option value="🎯 想極度專注">🎯 想極度專注</option><option value="🛁 想徹底放鬆">🛁 想徹底放鬆</option><option value="🗣️ 想發洩情緒">🗣️ 想發洩情緒</option><option value="💤 想安穩入眠">💤 想安穩入眠</option></select></div>
                        </div>
                    </div>
                </div>

                <button onclick="generateCapsule()" id="btn_generate" class="btn-purple-gradient w-full mt-6 py-4 flex justify-center items-center text-lg tracking-wide disabled:opacity-50 disabled:cursor-not-allowed">
                    <span id="btn_text">✨ 生成為您推薦的歌曲</span>
                </button>
            </div>

            <div class="lg:col-span-8 brutalist-card p-8 flex flex-col relative overflow-hidden bg-white">
                <div id="welcome_panel" class="h-full flex items-center justify-center min-h-[500px]">
                    <div class="text-center text-gray-300">
                        <div class="text-6xl font-black mb-4 tracking-tighter text-gray-200">10,000+</div>
                        <p class="text-sm font-bold tracking-widest text-gray-400 uppercase">Songs in Matrix</p>
                        <p class="mt-4 text-xs font-bold text-gray-400">請在左側設定情境，系統將為您過濾出最契合的音樂</p>
                    </div>
                </div>

                <div id="result_panel" class="hidden flex-col h-full space-y-8 animate-fade-in">
                    <div class="bg-gray-50 p-5 rounded-2xl border-l-8 border-black">
                        <h3 class="text-xs text-gray-400 font-black mb-2 tracking-widest uppercase">System Message</h3>
                        <p id="empathy_message" class="text-sm leading-relaxed text-black font-bold"></p>
                    </div>
                    <div class="grid grid-cols-1 xl:grid-cols-12 gap-8 flex-grow">
                        <div class="xl:col-span-4 flex flex-col">
                            <h3 class="text-[11px] font-black text-gray-400 mb-4 uppercase tracking-widest border-b-2 border-gray-100 pb-2">Acoustic Features</h3>
                            <div class="space-y-4 bg-gray-50 p-5 rounded-2xl border-2 border-gray-100">
                                <div><div class="flex justify-between text-[10px] mb-1 font-bold"><span class="text-black">Valence (正向)</span><span id="val_v" class="text-gray-500"></span></div><div class="feature-bar-bg"><div id="bar_v" class="bg-black feature-bar" style="width:0%"></div></div></div>
                                <div><div class="flex justify-between text-[10px] mb-1 font-bold"><span class="text-black">Energy (能量)</span><span id="val_e" class="text-gray-500"></span></div><div class="feature-bar-bg"><div id="bar_e" class="bg-black feature-bar" style="width:0%"></div></div></div>
                                <div><div class="flex justify-between text-[10px] mb-1 font-bold"><span class="text-black">Acoustic (木吉他/鋼琴)</span><span id="val_a" class="text-gray-500"></span></div><div class="feature-bar-bg"><div id="bar_a" class="bg-black feature-bar" style="width:0%"></div></div></div>
                                <div><div class="flex justify-between text-[10px] mb-1 font-bold"><span class="text-black">Instrumental (純樂器)</span><span id="val_i" class="text-gray-500"></span></div><div class="feature-bar-bg"><div id="bar_i" class="bg-black feature-bar" style="width:0%"></div></div></div>
                                <div class="mt-4 pt-4 border-t-2 border-gray-200 text-center">
                                    <span class="text-[10px] text-gray-400 font-black mb-1 block uppercase tracking-widest">Target Tempo</span>
                                    <span id="val_bpm" class="text-2xl font-black text-black block"></span>
                                </div>
                            </div>
                        </div>
                        <div class="xl:col-span-8 flex flex-col">
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b-2 border-gray-100 pb-3 mb-4 gap-3">
                                <h3 class="text-xs font-black text-black uppercase tracking-widest whitespace-nowrap">🎧 推薦歌單 <span id="song_count_label" class="text-gray-400 font-normal"></span></h3>

                                <div class="flex flex-wrap gap-2 pb-1" id="filter_buttons">
                                    <button onclick="filterList('all', this)" class="filter-btn active">全部</button>
                                    <button onclick="filterList('cpop', this)" class="filter-btn">華語</button>
                                    <button onclick="filterList('western', this)" class="filter-btn">西洋</button>
                                    <button onclick="filterList('jpop', this)" class="filter-btn">日語</button>
                                    <button onclick="filterList('kpop', this)" class="filter-btn">韓語</button>
                                    <button onclick="filterList('instrumental', this)" class="filter-btn">純音樂</button>
                                </div>
                            </div>
                            <div id="playlist_container" class="grid grid-cols-1 sm:grid-cols-2 gap-3 overflow-y-auto pr-2 h-[350px] custom-scrollbar"></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function filterList(regionCode, btnElement) {
            document.querySelectorAll('.filter-btn').forEach(btn => btn.className = "filter-btn");
            btnElement.className = "filter-btn active";
            const songs = document.querySelectorAll('.song-item');
            let visibleCount = 0;
            songs.forEach(song => {
                if (regionCode === 'all' || song.getAttribute('data-region') === regionCode) {
                    song.style.display = 'flex'; visibleCount++;
                } else { song.style.display = 'none'; }
            });
            document.getElementById('song_count_label').innerText = `(${visibleCount} 首)`;
        }

        async function generateCapsule() {
            const btn = document.getElementById('btn_generate');
            const overlay = document.getElementById('music_loading_overlay');

            btn.disabled = true;
            overlay.classList.remove('hidden');

            document.getElementById('welcome_panel').classList.add('hidden');
            document.getElementById('result_panel').classList.add('hidden');

            const payload = { weather: document.getElementById('env_weather').value, time: document.getElementById('env_time').value, activity: document.getElementById('ctx_activity').value, mood: document.getElementById('psy_mood').value, goal: document.getElementById('psy_goal').value };

            try {
                await new Promise(r => setTimeout(r, 1200));

                const response = await fetch('/api/recommend', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
                if (!response.ok) throw new Error("伺服器回傳錯誤代碼");
                const data = await response.json();

                document.getElementById('empathy_message').innerHTML = data.empathy_message;
                const features = data.target_features;
                document.getElementById('val_v').textContent = features.valence; document.getElementById('val_e').textContent = features.energy; document.getElementById('val_a').textContent = features.acousticness; document.getElementById('val_i').textContent = features.instrumentalness; document.getElementById('val_bpm').textContent = features.bpm + " BPM";

                setTimeout(() => { document.getElementById('bar_v').style.width = (features.valence * 100) + '%'; document.getElementById('bar_e').style.width = (features.energy * 100) + '%'; document.getElementById('bar_a').style.width = (features.acousticness * 100) + '%'; document.getElementById('bar_i').style.width = (features.instrumentalness * 100) + '%'; }, 100);

                const playlistDiv = document.getElementById('playlist_container'); playlistDiv.innerHTML = '';

                // 🌟 色彩地圖對應表 (定義各語系的專屬顏色)
                const styleMap = {
                    'cpop': { bg: 'bg-blue-100', text: 'text-blue-700', border: 'border-l-blue-500', avatarBg: '3b82f6' },
                    'western': { bg: 'bg-rose-100', text: 'text-rose-700', border: 'border-l-rose-500', avatarBg: 'e11d48' },
                    'jpop': { bg: 'bg-purple-100', text: 'text-purple-700', border: 'border-l-purple-500', avatarBg: '9333ea' },
                    'kpop': { bg: 'bg-amber-100', text: 'text-amber-700', border: 'border-l-amber-500', avatarBg: 'd97706' },
                    'instrumental': { bg: 'bg-emerald-100', text: 'text-emerald-700', border: 'border-l-emerald-500', avatarBg: '059669' }
                };

                data.playlist.forEach((song, index) => {
                    const safeTitle = song.title.length >= 2 ? song.title.substring(0,2) : song.title;
                    const style = styleMap[song.region] || { bg: 'bg-gray-100', text: 'text-gray-700', border: 'border-l-gray-400', avatarBg: '4b5563' };

                    // 將預設背景 000 替換為該語系的專屬顏色
                    const coverUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(safeTitle)}&background=${style.avatarBg}&color=fff&size=128&bold=true`;
                    const playUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(song.title + " " + song.artist)}`;

                    // 加入語系專屬 border-l-4 顏色
                    playlistDiv.innerHTML += `
                        <a href="${playUrl}" target="_blank" data-region="${song.region}" class="song-item border-l-4 ${style.border} flex items-center p-3 group cursor-pointer decoration-transparent w-full">
                            <div class="text-xs text-gray-400 font-black w-6 flex-shrink-0 text-center mr-2">${index + 1}</div>
                            <div class="w-10 h-10 rounded shadow-sm overflow-hidden flex-shrink-0 relative border border-gray-200">
                                <img src="${coverUrl}" class="w-full h-full object-cover">
                                <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 bg-black/70 backdrop-blur-sm"><span class="text-white text-xs">▶</span></div>
                            </div>
                            <div class="ml-3 flex-grow min-w-0 flex flex-col justify-center">
                                <p class="text-sm font-black text-black truncate leading-tight">${song.title}</p>
                                <p class="text-[10px] font-bold text-gray-500 truncate mt-0.5 leading-tight">${song.artist}</p>
                            </div>
                            <div class="text-right flex-shrink-0 ml-2 w-14 flex items-center justify-end">
                                <!-- 加入語系專屬 Tag 顏色 -->
                                <span class="text-[9px] font-black ${style.text} ${style.bg} px-1.5 py-0.5 rounded uppercase tracking-wider whitespace-nowrap">${song.region_label}</span>
                            </div>
                        </a>
                    `;
                });

                const allBtn = document.querySelector('.filter-btn'); if(allBtn) filterList('all', allBtn);

                overlay.classList.add('hidden');
                document.getElementById('result_panel').classList.remove('hidden');
            } catch (error) {
                console.error(error); alert('系統演算法推論出錯：後端可能發生錯誤，請重新嘗試。');
                overlay.classList.add('hidden');
                document.getElementById('welcome_panel').classList.remove('hidden');
            } finally {
                btn.disabled = false;
            }
        }
    </script>
</body>
</html>
"""

music_app = Flask(__name__)

@music_app.route('/')
def home():
    return render_template_string(MUSIC_HTML_TEMPLATE)

@music_app.route('/api/recommend', methods=['POST'])
def recommend():
    req = request.json
    target_v, target_e, target_a, target_i, target_bpm = 0.5, 0.5, 0.5, 0.0, 100

    act = req.get('activity', '')
    if "讀書" in act or "工作" in act: target_i, target_e, target_bpm = 0.85, 0.3, 70
    elif "運動" in act or "健身" in act: target_e, target_bpm, target_v, target_a = 0.9, 132, 0.75, 0.05
    elif "入睡" in act: target_e, target_a, target_i, target_bpm = 0.08, 0.95, 0.9, 52
    elif "放空" in act or "發呆" in act: target_e, target_a, target_bpm = 0.45, 0.75, 82
    elif "遊戲" in act: target_e, target_bpm, target_i = 0.85, 122, 0.4
    elif "閱讀" in act: target_e, target_a, target_i, target_bpm = 0.25, 0.85, 0.75, 68
    elif "開車" in act or "兜風" in act: target_e, target_bpm, target_v = 0.72, 112, 0.65
    elif "家事" in act: target_e, target_bpm, target_v = 0.68, 116, 0.68
    elif "派對" in act or "聚會" in act: target_e, target_bpm, target_v = 0.92, 126, 0.82

    mood = req.get('mood', '')
    if "平靜" in mood: target_v, target_e = 0.58, 0.38
    elif "焦慮" in mood: target_v, target_e = 0.38, 0.72
    elif "愉悅" in mood: target_v, target_e = 0.82, 0.78
    elif "低落" in mood or "憂鬱" in mood: target_v, target_e = 0.18, 0.28
    elif "憤怒" in mood or "煩躁" in mood: target_v, target_e = 0.22, 0.88
    elif "浪漫" in mood or "微醺" in mood: target_v, target_e, target_a = 0.62, 0.42, 0.65
    elif "懷舊" in mood or "思念" in mood: target_v, target_e, target_a = 0.42, 0.32, 0.72
    elif "活力" in mood: target_v, target_e = 0.82, 0.88

    goal = req.get('goal', '')
    if "治癒" in goal or "陪伴" in goal: target_v = 0.42; target_a = min(1.0, target_a + 0.28); target_e = min(target_e, 0.38)
    elif "精神" in goal: target_v = 0.78; target_e = 0.82; target_bpm = max(target_bpm, 115)
    elif "專注" in goal: target_i = 0.92; target_v = 0.48
    elif "放鬆" in goal: target_e = 0.18; target_a = 0.78; target_bpm = min(target_bpm, 72)
    elif "發洩" in goal: target_e = 0.88; target_bpm = max(target_bpm, 132)
    elif "安穩" in goal: target_e = 0.04; target_a = 0.92; target_i = 0.92; target_bpm = 48

    weather = req.get('weather', '')
    if "雨" in weather: target_a = min(1.0, target_a + 0.18); target_v = max(0.0, target_v - 0.12)
    elif "風" in weather: target_e = min(1.0, target_e + 0.08)
    elif "雪" in weather: target_a = min(1.0, target_a + 0.22); target_e = max(0.0, target_e - 0.08)

    time_val = req.get('time', '')
    if time_val in ["night", "midnight", "dawn"] or "夜" in time_val or "晨" in time_val: target_e = max(0.0, target_e - 0.12)

    target_bpm_norm = max(0, min(1, (target_bpm - 50) / 130))
    target_vector = np.array([[target_v, target_e, target_a, target_i, target_bpm_norm]])

    db_features = df_songs[['valence', 'energy', 'acoustic', 'instrumental', 'bpm_norm']].values
    df_songs['distance'] = euclidean_distances(target_vector, db_features)[0]

    unique_sorted_songs = df_songs.sort_values('distance').drop_duplicates(subset=['title', 'artist'], keep='first')
    quota_config = {"cpop": 50, "western": 50, "jpop": 50, "kpop": 50, "instrumental": 50}

    recommended_frames = []
    for region_code, quota in quota_config.items():
        recommended_frames.append(unique_sorted_songs[unique_sorted_songs['region'] == region_code].head(quota))

    recommended_df = pd.concat(recommended_frames).sort_values('distance')
    recommended_songs = recommended_df.to_dict(orient='records')

    msg = f"系統精算完畢。感測到您目前處於「{mood}」的心境，且在「{weather}」環境下正準備進行「{act}」。 我們為您精選了無重複歌曲，請盡情享受。"
    response = {
        "target_features": { "valence": round(target_v, 2), "energy": round(target_e, 2), "acousticness": round(target_a, 2), "instrumentalness": round(target_i, 2), "bpm": target_bpm },
        "playlist": recommended_songs, "empathy_message": msg
    }
    return jsonify(response)

class MusicServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 8889, app)
        self.ctx = app.app_context()
        self.ctx.push()
    def run(self): self.server.serve_forever()
    def shutdown(self): self.server.shutdown()

def start_music_server():
    global music_server
    if 'music_server' in globals(): music_server.shutdown(); time.sleep(1)
    music_server = MusicServerThread(music_app)
    music_server.start()

    print("\n" + "="*60)
    print("🚀 音樂版終極融合系統已啟動！(豐富色彩區分升級版)")
    print("🌍 正在啟動【音樂版】專屬公開通道...")

    subprocess.run(["wget", "-q", "-nc", "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"])
    subprocess.run(["chmod", "+x", "cloudflared-linux-amd64"])

    # 強制清理舊執行環境
    os.system("mkdir -p /tmp/music_cf")
    os.system("rm -f music_cf.log")

    subprocess.Popen(['./cloudflared-linux-amd64', 'tunnel', '--url', 'http://127.0.0.1:8889', '--logfile', '/tmp/music_cf/music.log', '--metrics', '127.0.0.1:40002'], stdout=open('music_cf.log', 'w'), stderr=subprocess.STDOUT)

    # 🌟 優化的防呆迴圈，最多等待 15 秒
    url_match = None
    for _ in range(15):
        time.sleep(1)
        try:
            with open('music_cf.log', 'r') as f:
                log_content = f.read()
                url_match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", log_content)
                if url_match:
                    break
        except:
            pass

    if url_match:
        print("✅ 成功！這是你的音樂版專屬公開網址：")
        print(f"👉 {url_match.group(0)}")
    else:
        print("❌ 網址獲取失敗。詳細日誌內容：")
        os.system("cat music_cf.log")
    print("="*60 + "\n")

if __name__ == '__main__':
    start_music_server()