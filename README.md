# leroy-skills-garage

個人技能的版本管理倉庫，與全局精簡版同步。一般問答、搜尋、編碼與小修直接處理；需要專項能力時才讀取相應技能。

## 目前技能

| 技能 | 使用時機 |
| --- | --- |
| [work-planning](skills/work-planning/SKILL.md) | 複雜需求、取捨及執行計畫 |
| [engineering-review](skills/engineering-review/SKILL.md) | 指定評審或高風險復核 |
| [delivery-evidence](skills/delivery-evidence/SKILL.md) | 驗證、交付證據與發布檢查 |
| [project-memory](skills/project-memory/SKILL.md) | 工作摘要、交接與穩定決策 |
| [devflow-marshal](skills/devflow-marshal/SKILL.md) | 正式狀態、契約、審計及封存 |
| [hatch-pet](skills/hatch-pet/SKILL.md) | 動畫寵物建立、修復及封裝 |
| [quarkclouddrive](skills/quarkclouddrive/SKILL.md) | 夸克網盤操作及已要求的帳號授權 |
| [entry-router](skills/entry-router/SKILL.md) | 舊規則相容入口 |
| [grill-lite](skills/grill-lite/SKILL.md) | 舊規則澄清相容入口 |

文件、簡報、試算表、網站與一般圖像使用目前環境已安裝的系統／插件技能；本倉庫不再重複封裝通用編碼護欄或強制技能鏈。

## 規則與驗證

[AGENTS.md](AGENTS.md) 與 [CLAUDE.md](CLAUDE.md) 使用同一份規則。L0 直接答覆；L1 最小修改與驗證；L2 按專案規則規劃審議並承接已批准執行；L3 才啟用正式治理。

```text
python scripts/validate_skills.py
python scripts/devflow.py validate-workflow --all
python scripts/devflow.py doctor-capabilities --strict
python -m unittest discover -s tests -p test_*.py -v
python scripts/update_knowledge_index.py
```

技能驗證檢查名稱、frontmatter、引用資源及套件／路由；不要求每個技能都有 Contract/Fallback/Handoff。正式契約與交付門禁依專案設定執行。

## 入口

- [技能套件](skills.packages.json)、[路由提示](skills.registry.json)：僅列目前技能；不是必讀鏈。
- [協作協定](skills/collaboration-protocol.yaml)：分級與按需使用原則。
- [工作流](workflows)：implement/debug/ship/archive 的選用配方；一般小修不必啟用。
- [能力供應者](capabilities/providers.yaml)：沿用可用工具與 fallback。
- [知識庫索引](docs/indexes/01-知识库索引.md)、[狀態](docs/status.md)。
- [DevFlow 工具說明](docs/devflow-run-tooling.md)、[Change 生命週期](docs/change-lifecycle.md)。

## 同步與歷史

本次以全局 9 個非系統技能為準，保留其實際使用的 scripts、references、schemas、tests 與授權文件；不包含快取、憑證或系統／插件技能。未新增或升級依賴，專項 Runtime 需求由各技能在實際使用時確認。

原有零散規劃、評審、測試與記憶技能已整併；通用編碼、壓力式 PUA 技能及 PUA 重複副本已移除。過往計畫、change/run、spec 與 memory 保留作歷史證據，其中舊技能名稱不代表目前可用能力。現行能力以本頁及 skills 目錄為準。

[本次變更與驗證](changes/20260907-global-skill-slim-sync/proposal.md) 記錄同步範圍、批准、回滾及交付結果。
