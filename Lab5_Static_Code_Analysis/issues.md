# Lab 5 – Issues Found and Fixed

**Name:** Pranaav P  **SRN:** PES1UG24AM387  **File:** `dairy_collection.py`

Line numbers refer to the original file (`before/` reports). Sorted by severity, highest first.

| # | Issue | Tool / Code | Type | Severity | Line(s) | Description | Fix Approach |
|---|-------|-------------|------|----------|---------|-------------|--------------|
| 1 | Shell command injection | Bandit B605 | Security | High | 31 | `os.system("echo printing slip for " + farmer)` runs a shell with user data; a name like `x; rm -rf ~` would run arbitrary commands | Removed the shell call; slip is printed with `print()` and the `os` import was dropped |
| 2 | Weak MD5 hash | Bandit B324 | Security | High | 16 | `hashlib.md5` is broken (collisions) and unsuitable for tokens | Switched to `hashlib.sha256` |
| 3 | SQL injection | Bandit B608 | Security | Medium | 11 | INSERT built with `str.format`, so a farmer name with `'` breaks or alters the query | Parameterised query with `?` placeholders and a values tuple |
| 4 | Unused import | Flake8 F401 / Pylint W0611 | Code smell | Medium | 2 | `json` imported but never used | Removed the import |
| 5 | Comparison to None with `==` | Flake8 E711 / Pylint C0121 | Bug-prone | Medium | 36 | `fat == None` can be fooled by objects overriding `__eq__` | Changed to `fat is None` |
| 6 | Global connection shadowed by parameters | Pylint W0621 | Design | Medium | 6, 10, 19, 24, 34 | Module-level `conn` is redefined in every function, and the DB is created on import | Moved setup into `create_ledger()`, called from `main()`; parameters renamed `db` |
| 7 | Crash on empty ledger | Manual review | Bug | Medium | 26 | `max()` on an empty result raises `ValueError` | `top_farmer` returns `None` when there are no rows |
| 8 | Code runs on import | Manual review | Design | Low | 47 | `main()` called unconditionally, so importing the module runs the demo | Wrapped in `if __name__ == "__main__":` |
| 9 | Ambiguous variable name | Flake8 E741 | Style | Low | 26 | Variable `l` looks like `1`/`I` | Renamed to `top` |
| 10 | Lines too long | Flake8 E501 / Pylint C0301 | Style | Low | 7, 11, 20, 25 | Lines over 79 characters (PEP 8) | Split SQL strings and calls across lines |
| 11 | Non-snake_case function names | Pylint C0103 | Style | Low | 10, 15, 19, 24, 30, 34 | `recordMilk`, `farmerToken`, etc. break PEP 8 naming | Renamed to `record_milk`, `farmer_token`, `daily_total`, `top_farmer`, `print_slip`, `low_fat` |
| 12 | Missing docstrings | Pylint C0114 / C0116 | Documentation | Low | 1 and every function | No module or function docstrings | Added docstrings throughout |
| 13 | Old-style formatting | Pylint C0209 | Style | Low | 11, 21 | `str.format` / `%` instead of f-strings | Used f-strings (and parameters for SQL) |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 2.00/10 (24 messages) | **10.00/10** |
| Bandit | 3 issues (2 High, 1 Medium) | **No issues identified** |
| Flake8 | 7 issues | **0 issues** (empty report) |

The program still produces the same output (`Total: 32.5 litres Lata ['Lata']`, the slip line, and the farmer token, which is now a SHA-256 digest instead of MD5).
