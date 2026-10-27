---
name: zhengli-huiyi-jilu
description: Use this skill when the user asks for 「整理會議記錄」, meeting minutes, meeting transcript cleanup, or converting ChatGPT/Gemini/shared conversation content into formal Chinese meeting records. This workflow requires confirming attendees first, generating Markdown before PDF, avoiding visible AI/source labels in deliverables, and archiving outputs in a folder named by meeting title and date.
---

# 整理會議記錄

## Purpose

Use this skill to turn meeting transcripts, conversation links, copied notes, or exported text into formal Chinese meeting records. It supports sources from ChatGPT, Gemini, pasted text, local files, or exported documents, but the final meeting record must read like a normal business record and must not expose the AI/source platform.

## Mandatory Workflow

Follow this sequence every time:

1. Read or extract the meeting content from the user-provided source.
2. Identify the meeting title/date and extract the attendee list.
3. Stop and ask the user to confirm the attendee list before drafting minutes.
4. Once a meeting title/date is identified, use the actual meeting title plus meeting date in user-visible headings, file links, folder names, and status messages. Do not keep using the generic label `整理會議記錄` as the visible item title after the meeting title is known.
5. After attendee confirmation, create a dedicated folder named:
   `會議記錄名稱_YYYY-MM-DD`
6. Generate a Markdown draft (`.md`) first and place it in that folder.
7. Ask the user to confirm the Markdown content.
8. Only after user confirmation, convert the Markdown into PDF and place it in the same folder.
9. Verify the PDF exists, is readable, and report the page count when possible.

Do not skip the attendee confirmation or Markdown confirmation unless the user explicitly overrides the workflow.

## Attendee Confirmation

Before generating the minutes, present a concise confirmation block:

```markdown
**會議名稱**
<title>

**目前辨識的與會／列席人員**
- <company/team>: <names>
- <company/team>: <names>

請確認這份名單是否正確，或直接回覆要修改的版本。
```

If the transcript contains uncertain names, mark them as `待確認` rather than inventing names or titles.

## Visible Item Title

The user wants each meeting-minutes item to be recognizable by the final meeting-record title and meeting date, not by the generic skill name.

After extracting or confirming the meeting title/date:

- Use `會議名稱_YYYY-MM-DD` as the first visible heading in the attendee-confirmation response whenever the date is known or reasonably defaulted.
- Use the meeting title as the Markdown H1.
- Use the meeting title and date in the folder and file names.
- Use the meeting title and date in final links and handoff messages.
- Avoid naming generated meeting-record items only `整理會議記錄`.

If the app sidebar or project list title is controlled outside the skill and cannot be directly renamed, still make the conversation content, output folder, and file names start with the actual meeting title plus date so the item is easy to identify.

## Content Rules

The meeting record should usually include:

- 會議基本資訊
- 會議目的
- 重點摘要
- 會議結論
- 後續行動項目
- 待確認事項, when useful

Use formal business Chinese. Remove filler words, repeated speech, incomplete starts, and transcript artifacts. Preserve concrete decisions, commitments, risks, dates, quantities, owners, and next steps.

Do not include visible AI/source wording in deliverables. Avoid words such as:

- ChatGPT
- Gemini
- AI
- 人工智慧
- 由模型整理
- 由機器生成

It is acceptable to mention the source in your chat response if needed, but not inside the `.md` or `.pdf` meeting record.

## Dates And Naming

Use the meeting date if it is explicit in the source. If the source does not explicitly provide a meeting date, default to the current local date for the meeting date. Only mark the date as `（待確認）` when the user questions the date, provides conflicting date information, or the workflow has a concrete reason to doubt the current-date default.

Folder naming:

```text
<會議記錄名稱>_<YYYY-MM-DD>
```

Example:

```text
業務技術對接會議_2026-05-21
```

File naming:

```text
<會議記錄名稱>_<YYYY-MM-DD>.md
<會議記錄名稱>_<YYYY-MM-DD>.pdf
```

For user-facing PDF links, prefer stable filenames. Avoid temporary Word lock files and avoid relying on filenames with unusual punctuation if they caused opening issues.

## Source Handling

For ChatGPT or Gemini links:

- Use available browser/Chrome capabilities when the page requires user login.
- Extract only the visible meeting-relevant text.
- Ignore sidebars, navigation, history lists, platform warnings, and prompt scaffolding.
- If a shared page already contains an AI-generated draft, use it only as a reference and still apply this workflow.

