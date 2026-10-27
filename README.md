# 整理會議記錄 Skill

這是一個供 Codex 使用的繁體中文會議記錄整理 Skill。

## 安裝

1. 下載本專案的 ZIP。
2. 建立名為 `zhengli-huiyi-jilu` 的資料夾，將 ZIP 內的 `SKILL.md`、`agents`、`scripts` 放入其中，再將該資料夾放到 Codex 的個人 Skills 目錄：
   - macOS / Linux：`~/.codex/skills/zhengli-huiyi-jilu/`
   - Windows：`%USERPROFILE%\.codex\skills\zhengli-huiyi-jilu\`
3. 確認 `SKILL.md` 位於該資料夾根目錄。

## PDF 輸出

附帶的 `scripts/markdown_minutes_to_pdf.py` 可將 Markdown 會議記錄轉成 PDF。使用前需安裝 Python 3 與 ReportLab：

```bash
python -m pip install reportlab
python scripts/markdown_minutes_to_pdf.py input.md output.pdf
```

## 專案內容

- `SKILL.md`：整理流程與格式規範。
- `agents/openai.yaml`：Skill 在 Codex 中顯示的名稱與描述。
- `scripts/markdown_minutes_to_pdf.py`：Markdown 轉 PDF 的工具。

