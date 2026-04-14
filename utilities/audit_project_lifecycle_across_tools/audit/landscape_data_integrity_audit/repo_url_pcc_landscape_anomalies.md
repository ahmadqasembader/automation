# Repo URL anomalies for PCC (Landscape vs PCC)

Generated from `landscape_source_diff.json` (`field = repo_url`) with `curl` URL checks.

Rule: when both URLs are GitHub and org/owner matches, repo path differences are treated as aligned.
This report includes only non-aligned (anomalous) PCC vs Landscape rows.

| Project | Maturity | PCC URL | PCC | Landscape URL | Landscape | Org match | Same final destination | Result | Note |
|---|---|---|---|---|---|---|---|---|---|
| Fluid | incubating | https://github.com/Project-Fluid | ✅ 200 | https://github.com/fluid-cloudnative/fluid | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/Project-Fluid` vs Landscape `https://github.com/fluid-cloudnative/fluid`. |
| Microcks | sandbox | https://github.com/meshery/meshery | ✅ 200 | https://github.com/microcks/microcks | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/meshery/meshery` vs Landscape `https://github.com/microcks/microcks`. |
| Notary Project | incubating | https://github.com/theupdateframework/notary | ✅ 200 | https://github.com/notaryproject/notation | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/notaryproject/notary` vs Landscape `https://github.com/notaryproject/notation`. |
| OpenYurt | incubating | https://github.com/OpenYurt | ✅ 200 | https://github.com/openyurtio/openyurt | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/OpenYurt` vs Landscape `https://github.com/openyurtio/openyurt`. |
| Porter | sandbox | https://github.com/Porter | ✅ 200 | https://github.com/getporter/porter | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/Porter` vs Landscape `https://github.com/getporter/porter`. |
| SpinKube | sandbox | — | ❌ missing | https://github.com/spinframework/spin-operator | ✅ 200 | No | N/A | Missing URL | One side is missing. |
