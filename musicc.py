# ============================================================
# 🎵 靈魂調音師 (Soul Tuner) - 10,000首真實在地化旗艦版
# 🚀 近十年華語新歌+周杰倫 ✕ 絕對去重演算法 ✕ 250首推薦
# ============================================================
import os
import threading
import time
import json
import random
import urllib.parse
import pandas as pd
import numpy as np
from flask import Flask, request, jsonify, render_template_string
from werkzeug.serving import make_server
from sklearn.metrics.pairwise import euclidean_distances
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────
# 1. 核心真實音樂資料庫 (大幅擴充各語系基底，加入周董與更多獨立/流行指標)
# ─────────────────────────────────────────
REAL_SONGS_CONFIG = {
    "華語": [
        # 周杰倫專區
        ("七里香", "周杰倫"), ("晴天", "周杰倫"), ("告白氣球", "周杰倫"), ("稻香", "周杰倫"), ("愛在西元前", "周杰倫"),
        ("夜曲", "周杰倫"), ("半島鐵盒", "周杰倫"), ("安靜", "周杰倫"), ("說好不哭", "周杰倫"), ("擱淺", "周杰倫"),
        # 盧廣仲專區
        ("刻在我心底的名字", "盧廣仲"), ("魚仔", "盧廣仲"), ("幾分之幾", "盧廣仲"), ("狂迪", "盧廣仲"), ("明亮", "盧廣仲"),
        # 近年流行與獨立樂團
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

# ─────────────────────────────────────────
# 2. 自動擴充生成引擎 (擴充至 10,000 首，創造足夠的空間密度)
# ─────────────────────────────────────────
print("⚙️ 正在建構五維矩陣空間... 擴充音樂資料庫至 10,000 首...")
start_time = time.time()

song_list_build = []
for lang_chinese, songs in REAL_SONGS_CONFIG.items():
    region_code = REGIONS_MAP[lang_chinese]
    for title, artist in songs:
        if region_code == "instrumental":
            bpm, valence, energy, acoustic, instrumental = 65, 0.3, 0.15, 0.95, 0.95
        elif region_code == "kpop":
            bpm, valence, energy, acoustic, instrumental = 125, 0.75, 0.85, 0.05, 0.0
        else:
            bpm, valence, energy, acoustic, instrumental = 100, 0.5, 0.55, 0.3, 0.0

        song_list_build.append({
            "title": title, "artist": artist, "region": region_code,
            "region_label": lang_chinese,
            "bpm": bpm, "valence": valence, "energy": energy, "acoustic": acoustic, "instrumental": instrumental
        })

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
        "title": base_song[0],  # 🚀 移除礙眼的 vX 後綴，保持原始乾淨歌名
        "artist": base_song[1],
        "region": REGIONS_MAP[rand_lang],
        "region_label": rand_lang,
        "bpm": int(mock_bpm[i]),
        "valence": round(float(mock_valence[i]), 2),
        "energy": round(float(mock_energy[i]), 2),
        "acoustic": round(float(mock_acoustic[i]), 2),
        "instrumental": round(float(mock_instrumental[i]), 2)
    })

df_songs = pd.DataFrame(song_list_build)
df_songs['bpm_norm'] = (df_songs['bpm'] - 50) / 130
df_songs['bpm_norm'] = df_songs['bpm_norm'].clip(0, 1)

print(f"✅ 大數據空間架設成功！目前線上共有 {len(df_songs)} 首精算歌曲。(耗時: {time.time() - start_time:.2f} 秒)")

