import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from youtube_transcriber.whisper_engine import transcribe_with_whisper

class TestWhisperEngine:    
    @patch("whisper.load_model")
    def test_transcribe_success(self, mock_load, tmp_path): # <-- 加入 tmp_path fixture
        """測試語音轉錄成功的情況"""
        # 設置mock
        mock_model = MagicMock()
        # <-- 讓 mock 回傳值包含 segments 以測試 SRT 生成
        mock_model.transcribe.return_value = {
            "text": "測試轉錄結果",
            "segments": [
                {"start": 0.0, "end": 1.0, "text": "第一句"},
                {"start": 1.5, "end": 2.5, "text": "第二句"}
            ]
        }
        mock_load.return_value = mock_model
        
        # 調用測試
        output_dir = tmp_path # <-- 使用 tmp_path
        text_path, srt_path = transcribe_with_whisper("test.mp3", output_dir)
        
        # 驗證結果
        assert Path(text_path) == output_dir / "test.txt"
        assert Path(srt_path) == output_dir / "test.srt"
        mock_model.transcribe.assert_called_once()

        # <-- 增加檔案內容驗證
        assert (output_dir / "test.txt").read_text(encoding="utf-8") == "測試轉錄結果"
        expected_srt_content = (
            "1\n00:00:00,000 --> 00:00:01,000\n第一句\n\n"
            "2\n00:00:01,500 --> 00:00:02,500\n第二句\n\n"
        )
        assert (output_dir / "test.srt").read_text(encoding="utf-8") == expected_srt_content
        
    @patch("whisper.load_model", side_effect=Exception("模擬錯誤"))
    def test_transcribe_exception(self, mock_load, tmp_path): # <-- 加入 tmp_path fixture
        """測試轉錄拋出異常的情況"""
        with pytest.raises(Exception, match="模擬錯誤"):
            transcribe_with_whisper("test.mp3", tmp_path) # <-- 使用 tmp_path