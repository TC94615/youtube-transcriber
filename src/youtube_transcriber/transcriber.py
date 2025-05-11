import os
import whisper
from youtube_transcriber.whisper_engine import transcribe_with_whisper
from youtube_transcriber.funasr_engine import transcribe_with_funasr


def detect_language(audio_file):
    """使用 Whisper tiny 模型檢測語言"""
    model = whisper.load_model("tiny")
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    detected_lang = max(probs, key=probs.get)
    print(f"檢測到語言: {detected_lang}")
    return detected_lang


def transcribe_youtube_video(
    url, output_dir, engine="auto", model_size="base", language=None, device="cpu"
):
    os.makedirs(output_dir, exist_ok=True)

    # 1. 下載音頻
    from youtube_transcriber.downloader import download_audio

    audio_file = download_audio(url, output_dir)

    # 2. 自動語言檢測 or 強制指定語言
    detected_lang = language if language else detect_language(audio_file)

    # 3. 根據語言或引擎選擇模型
    if engine == "auto":
        if detected_lang == "zh":
            return transcribe_with_funasr(
                audio_file, output_dir, model_type="paraformer-zh"
            )
        else:
            return transcribe_with_whisper(
                audio_file, output_dir, model_size, language=detected_lang
            )
    elif engine == "whisper":
        return transcribe_with_whisper(
            audio_file, output_dir, model_size, language=language
        )
    elif engine == "funasr":
        return transcribe_with_funasr(
            audio_file, output_dir, model_type="paraformer-zh"
        )
    else:
        raise ValueError(f"不支援的引擎類型: {engine}")
