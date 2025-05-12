import yt_dlp
from pathlib import Path
import os
import re

def sanitize_filename(title):
    """清理非法檔名字符，並將空格替換為底線"""
    # 先將所有空格替換為底線
    title = title.replace(" ", "_")
    
    # 移除 Windows 不支援的字符：\/:*?"<>|
    sanitized = re.sub(r'[\\/:*?"<>|]', "", title)
    
    return sanitized.strip()


def download_audio(url, output_dir):
    print(f"正在從 {url} 下載音頻...")

    # 先獲取影片資訊但不下載
    ydl = yt_dlp.YoutubeDL()
    info = ydl.extract_info(url, download=False)
    original_title = info['title']
    base_filename = sanitize_filename(original_title)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': str(Path(output_dir) / base_filename),  # 使用清理過的檔名
        'quiet': False,
        'no_warnings': False
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        print(f"原始標題: {original_title}")
        print(f"安全檔名: {base_filename}")
        audio_file = str(Path(output_dir) / f"{base_filename}.mp3")
        return audio_file