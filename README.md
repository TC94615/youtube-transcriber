# YouTube Transcriber

使用 Whisper 或 FunASR 自動將 YouTube 影片轉換為文字與 SRT 字幕。

---

## 📦 功能特色

- 🎥 從 YouTube 下載音頻（支援多種格式）
- 🔊 自動語言偵測（英文 ➜ Whisper，中文 ➜ FunASR）
- 🧠 支援多種引擎：
  - OpenAI Whisper（英語優先）
  - ModelScope + FunASR（中文優先）
- 📄 輸出純文字 `.txt` 與字幕檔 `.srt`
- ⚙️ 可選擇 CPU / CUDA 推論（依設備支援）

---

## 🧰 技術架構

本專案基於以下技術開發：

| 工具 | 用途 |
|------|------|
| `yt-dlp` | 下載 YouTube 音視訊 |
| `openai-whisper` | 英文語音轉文字 |
| `funasr` / `modelscope` | 中文語音轉文字 |
| `onnxruntime` | ONNX 模型推論支援 |
| `torch` | PyTorch 基礎支援 |
| `Poetry` | 專案與依賴管理 |

---

## 📦 安裝方式

### 使用 Poetry（推薦）

```bash
git clone https://github.com/yourname/youtube-transcriber.git 
cd youtube-transcriber