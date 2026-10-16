# Lab 5 – Reflection

**Name:** Pranaav P  **SRN:** PES1UG24AM387

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest were Flake8's style issues: removing the unused `json` import, renaming `l` to `top`, using `is None`, and wrapping long lines. Each is a mechanical one-line change and the tool points at the exact spot.

The hardest was Pylint's `redefined-outer-name` (W0621). The cause was a design choice, a global `conn` created at import time, not one bad line. Fixing it meant adding a `create_ledger()` function, passing the connection in from `main()`, and adding the `__name__` guard. The security fixes needed some thought too: removing `os.system` raised the question of what a "slip" should actually do, and switching MD5 to SHA-256 changes the token value, which matters if tokens are already stored somewhere.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

There were no real false positives, but some findings were stronger than the context called for. Bandit's B324 rates MD5 as **High**, but here the hash is only an identifier token, not a password, so the practical risk is low. Using `hashlib.md5(..., usedforsecurity=False)` would also have satisfied Bandit. I chose SHA-256 anyway because it costs nothing. Several tools also report the same problem (long lines in both Flake8 E501 and Pylint C0301, `== None` in both E711 and C0121), so the raw issue count overstates how many distinct problems there are.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- **Locally:** run Flake8 and Pylint in the editor, and add a `pre-commit` hook running Flake8, Pylint and Bandit so problems are caught before a commit.
- **CI:** add a GitHub Actions job that runs all three on every push and pull request. It fails the build on any Bandit Medium/High finding, on Flake8 errors, or on a Pylint score below a threshold (for example 9.5, using `--fail-under`).
- **Configuration:** keep shared settings in `pyproject.toml`/`setup.cfg` so everyone uses the same rules, and suppress a finding (`# nosec`, `# pylint: disable=`) only with a written reason.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- **Security:** the SQL injection, shell injection and weak-hash issues are gone. Bandit now reports no issues.
- **Robustness:** `top_farmer` no longer crashes on an empty ledger, and importing the module no longer runs the demo or opens a database.
- **Readability:** snake_case names, docstrings, a named `LOW_FAT_THRESHOLD` constant and f-strings make the intent clear without comments.
- **Measured quality:** Pylint went from 2.00/10 to 10.00/10 and Flake8 from 7 warnings to 0, while the program's behaviour stayed the same.
