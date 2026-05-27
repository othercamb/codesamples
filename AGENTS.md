# AGENTS.md

## Cursor Cloud specific instructions

This is a multi-language code samples repository with no unified build system. Each component is standalone. See `CLAUDE.md` for full architecture and run commands.

### Runtimes available

- **Python 3.12** (system) — all Python scripts use this
- **GCC/G++ 13** (system) — for `count_pairs.c` and `count_pairs.cpp` (use `-std=c++17` for C++)
- **dotnet-sdk-8.0** — for `CountPairs.cs`; no `csc` binary, use `dotnet run` via a temp console project (copy file as `Program.cs` into a `dotnet new console` scaffold)

### Running the Flask demo

```bash
cd flask-demo && python3 app.py
```

Runs on `0.0.0.0:5000` in debug mode. Verify with `curl http://localhost:5000`.

### Scripts requiring external credentials or services

- `OCRDemo.py` requires `CLOUD_SDK_AK` and `CLOUD_SDK_SK` environment variables (Huawei Cloud). Will crash immediately without them.
- `fetch_etfs.py` requires Google Chrome installed for headless Selenium scraping. May fail if Chrome is not in PATH.
- `google_finance_demo.py` uses `yfinance` (not Selenium despite the filename in CLAUDE.md); works with just network access.

### Linting and testing

There are no lint configs, test suites, or CI pipelines in this repo. To verify correctness, run each script individually per the commands in `CLAUDE.md`.
