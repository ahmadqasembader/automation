# Repo URL anomalies for PCC (Landscape vs PCC)

Generated from `landscape_source_diff.json` (`field = repo_url`) with `curl` URL checks.

Rule: when both URLs are GitHub and org/owner matches, repo path differences are treated as aligned.
This report includes only non-aligned (anomalous) PCC vs Landscape rows.

| Project | Maturity | PCC URL | PCC | Landscape URL | Landscape | Org match | Same final destination | Result | Note |
|---|---|---|---|---|---|---|---|---|---|
| SpinKube | sandbox | — | ❌ missing | https://github.com/spinframework/spin-operator | ✅ 200 | No | N/A | Missing URL | One side is missing. |
