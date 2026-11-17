# leroy-skills-garage

個人技能的版本管理倉庫。一般問答、搜尋、編碼與小修直接處理；需要專項能力時才讀取對應技能。

## 技能

| 技能 | 使用時機 |
| --- | --- |
| [critical-analysis](skills/critical-analysis/SKILL.md) | 分析、評估、給想法、修復診斷、規劃、評審 |
| [delivery-evidence](skills/delivery-evidence/SKILL.md) | 驗證、交付證據與發布檢查 |
| [project-memory](skills/project-memory/SKILL.md) | 工作摘要、交接與穩定決策 |
| [hatch-pet](skills/hatch-pet/SKILL.md) | 動畫寵物建立、修復及封裝 |
| [quarkclouddrive](skills/quarkclouddrive/SKILL.md) | 夸克網盤操作及已要求的帳號授權 |

每個技能的描述都會出現在每次對話裡，新增技能前先確認現有技能無法涵蓋。技能之間不設必讀鏈。

## 結構

- `AGENTS.md`、`CLAUDE.md`：協作規則，兩份內容相同。
- `skills/`：技能本體。
- `scripts/validate_skills.py`：檢查技能的編碼、frontmatter、名稱與連結。
- `tests/`：驗證腳本的測試。

## 驗證

```text
python scripts/validate_skills.py
python -m unittest discover -s tests -p "test_*.py" -v
```

兩者只用標準庫。修改技能或腳本後都要執行。
