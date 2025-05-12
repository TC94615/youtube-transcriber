import os
import whisper
from youtube_transcriber.logger import logger


def transcribe_with_whisper(audio_file, output_dir, model_size="base", language=None):
    logger.info(f"[Whisper] 使用 {model_size} 模型進行轉錄")
    model = whisper.load_model(model_size)
    result = model.transcribe(audio_file, language=language)

    base_filename = os.path.splitext(os.path.basename(audio_file))[0]
    text_path = os.path.join(output_dir, f"{base_filename}.txt")
    srt_path = os.path.join(output_dir, f"{base_filename}.srt")

    with open(text_path, "w", encoding="utf-8") as f:
        f.write(result["text"])

    # 寫入 SRT 檔案（簡單實作）
    with open(srt_path, "w", encoding="utf-8") as f:
        for i, seg in enumerate(result.get("segments", []), 1):
            start = format_timestamp(seg["start"])
            end = format_timestamp(seg["end"])
            f.write(f"{i}\n{start} --> {end}\n{seg['text'].strip()}\n\n")

    return text_path, srt_path


def format_timestamp(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{ms:03d}"
