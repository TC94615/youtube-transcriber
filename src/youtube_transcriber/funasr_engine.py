import os
from pathlib import Path
from modelscope.pipelines import pipeline as asr_pipeline
from modelscope.utils.constant import Tasks


def transcribe_with_funasr(audio_file, output_dir, model_type="paraformer-zh"):
    from modelscope.pipelines import pipeline as asr_pipeline
    from modelscope.utils.constant import Tasks

    # 模型 ID 映射表（可擴充）
    model_mapping = {
        "paraformer-zh": "damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch",
        "paraformer-zh-fast": "damo/speech_paraformer-large-contextual_asr_nat-zh-cn-16k-common-vocab8404-onnx",
    }

    model_id = model_mapping.get(model_type, model_mapping["paraformer-zh"])

    print(f"[FunASR] 使用模型 {model_type} 進行轉錄 (ID: {model_id})")
    inference_pipeline = asr_pipeline(
        task=Tasks.auto_speech_recognition, model=model_id
    )
    result = inference_pipeline(audio_file)

    base_filename = Path(audio_file).stem
    text_path = os.path.join(output_dir, f"{base_filename}.txt")
    srt_path = os.path.join(output_dir, f"{base_filename}.srt")

    # 處理可能為 list 的情況
    if isinstance(result, list):
        if len(result) == 0:
            raise ValueError("FunASR 返回空的 list，沒有任何轉錄結果")
        result = result[0]

    text_result = result.get("text", "").strip()

    # 寫入純文字
    with open(text_path, "w", encoding="utf-8") as f:
        f.write(text_result)

    # 寫入 SRT（簡單版本）
    with open(srt_path, "w", encoding="utf-8") as f:
        f.write("1\n00:00:00,000 --> 99:59:59,999\n")
        f.write(f"{text_result}\n\n")

    return text_path, srt_path