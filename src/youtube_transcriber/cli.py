import argparse
from youtube_transcriber.transcriber import transcribe_youtube_video


def main():
    parser = argparse.ArgumentParser(description="YouTube 影片語音轉文字工具")
    parser.add_argument("url", help="YouTube 影片 URL")
    parser.add_argument("-o", "--output-dir", default="./output")
    parser.add_argument(
        "-e", "--engine", choices=["auto", "whisper", "funasr"], default="auto"
    )
    parser.add_argument(
        "-m",
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
    )
    parser.add_argument("-l", "--language", help="強制指定語言（例如：zh, en）")
    parser.add_argument("--device", default="cpu", choices=["cpu", "cuda"])

    args = parser.parse_args()
    transcribe_youtube_video(
        url=args.url,
        output_dir=args.output_dir,
        engine=args.engine,
        model_size=args.model,
        language=args.language,
        device=args.device,
    )