For pasted text or local files:

- Read the full supplied content first.
- If multiple files exist, identify the newest or ask only when ambiguous and risky.

## Markdown Draft Requirements

Write the Markdown as the primary editable draft. Keep it clean and human-facing:

- Title as H1.
- Use tables for meeting metadata and action items.
- Use numbered conclusions or bullets for decisions.
- Keep wording concise and traceable to the transcript.
- Include `待確認事項` for uncertain dates, names, titles, quantities, or next meetings.

After creating the Markdown, provide only the draft file link and ask for confirmation before PDF conversion.

## Word And PDF Layout Quality Rules

When exporting meeting records to Word or PDF, apply these quality gates before final handoff:

- Normalize mixed Chinese/English and number/unit spacing in the Markdown source before conversion. Insert half-width spaces between Chinese characters and adjacent English letters or numbers, for example `Molding 設備`, `Molding 製程`, `TB 場`, `2026 年 9 月`, and `10 至 12 個月`. Also remove accidental spaces after Chinese punctuation before English or numbers, for example `、2027 年` instead of `、 2027 年`.
- Preserve numbered-list boundaries in Markdown. Each numbered item must be on its own line. If source cleanup or batch replacement creates `1. ...。2. ...。3. ...` on one line, split it before conversion. Do not let Word/PDF output show a later number at the end of the previous sentence.
- For Word conversion, avoid relying only on automatic Word list styles for critical numbered conclusions. Prefer explicit numbered paragraphs with hanging indent when custom conversion scripts are used, so `1.`, `2.`, and later numbers stay at the beginning of their own paragraphs.
- Use table-specific column widths instead of equal widths. For 4-column comparison tables, keep the schedule column narrow and give the action/evaluation columns enough width for full text. For action-item tables, give the content column the most width.
- Use landscape page orientation for wide Word/PDF tables when portrait layout would force cramped text. Set fixed table widths, top vertical alignment, cell padding, and slightly smaller table font.
- Tune paragraph readability: body text should use moderate line spacing, controlled paragraph spacing, and consistent bullet/number indentation. Avoid overly tight line spacing or cramped table cells.
- For ReportLab or other Chinese-font PDF generation, never render Markdown bullets with the `•` glyph. This glyph has repeatedly mapped incorrectly to the Chinese character `煉` in meeting-minutes PDFs. For meeting records where the user wants round bullets, render bullets as the stable black circle `●` but set the bullet marker smaller than body text, for example Word `● ` at about 7 pt with 10.5 pt body text, and ReportLab `bulletText="●"` with `bulletFontSize` about 6.5 pt for a 9.5 pt body. This keeps the visible round-dot style without oversized black dots or glyph garbling. Use ASCII hyphens (`-`) only when round bullets cannot be verified safely.
- Before final handoff, verify the generated outputs: confirm Word is readable, PDF page count is available, forbidden source labels are absent, no `Molding設備`-style mixed-language joins remain, no `。2.` / `。3.` continuous numbered-list joins remain, and no accidental `煉` glyph appears from list rendering.

## PDF Conversion

After the user confirms the Markdown:

1. Convert the `.md` into PDF in the same folder.
2. Use a reliable local method available in the environment.
3. If using a custom script, keep it in the same meeting folder only when it helps reproduce the output.
4. Verify:
   - PDF file exists.
   - PDF is readable.
   - Page count can be determined.
   - Forbidden AI/source labels are absent from the PDF text when extraction is available.
   - The PDF extracted text does not contain `煉`; if it does, treat it as a failed export, replace bullet rendering with ASCII `-`, regenerate the PDF, and verify again.

If common converters such as `pandoc` are unavailable, use Python `reportlab` or another local PDF method with Chinese font support. If layout verification tools such as `pdftoppm` are unavailable, state that visual rendering was not performed but still verify the PDF structure.

## Final Response Pattern

Before PDF confirmation, say:

```markdown
已產生 Markdown 草稿：
[filename.md](absolute/path/to/file.md)

請確認內容是否可以，確認後我再轉成 PDF。
```

After PDF generation, say:

```markdown
已轉成 PDF：
[filename.pdf](absolute/path/to/file.pdf)

已確認 PDF 可讀，共 N 頁。
```

Keep responses short and do not include unnecessary implementation details.
