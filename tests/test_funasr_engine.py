import pytest
import modelscope
from pathlib import Path
from unittest.mock import patch, MagicMock
from youtube_transcriber.funasr_engine import transcribe_with_funasr

class TestFunASREngine:
    @patch("modelscope.pipelines.pipeline")
    def test_transcribe_success(self, mock_pipeline, tmp_path): # <-- 加入 tmp_path fixture
        """測試語音轉錄成功的情況"""
        # 設置mock
        mock_result = {"text": "測試轉錄結果"}
        mock_pipeline.return_value = MagicMock(return_value=mock_result)
        
        # 調用測試
        output_dir = tmp_path # <-- 使用 tmp_path
        text_path, srt_path = transcribe_with_funasr("test.mp3", output_dir)
        
        # 驗證結果
        assert Path(text_path) == output_dir / "test.txt"
        assert Path(srt_path) == output_dir / "test.srt"
        mock_pipeline.assert_called_once()

        # <-- 增加檔案內容驗證
        assert (output_dir / "test.txt").read_text(encoding="utf-8") == "測試轉錄結果"
        expected_srt_content = "1\n00:00:00,000 --> 99:59:59,999\n測試轉錄結果\n\n"
        assert (output_dir / "test.srt").read_text(encoding="utf-8") == expected_srt_content
    
    @patch('modelscope.pipelines.pipeline')
    def test_transcribe_empty_result(self, mock_pipeline, tmp_path): # <-- 加入 tmp_path fixture
        """測試轉錄返回空結果的情況"""
        # 設置mock
        mock_pipeline.return_value = MagicMock(return_value=[])
        
        # 驗證異常
        with pytest.raises(ValueError, match="FunASR 返回空的 list"):
            transcribe_with_funasr("test.mp3", tmp_path) # <-- 使用 tmp_path