import pytest
import yt_dlp
from pathlib import Path
from unittest.mock import patch, MagicMock
from youtube_transcriber.downloader import download_audio, sanitize_filename

class TestDownloader:
    def test_sanitize_filename(self):
        """測試清理非法檔名字符的功能"""
        # 測試空格替換
        assert sanitize_filename("test video") == "test_video"
        # 測試非法字符移除
        assert sanitize_filename("test/video*name?") == "testvideoname"
        # 測試混合情況
        assert sanitize_filename("test/video name*") == "testvideo_name"
    
    @patch("yt_dlp.YoutubeDL")
    def test_download_audio(self, mock_ydl):
        """測試音頻下載功能"""
        # 設置mock
        mock_instance = MagicMock()
        mock_ydl.return_value = mock_instance
        
        # 模擬extract_info返回
        mock_info = {
            'title': 'test video',
            'formats': [{'format_id': 'bestaudio'}]
        }
        mock_instance.extract_info.return_value = mock_info
        
        # 設置mock以替換with語句中的YoutubeDL
        mock_ydl.return_value.__enter__.return_value = mock_instance
        
        # 調用測試
        output_dir = Path("tmp")  
        result = download_audio("http://test.com", output_dir)
        
        # 驗證結果
        assert Path(result) == output_dir / "test_video.mp3"
        mock_instance.download.assert_called_once()
        mock_instance.extract_info.assert_called_once()