# Lab 5: Static Code Analysis — Dairy Milk Collection Ledger

**Name:** Pranaav P  **SRN:** PES1UG24AM387
**Assigned repo:** https://github.com/SETAPESU26/L5_26_dairy_collection

| File | Contents |
|------|----------|
| `dairy_collection.py` | Cleaned script (Pylint 10.00/10, Bandit and Flake8 clean) |
| `before/` | `pylint_report.txt`, `bandit_report.txt`, `flake8_report.txt` for the original code |
| `after/` | The same three reports after the fixes (the Flake8 report is empty, meaning no issues) |
| `issues.md` | Table of the issues found and how each was fixed |
| `reflection.md` | Answers to the reflection questions |

Fix commits, one per tool: Bandit (security), Flake8 (style), Pylint (quality).

```bash
pip install pylint bandit flake8
python dairy_collection.py
pylint dairy_collection.py > pylint_report.txt
bandit -r dairy_collection.py > bandit_report.txt
flake8 dairy_collection.py > flake8_report.txt
```
