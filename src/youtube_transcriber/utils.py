import os
import shutil
import subprocess


def find_executable(name: str, common_paths: list = None) -> str | None:
    """
    在系統 PATH 和指定的常見路徑中查找可執行檔
    """
    # 先嘗試從 PATH 找
    path = shutil.which(name)
    if path:
        return path

    # 再嘗試常見安裝路徑
    if common_paths:
        for base_path in common_paths:
            exe_path = os.path.join(base_path, name + ".exe")
            if os.path.isfile(exe_path):
                return exe_path

    return None


def find_ffmpeg(common_ffmpeg_paths=None) -> dict | None:
    """
    嘗試自動偵測 ffmpeg 和 ffprobe 的位置
    回傳 yt-dlp 可用的 ffmpeg_location 選項
    """
    if common_ffmpeg_paths is None:
        common_ffmpeg_paths = [
            "C:/ffmpeg/bin",
            "C:/Program Files/ffmpeg/bin",
            "C:/Program Files (x86)/ffmpeg/bin",
            os.path.expanduser("~/ffmpeg/bin"),
        ]

    ffmpeg_path = find_executable("ffmpeg", common_ffmpeg_paths)
    ffprobe_path = find_executable("ffprobe", common_ffmpeg_paths)

    if ffmpeg_path and ffprobe_path:
        print(f"✅ 找到 ffmpeg: {ffmpeg_path}")
        print(f"✅ 找到 ffprobe: {ffprobe_path}")
        return {
            'ffmpeg': ffmpeg_path,
            'ffprobe': ffprobe_path,
            'ffmpeg_location': os.path.dirname(ffmpeg_path)
        }
    else:
        print("❌ 無法自動找到 ffmpeg 或 ffprobe")
        print("請手動安裝 ffmpeg 並將其加入系統 PATH，或設定 --ffmpeg-location 參數")
        return None


# 🔍 測試是否能正常呼叫 ffmpeg（可選）
def test_ffmpeg(ffprobe_path: str):
    try:
        result = subprocess.run([ffprobe_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print("🟢 ffprobe 已正確運作！")
        else:
            print("🔴 ffprobe 有問題，請檢查路徑或安裝狀態。")
    except Exception as e:
        print("⚠️ 測試失敗：", e)


# ✅ 使用範例
if __name__ == "__main__":
    ffmpeg_info = find_ffmpeg()

    if ffmpeg_info:
        ffmpeg_location = ffmpeg_info['ffmpeg_location']

        # 這個參數可以直接給 yt-dlp 使用
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'ffmpeg_location': ffmpeg_location,
            'outtmpl': './output/%(title)s.%(ext)s',
            'quiet': False,
        }

        # 可選：測試一下 ffprobe 是否可用
        test_ffmpeg(ffmpeg_info['ffprobe'])
    else:
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': './output/%(title)s.%(ext)s',
            'quiet': True,
        }
        print("⚠️ 注意：未找到 ffmpeg，後處理將無法使用！")

    # 把 ydl_opts 傳進你的下載函數中