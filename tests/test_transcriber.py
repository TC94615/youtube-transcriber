import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
import youtube_transcriber

class TestTranscriber:
    # 測試 Whisper 引擎轉錄        
    def test_transcribe_with_whisper(self, monkeypatch):
        tmp_dir = Path("/tmp")
        monkeypatch.setattr("youtube_transcriber.downloader.download_audio", lambda url, tmp_dir: str(tmp_dir / "test.mp3"))
        
        mock_detect_language = Mock(return_value="en")
        monkeypatch.setattr("youtube_transcriber.transcriber.detect_language", mock_detect_language)
    
        def mock_whisper(audio_file, output_dir, model_size="base", language=None):
            return tmp_dir / "test.txt", tmp_dir / "test.srt"
        monkeypatch.setattr("youtube_transcriber.transcriber.transcribe_with_whisper", mock_whisper)
        
        result = youtube_transcriber.transcriber.transcribe_youtube_video(url="http://test.com", output_dir=tmp_dir, engine="whisper", language="en")
        assert result[0] == tmp_dir / "test.txt"
        assert result[1] == tmp_dir / "test.srt"
        mock_detect_language.assert_not_called()
    
    # 測試 Funsar 引擎轉錄        
    def test_transcribe_with_funasr(self, monkeypatch):
        tmp_dir = Path("/tmp")
        mock_audio_file = str(tmp_dir / "test.mp3")
        monkeypatch.setattr("youtube_transcriber.downloader.download_audio", lambda url, tmp_dir: mock_audio_file)
        monkeypatch.setattr("youtube_transcriber.transcriber.detect_language", lambda audio_file: "zh")
        def mock_funasr(audio_file, output_dir, model_type="paraformer-zh"):            
            return str(tmp_dir / "test.txt"), str(tmp_dir / "test.srt")
        monkeypatch.setattr("youtube_transcriber.transcriber.transcribe_with_funasr", mock_funasr)
        result = youtube_transcriber.transcriber.transcribe_youtube_video("http://test.com", tmp_dir, language="zh", engine="funasr")
        assert Path(result[0]) == tmp_dir / "test.txt"
        assert Path(result[1]) == tmp_dir / "test.srt"

    # 測試自動引擎選擇（中文）
    def test_auto_engine_selection_chinese(self, monkeypatch):
        tmp_dir = Path("/tmp")
        mock_audio_file = str(tmp_dir / "test.mp3")
        monkeypatch.setattr("youtube_transcriber.downloader.download_audio", lambda url, tmp_dir: mock_audio_file)
        monkeypatch.setattr("youtube_transcriber.transcriber.detect_language", lambda audio_file: "zh")
        def mock_funasr(audio_file, output_dir, model_type="paraformer-zh"):
            return str(tmp_dir / "test.txt"), str(tmp_dir / "test.srt")
        monkeypatch.setattr("youtube_transcriber.transcriber.transcribe_with_funasr", mock_funasr)
        def mock_whisper(*args, **kwargs):
            raise AssertionError("Whisper 不應被呼叫")
        monkeypatch.setattr("youtube_transcriber.transcriber.transcribe_with_whisper", mock_whisper)
        result = youtube_transcriber.transcriber.transcribe_youtube_video("http://test.com", tmp_dir)
        assert Path(result[0]) == tmp_dir / "test.txt"
        assert Path(result[1]) == tmp_dir / "test.srt"

    # 測試自動引擎選擇（英文）
    def test_auto_engine_selection_english(self, monkeypatch):
        tmp_dir = Path("/tmp")
        mock_audio_file = str(tmp_dir / "test.mp3")
        monkeypatch.setattr("youtube_transcriber.downloader.download_audio", lambda url, tmp_dir: mock_audio_file)
        monkeypatch.setattr("youtube_transcriber.transcriber.detect_language", lambda audio_file: "en")
        def mock_funasr(*args, **kwargs):
            raise AssertionError("FunASR 不應被呼叫")
        monkeypatch.setattr("youtube_transcriber.transcriber.transcribe_with_funasr", mock_funasr)
        def mock_whisper(audio_file, output_dir, model_size="base", language=None):
            return str(tmp_dir / "test.txt"), str(tmp_dir / "test.srt")
        monkeypatch.setattr("youtube_transcriber.transcriber.transcribe_with_whisper", mock_whisper)
        result = youtube_transcriber.transcriber.transcribe_youtube_video("http://test.com", tmp_dir)
        assert Path(result[0]) == tmp_dir / "test.txt"
        assert Path(result[1]) == tmp_dir / "test.srt"

    # 測試下載失敗
    def test_transcribe_download_failure(self, monkeypatch):
        def raise_download(*args, **kwargs):
            raise Exception("下載錯誤")
        monkeypatch.setattr("youtube_transcriber.downloader.download_audio", raise_download)
        with pytest.raises(Exception, match="下載錯誤"):
            youtube_transcriber.transcriber.transcribe_youtube_video("http://test.com", Path("/tmp"), "whisper")

    # 測試語言檢測功能
    def test_detect_language(self, monkeypatch):  
        # 創建模擬的 model 物件  
        mock_model = MagicMock()  
        mock_model.detect_language = MagicMock(return_value=(None, {"en": 0.8, "zh": 0.2}))  
        
        # 設置 load_model 返回我們的模擬 model  
        monkeypatch.setattr("whisper.load_model", MagicMock(return_value=mock_model))  
        monkeypatch.setattr("whisper.load_audio", MagicMock())  
        monkeypatch.setattr("whisper.pad_or_trim", MagicMock())  
    
        mock_mel = MagicMock()  
        mock_mel.to = MagicMock(return_value=mock_mel)  
        monkeypatch.setattr("whisper.log_mel_spectrogram", MagicMock(return_value=mock_mel))  
        
        result = youtube_transcriber.transcriber.detect_language(Path("/tmp/test.mp3"))  
        assert result == "en"