# Repo URL anomalies for CLOMonitor (Landscape vs CLOMonitor)

Generated from `landscape_source_diff.json` (`field = repo_url`) with `curl` URL checks.

Rule: when both URLs are GitHub and org/owner matches, repo path differences are treated as aligned.
This report includes only non-aligned (anomalous) CLOMonitor vs Landscape rows.

| Project | Maturity | CLOMonitor URL | CLOMonitor | Landscape URL | Landscape | Org match | Same final destination | Result | Note |
|---|---|---|---|---|---|---|---|---|---|
| KubeFleet | sandbox | https://github.com/Azure/fleet | ✅ 200 | https://github.com/kubefleet-dev/kubefleet | ✅ 200 | No | No | Mismatch | Different final destinations: CLOMonitor `https://github.com/Azure/fleet` vs Landscape `https://github.com/kubefleet-dev/kubefleet`. |
| SpinKube | sandbox | https://github.com/spinkube/documentation | ✅ 200 | https://github.com/spinframework/spin-operator | ✅ 200 | No | No | Mismatch | Different final destinations: CLOMonitor `https://github.com/spinframework/spinkube-docs` vs Landscape `https://github.com/spinframework/spin-operator`. |