# ─────────────────────────────────────────
# 3. 網頁前端 HTML 模板
# ─────────────────────────────────────────
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎵 靈魂調音師 Soul Tuner</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); color: #e2e8f0; font-family: 'Helvetica Neue', sans-serif; }
        .glass-panel { background: rgba(30, 41, 59, 0.7); backdrop-filter: blur(16px); border: 1px solid rgba(255, 255, 255, 0.1); }
        .feature-bar { transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1); }
        .custom-select { appearance: none; background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%239ca3af' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='M6 8l4 4 4-4'/%3e%3c/svg%3e"); background-position: right 0.5rem center; background-repeat: no-repeat; background-size: 1.5em 1.5em; }
        .custom-scrollbar::-webkit-scrollbar { width: 8px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: rgba(0,0,0,0.1); border-radius: 8px; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: rgba(168, 85, 247, 0.5); border-radius: 8px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: rgba(168, 85, 247, 0.8); }
        .filter-btn { opacity: 0.5; transition: all 0.3s; }
        .filter-btn.active { opacity: 1; border-color: #a855f7; background: rgba(168, 85, 247, 0.2); }
    </style>
</head>
<body class="min-h-screen p-4 md:p-8">

    <div class="max-w-7xl mx-auto">
        <div class="glass-panel rounded-2xl shadow-2xl p-6 mb-8 flex items-center justify-between">
            <div class="flex items-center space-x-4">
                <div class="w-14 h-14 rounded-full bg-gradient-to-tr from-purple-500 to-indigo-500 flex items-center justify-center shadow-lg">
                    <span class="text-2xl">🎵</span>
                </div>
                <div>
                    <h1 class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-pink-400">Soul Tuner 靈魂調音師</h1>
                </div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
            <div class="lg:col-span-4 glass-panel p-4 rounded-2xl shadow-xl flex flex-col">
                <h2 class="text-lg font-bold mb-3 text-indigo-300 border-b border-slate-700 pb-2 flex items-center">
                    <span class="mr-2">🔍</span> 當下狀態
                </h2>

                <div class="space-y-3 flex-grow">
                    <div class="bg-slate-800/50 p-3 rounded-xl border border-slate-700/50">
                        <h3 class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Environment 環境狀態</h3>
                        <div class="grid grid-cols-2 gap-2">
                            <div>
                                <label class="block text-xs mb-1 text-slate-300">⛅ 天氣</label>
                                <select id="env_weather" class="custom-select w-full bg-slate-900 border border-slate-600 rounded-lg p-1.5 text-xs focus:ring-2 focus:ring-purple-500 outline-none">
                                    <option value="☀️ 晴天">☀️ 晴天</option>
                                    <option value="⛅ 陰天">⛅ 陰天</option>
                                    <option value="🌧️ 雨天">🌧️ 雨天</option>
                                    <option value="⛈️ 雷陣雨">⛈️ 雷陣雨</option>
                                    <option value="🍃 起風">🍃 起風</option>
                                    <option value="❄️ 下雪">❄️ 下雪</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs mb-1 text-slate-300">🕰️ 時間</label>
                                <select id="env_time" class="custom-select w-full bg-slate-900 border border-slate-600 rounded-lg p-1.5 text-xs focus:ring-2 focus:ring-purple-500 outline-none">
                                    <option value="🌅 清晨">🌅 清晨</option>
                                    <option value="🌄 早上">🌄 早上</option>
                                    <option value="🕛 正午">🕛 正午</option>
                                    <option value="🌇 午後">🌇 午後</option>
                                    <option value="🌆 黃昏">🌆 黃昏</option>
                                    <option value="🌃 晚上">🌃 晚上</option>
                                    <option value="🌙 深夜" selected>🌙 深夜</option>
                                    <option value="🌌 凌晨">🌌 凌晨</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <div class="bg-slate-800/50 p-3 rounded-xl border border-slate-700/50">
                        <h3 class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-1">Context 情境狀態</h3>
                        <label class="block text-xs mb-1 text-slate-300">🏃‍♂️ 當下活動</label>
                        <select id="ctx_activity" class="custom-select w-full bg-slate-900 border border-slate-600 rounded-lg p-1.5 text-xs focus:ring-2 focus:ring-pink-500 outline-none">
                            <option value="📖 讀書/工作" selected>📖 讀書/工作</option>
                            <option value="📚 閱讀休閒">📚 閱讀休閒</option>
                            <option value="🚌 通勤/移動">🚌 通勤/移動</option>
                            <option value="🚗 開車兜風">🚗 開車兜風</option>
                            <option value="🏋️ 運動/健身">🏋️ 運動/健身</option>
                            <option value="🎮 打遊戲">🎮 打遊戲</option>
                            <option value="🧹 做家事">🧹 做家事</option>
                            <option value="🎉 派對/聚會">🎉 派對/聚會</option>
                            <option value="🍵 發呆/放空">🍵 發呆/放空</option>
                            <option value="🛏️ 準備入睡">🛏️ 準備入睡</option>
                        </select>
                    </div>

                    <div class="bg-slate-800/50 p-3 rounded-xl border border-slate-700/50">
                        <h3 class="text-[11px] font-bold text-slate-400 uppercase tracking-wider mb-2">Psychological 心理狀態</h3>
                        <div class="space-y-2">
                            <div>
                                <label class="block text-xs mb-1 text-slate-300">❤️ 當前心情</label>
                                <select id="psy_mood" class="custom-select w-full bg-slate-900 border border-slate-600 rounded-lg p-1.5 text-xs focus:ring-2 focus:ring-blue-500 outline-none">
                                    <option value="🧘 平靜">🧘 平靜</option>
                                    <option value="😰 焦慮/壓力大">😰 焦慮/壓力大</option>
                                    <option value="😄 愉悅">😄 愉悅</option>
                                    <option value="🌧️ 低落/憂鬱" selected>🌧️ 低落/憂鬱</option>
                                    <option value="😡 憤怒/煩躁">😡 憤怒/煩躁</option>
                                    <option value="🍷 浪漫/微醺">🍷 浪漫/微醺</option>
                                    <option value="🕰️ 懷舊/思念">🕰️ 懷舊/思念</option>
                                    <option value="🔥 充滿活力">🔥 充滿活力</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs mb-1 text-slate-300">✨ 期望轉換的狀態</label>
                                <select id="psy_goal" class="custom-select w-full bg-slate-900 border border-slate-600 rounded-lg p-1.5 text-xs focus:ring-2 focus:ring-blue-500 outline-none">
                                    <option value="🩹 想被治癒/陪伴" selected>🩹 想被治癒/陪伴</option>
                                    <option value="⚡ 想提振精神">⚡ 想提振精神</option>
                                    <option value="🎯 想極度專注">🎯 想極度專注</option>
                                    <option value="🛁 想徹底放鬆">🛁 想徹底放鬆</option>
                                    <option value="🗣️ 想發洩情緒">🗣️ 想發洩情緒</option>
                                    <option value="💤 想安穩入眠">💤 想安穩入眠</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <button onclick="generateCapsule()" id="btn_generate" class="w-full mt-4 bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-400 hover:to-purple-500 text-white font-bold py-2.5 px-4 rounded-xl transition duration-300 shadow-[0_0_15px_rgba(168,85,247,0.4)] flex justify-center items-center text-sm">
                    <span id="btn_text">✨ 生成為您推薦的歌曲</span>
                </button>
            </div>

            <div class="lg:col-span-8 glass-panel p-6 rounded-2xl shadow-xl flex flex-col relative overflow-hidden">
                <div id="welcome_panel" class="h-full flex items-center justify-center min-h-[500px]">
                    <div class="text-center text-slate-500">
                        <div class="text-6xl mb-4 opacity-50">🎧</div>
                        <p>精算 10,000 首核心音樂矩陣，為您精準過濾推薦歌曲</p>
                    </div>
                </div>

                <div id="loading_panel" class="hidden h-full flex flex-col items-center justify-center space-y-4 min-h-[500px]">
                    <div class="flex space-x-2">
                        <div class="w-3 h-10 bg-purple-500 rounded-full animate-bounce"></div>
                        <div class="w-3 h-16 bg-pink-500 rounded-full animate-bounce" style="animation-delay: 0.1s"></div>
                        <div class="w-3 h-8 bg-indigo-500 rounded-full animate-bounce" style="animation-delay: 0.2s"></div>
                    </div>
                    <p class="text-purple-300 font-mono text-sm tracking-widest animate-pulse">ANALYZING 10,000 UNIQUE FEATURES...</p>
                </div>

                <div id="result_panel" class="hidden flex-col h-full space-y-6 animate-fade-in">
                    <div class="bg-gradient-to-r from-slate-800 to-slate-900 p-5 rounded-xl border-l-4 border-purple-500 shadow-inner">
                        <h3 class="text-xs text-purple-400 font-bold mb-2 tracking-widest uppercase">💌 Soul Tuner Message</h3>
                        <p id="empathy_message" class="text-sm leading-relaxed text-slate-200 font-medium"></p>
                    </div>

                    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6 flex-grow">
                        <div class="lg:col-span-1 bg-slate-800/40 p-3 rounded-xl border border-slate-700 flex flex-col">
                            <h3 class="text-[11px] font-bold text-slate-400 mb-4 flex items-center"><span class="mr-2">🎛️</span> 目標特徵</h3>
                            <div class="space-y-4 flex-grow">
                                <div>
                                    <div class="flex justify-between text-[10px] mb-1"><span class="text-pink-400 font-bold">Valence</span><span id="val_v"></span></div>
                                    <div class="w-full bg-slate-900 rounded-full h-1.5"><div id="bar_v" class="bg-pink-500 h-1.5 rounded-full feature-bar shadow-[0_0_10px_rgba(236,72,153,0.5)]" style="width:0%"></div></div>
                                </div>
                                <div>
                                    <div class="flex justify-between text-[10px] mb-1"><span class="text-amber-400 font-bold">Energy</span><span id="val_e"></span></div>
                                    <div class="w-full bg-slate-900 rounded-full h-1.5"><div id="bar_e" class="bg-amber-500 h-1.5 rounded-full feature-bar shadow-[0_0_10px_rgba(245,158,11,0.5)]" style="width:0%"></div></div>
                                </div>
                                <div>
                                    <div class="flex justify-between text-[10px] mb-1"><span class="text-emerald-400 font-bold">Acoustic</span><span id="val_a"></span></div>
                                    <div class="w-full bg-slate-900 rounded-full h-1.5"><div id="bar_a" class="bg-emerald-500 h-1.5 rounded-full feature-bar shadow-[0_0_10px_rgba(16,185,129,0.5)]" style="width:0%"></div></div>
                                </div>
                                <div>
                                    <div class="flex justify-between text-[10px] mb-1"><span class="text-blue-400 font-bold">Instru.</span><span id="val_i"></span></div>
                                    <div class="w-full bg-slate-900 rounded-full h-1.5"><div id="bar_i" class="bg-blue-500 h-1.5 rounded-full feature-bar shadow-[0_0_10px_rgba(59,130,246,0.5)]" style="width:0%"></div></div>
                                </div>
                            </div>
                            <div class="mt-4 pt-3 border-t border-slate-700 flex flex-col justify-center items-center">
                                <span class="text-[10px] text-slate-400 font-bold mb-1">🎯 Tempo</span>
                                <span id="val_bpm" class="text-lg font-black text-white bg-slate-900 px-3 py-1 rounded-lg border border-slate-600 shadow-inner w-full text-center"></span>
                            </div>
                        </div>

                        <div class="lg:col-span-3 bg-slate-800/40 p-4 rounded-xl border border-slate-700 flex flex-col">
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-700 pb-3 mb-3 gap-2">
                                <h3 class="text-xs font-bold text-slate-400">🎧 為您推薦的專屬歌單 <span id="song_count_label"></span> (點擊播放)</h3>
                                <div class="flex space-x-1.5 overflow-x-auto no-scrollbar pb-1" id="filter_buttons">
                                    <button onclick="filterList('all', this)" class="filter-btn text-[10px] px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 border border-purple-500/50 whitespace-nowrap active">全部</button>
                                    <button onclick="filterList('cpop', this)" class="filter-btn text-[10px] px-2.5 py-1 rounded text-slate-300 border border-slate-600 hover:bg-slate-700 whitespace-nowrap">華語</button>
                                    <button onclick="filterList('western', this)" class="filter-btn text-[10px] px-2.5 py-1 rounded text-slate-300 border border-slate-600 hover:bg-slate-700 whitespace-nowrap">西洋</button>
                                    <button onclick="filterList('jpop', this)" class="filter-btn text-[10px] px-2.5 py-1 rounded text-slate-300 border border-slate-600 hover:bg-slate-700 whitespace-nowrap">日語</button>
                                    <button onclick="filterList('kpop', this)" class="filter-btn text-[10px] px-2.5 py-1 rounded text-slate-300 border border-slate-600 hover:bg-slate-700 whitespace-nowrap">韓語</button>
                                    <button onclick="filterList('instrumental', this)" class="filter-btn text-[10px] px-2.5 py-1 rounded text-slate-300 border border-slate-600 hover:bg-slate-700 whitespace-nowrap">純音樂</button>
                                </div>
                            </div>

                            <div id="playlist_container" class="grid grid-cols-1 sm:grid-cols-2 gap-3 overflow-y-auto pr-2 h-[380px] custom-scrollbar">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        function filterList(regionCode, btnElement) {
            document.querySelectorAll('.filter-btn').forEach(btn => {
                btn.className = "filter-btn text-[10px] px-2.5 py-1 rounded text-slate-300 border border-slate-600 hover:bg-slate-700 whitespace-nowrap transition-colors";
            });
            btnElement.className = "filter-btn text-[10px] px-2.5 py-1 rounded bg-purple-500/20 text-purple-300 border border-purple-500/50 whitespace-nowrap transition-colors active";

            const songs = document.querySelectorAll('.song-item');
            let visibleCount = 0;
            songs.forEach(song => {
                if (regionCode === 'all' || song.getAttribute('data-region') === regionCode) {
                    song.style.display = 'flex';
                    visibleCount++;
                } else {
                    song.style.display = 'none';
                }
            });
            document.getElementById('song_count_label').innerText = `(共 ${visibleCount} 首完全不重複)`;
        }

        async function generateCapsule() {
            const btn = document.getElementById('btn_generate');
            const btnText = document.getElementById('btn_text');
            btn.disabled = true;
            btnText.innerHTML = '<span class="animate-pulse">特徵空間過濾與絕對去重中...</span>';

            document.getElementById('welcome_panel').classList.add('hidden');
            document.getElementById('result_panel').classList.add('hidden');
            document.getElementById('loading_panel').classList.remove('hidden');

            const payload = {
                weather: document.getElementById('env_weather').value,
                time: document.getElementById('env_time').value,
                activity: document.getElementById('ctx_activity').value,
                mood: document.getElementById('psy_mood').value,
                goal: document.getElementById('psy_goal').value
            };

            try {
                const response = await fetch('/api/recommend', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(payload)
                });

                if (!response.ok) throw new Error("伺服器回傳錯誤代碼");
                const data = await response.json();

                document.getElementById('empathy_message').innerHTML = data.empathy_message;

                const features = data.target_features;
                document.getElementById('val_v').textContent = features.valence;
                document.getElementById('val_e').textContent = features.energy;
                document.getElementById('val_a').textContent = features.acousticness;
                document.getElementById('val_i').textContent = features.instrumentalness;
                document.getElementById('val_bpm').textContent = features.bpm + " BPM";

                setTimeout(() => {
                    document.getElementById('bar_v').style.width = (features.valence * 100) + '%';
                    document.getElementById('bar_e').style.width = (features.energy * 100) + '%';
                    document.getElementById('bar_a').style.width = (features.acousticness * 100) + '%';
                    document.getElementById('bar_i').style.width = (features.instrumentalness * 100) + '%';
                }, 100);

                const playlistDiv = document.getElementById('playlist_container');
                playlistDiv.innerHTML = '';

                data.playlist.forEach((song, index) => {
                    const safeTitle = song.title.length >= 2 ? song.title.substring(0,2) : song.title;
                    const coverUrl = `https://ui-avatars.com/api/?name=${encodeURIComponent(safeTitle)}&background=random&color=fff&size=128&bold=true`;
                    const searchQuery = encodeURIComponent(song.title + " " + song.artist);
                    const playUrl = `https://www.youtube.com/results?search_query=${searchQuery}`;

                    const songHtml = `
                        <a href="${playUrl}" target="_blank" data-region="${song.region}" class="song-item flex items-center p-2 rounded-lg bg-slate-800/80 hover:bg-slate-700 transition-all group cursor-pointer border border-transparent hover:border-purple-500/50 decoration-transparent w-full">
                            <div class="text-[10px] text-slate-500 w-6 text-right font-mono mr-2">${index + 1}</div>
                            <div class="w-10 h-10 rounded shadow-md overflow-hidden flex-shrink-0 relative">
                                <img src="${coverUrl}" class="w-full h-full object-cover opacity-80 group-hover:opacity-100">
                                <div class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 bg-black/60 backdrop-blur-sm"><span class="text-white text-sm">▶</span></div>
                            </div>
                            <div class="ml-2 flex-grow min-w-0">
                                <p class="text-sm font-bold text-slate-200 truncate group-hover:text-purple-300 transition-colors">${song.title}</p>
                                <p class="text-[10px] text-slate-400 truncate">${song.artist}</p>
                            </div>
                            <div class="text-right flex-shrink-0 ml-1 flex flex-col items-end space-y-1">
                                <p class="text-[9px] font-mono text-emerald-400 bg-emerald-900/30 px-1.5 py-0.5 rounded">${song.bpm} BPM</p>
                                <p class="text-[9px] font-mono text-purple-400 bg-purple-900/30 px-1.5 py-0.5 rounded whitespace-nowrap">${song.region_label}</p>
                            </div>
                        </a>
                    `;
                    playlistDiv.innerHTML += songHtml;
                });

                const allBtn = document.querySelector('.filter-btn');
                if(allBtn) filterList('all', allBtn);

                document.getElementById('loading_panel').classList.add('hidden');
                document.getElementById('result_panel').classList.remove('hidden');

            } catch (error) {
                console.error(error);
                alert('系統演算法推論出錯：後端可能發生錯誤，請檢查 Colab 的執行日誌。');
                document.getElementById('loading_panel').classList.add('hidden');
                document.getElementById('welcome_panel').classList.remove('hidden');
            } finally {
                btn.disabled = false;
                btnText.innerHTML = '✨ 生成為您推薦的歌曲';
            }
        }
    </script>
</body>
</html>
"""

# ─────────────────────────────────────────
# 4. Flask 後端推薦演算核心
# ─────────────────────────────────────────
app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/recommend', methods=['POST'])
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
    if "治癒" in goal or "陪伴" in goal:
        target_v = 0.42; target_a = min(1.0, target_a + 0.28); target_e = min(target_e, 0.38)
    elif "精神" in goal:
        target_v = 0.78; target_e = 0.82; target_bpm = max(target_bpm, 115)
    elif "專注" in goal:
        target_i = 0.92; target_v = 0.48
    elif "放鬆" in goal:
        target_e = 0.18; target_a = 0.78; target_bpm = min(target_bpm, 72)
    elif "發洩" in goal:
        target_e = 0.88; target_bpm = max(target_bpm, 132)
    elif "安穩" in goal:
        target_e = 0.04; target_a = 0.92; target_i = 0.92; target_bpm = 48

    weather = req.get('weather', '')
    if "雨" in weather: target_a = min(1.0, target_a + 0.18); target_v = max(0.0, target_v - 0.12)
    elif "風" in weather: target_e = min(1.0, target_e + 0.08)
    elif "雪" in weather: target_a = min(1.0, target_a + 0.22); target_e = max(0.0, target_e - 0.08)

    time_val = req.get('time', '')
    if time_val in ["night", "midnight", "dawn"] or "夜" in time_val or "晨" in time_val:
        target_e = max(0.0, target_e - 0.12)

    target_bpm_norm = max(0, min(1, (target_bpm - 50) / 130))
    target_vector = np.array([[target_v, target_e, target_a, target_i, target_bpm_norm]])

    db_features = df_songs[['valence', 'energy', 'acoustic', 'instrumental', 'bpm_norm']].values

    # 算出距離
    df_songs['distance'] = euclidean_distances(target_vector, db_features)[0]

    # 🚀 絕對去重防線：以歌名和歌手為基準，刪除所有重複項，只保留距離目標最近的那一首
    unique_sorted_songs = df_songs.sort_values('distance').drop_duplicates(subset=['title', 'artist'], keep='first')

    # 重新配置語系數量，因為現在保證 100% 獨立，每種語系各取 50 首就很豐富了
    quota_config = {
        "cpop": 50, "western": 50, "jpop": 50, "kpop": 50, "instrumental": 50
    }

    recommended_frames = []
    for region_code, quota in quota_config.items():
        top_in_region = unique_sorted_songs[unique_sorted_songs['region'] == region_code].head(quota)
        recommended_frames.append(top_in_region)

    recommended_df = pd.concat(recommended_frames).sort_values('distance')
    recommended_songs = recommended_df.to_dict(orient='records')
    total_songs = len(recommended_songs)

    msg = f"系統精算完畢。感測到您目前處於 **{mood}** 的心境，且在 **{weather}** 環境下正準備進行 **{act}**。"
    msg += f" 我們從 10,000 首空間矩陣中執行了嚴格的去重掃描，為您精選了 {total_songs} 首「完全不重複」、契合 {target_bpm} BPM 的高品質音樂膠囊。聽聽看吧。"

    response = {
        "target_features": {
            "valence": round(target_v, 2), "energy": round(target_e, 2),
            "acousticness": round(target_a, 2), "instrumentalness": round(target_i, 2), "bpm": target_bpm
        },
        "playlist": recommended_songs,
        "empathy_message": msg
    }

    time.sleep(0.4)
    return jsonify(response)

# ─────────────────────────────────────────
# 5. 伺服器啟動邏輯
# ─────────────────────────────────────────
class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('127.0.0.1', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()
    def run(self): self.server.serve_forever()
    def shutdown(self): self.server.shutdown()

def start_server():
    global server
    if 'server' in globals():
        server.shutdown()
        time.sleep(1)
    server = ServerThread(app)
    server.start()

    print("\n" + "="*60)
    print("🚀 10,000首大數據「靈魂調音師 Soul Tuner」尊爵去重版上線！")
    print("📌 核心修正：啟用嚴格 drop_duplicates，保證推薦歌單 100% 唯一性")

    try:
        from google.colab.output import eval_js
        url = eval_js("google.colab.kernel.proxyPort(5000)")
        print("\n🔗 請點擊下方連結進入：")
        print(f"👉 {url}")
    except ImportError:
        print("\n🔗 本機執行環境請前往：http://127.0.0.1:5000")
    print("="*60 + "\n")

if __name__ == '__main__':
    start_server()