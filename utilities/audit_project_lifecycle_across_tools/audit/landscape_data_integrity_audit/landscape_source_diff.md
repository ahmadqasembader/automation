# Landscape vs datasources diff

**Canonical:** `datasources/pcc_projects.yaml` and `datasources/clomonitor.yaml`. 
When those two disagree, that is called out. **`landscape.yml` should be updated** to match the agreed sources (or you must reconcile PCC vs CLOMonitor first).

## Summary

- **CNCF landscape items in scope:** 251
- **With at least one drift / conflict row:** 39
- **Findings where Landscape and CLOMonitor disagree:** 38
- **No PCC and no CLOMonitor match:** 5

## Differences (sorted by field)

Each row is one detected mismatch. Sorted by `Field`, then `Project`.

| Field | Project | Maturity | Landscape | PCC | CLOMonitor | Landscape≈CLO? | Note |
|---|---|---|---|---|---|---|---|
| extra.accepted | Copa | sandbox | 2023-09-19 | — | 2023-12-19 | **No** | Landscape ('2023-09-19') ≠ CLOMonitor ('2023-12-19'). |
| extra.accepted | KubeStellar | sandbox | 2023-12-19 | — | 2023-09-19 | **No** | Landscape ('2023-12-19') ≠ CLOMonitor ('2023-09-19'). |
| extra.clomonitor_name | KAITO | sandbox | — | — | kaito | **No** | Landscape missing; CLOMonitor has 'kaito'. |
| extra.clomonitor_name | KServe | incubating | — | — | kserve | **No** | Landscape missing; CLOMonitor has 'kserve'. |
| extra.clomonitor_name | Podman Container Tools | sandbox | podman | — | podman-container-tools | **No** | Landscape ('podman') ≠ CLOMonitor ('podman-container-tool… |
| extra.clomonitor_name | Runme Notebooks | sandbox | runme | — | runme-notebooks | **No** | Landscape ('runme') ≠ CLOMonitor ('runme-notebooks'). |
| extra.dev_stats_url | OpenEverest | sandbox | — | — | https://openeverest.devstats.cncf.io/ | **No** | Landscape missing; CLOMonitor has 'https://openeverest.de… |
| extra.lfx_slug | Cloud Custodian | incubating | c7n | c7n | cloud-custodian | **No** | PCC ('c7n') and CLOMonitor ('cloud-custodian') disagree. … |
| extra.lfx_slug | Confidential Containers | sandbox | confcont | confcont | confidential-containers | **No** | PCC ('confcont') and CLOMonitor ('confidential-containers… |
| extra.lfx_slug | Connect RPC | sandbox | connect | connect | connect-rpc | **No** | PCC ('connect') and CLOMonitor ('connect-rpc') disagree. … |
| extra.lfx_slug | Distribution | sandbox | cncf-distribution | cncf-distribution | distribution | **No** | PCC ('cncf-distribution') and CLOMonitor ('distribution')… |
| extra.lfx_slug | Dragonfly | graduated | d7y | d7y | dragonfly | **No** | PCC ('d7y') and CLOMonitor ('dragonfly') disagree. Landsc… |
| extra.lfx_slug | Emissary-Ingress | incubating | emissary | emissary | emissary-ingress | **No** | PCC ('emissary') and CLOMonitor ('emissary-ingress') disa… |
| extra.lfx_slug | external-secrets | sandbox | externalsecretsoperator | externalsecretsoperator | external-secrets | **No** | PCC ('externalsecretsoperator') and CLOMonitor ('external… |
| extra.lfx_slug | Flux | graduated | fluxcd | fluxcd | flux-project | **No** | PCC ('fluxcd') and CLOMonitor ('flux-project') disagree. … |
| extra.lfx_slug | Hexa | sandbox | hexa | hexa | hexapolicyorchestrator | **No** | PCC ('hexa') and CLOMonitor ('hexapolicyorchestrator') di… |
| extra.lfx_slug | Inclavare Containers | sandbox | inclavarecontainers | inclavarecontainers | inclavare | **No** | PCC ('inclavarecontainers') and CLOMonitor ('inclavare') … |
| extra.lfx_slug | Kubernetes | graduated | k8s | k8s | kubernetes | **No** | PCC ('k8s') and CLOMonitor ('kubernetes') disagree. Lands… |
| extra.lfx_slug | Logging Operator (Kube Logging) | sandbox | logging-operator | logging-operator | kube-logging | **No** | PCC ('logging-operator') and CLOMonitor ('kube-logging') … |
| extra.lfx_slug | metal3-io | incubating | metal3 | metal3 | metal3-io | **No** | PCC ('metal3') and CLOMonitor ('metal3-io') disagree. Lan… |
| extra.lfx_slug | Network Service Mesh | sandbox | nsm | nsm | network-service-mesh | **No** | PCC ('nsm') and CLOMonitor ('network-service-mesh') disag… |
| extra.lfx_slug | Open Cluster Management | sandbox | openclustermanagement | openclustermanagement | ocm | **No** | PCC ('openclustermanagement') and CLOMonitor ('ocm') disa… |
| extra.lfx_slug | Open Policy Agent (OPA) | graduated | openpolicyagent | openpolicyagent | opa | **No** | PCC ('openpolicyagent') and CLOMonitor ('opa') disagree. … |
| extra.lfx_slug | OpenGitOps | sandbox | gitops-wg | gitops-wg | open-gitops | **No** | PCC ('gitops-wg') and CLOMonitor ('open-gitops') disagree… |
| extra.lfx_slug | OpenTofu | sandbox | opentf | opentf | opentofu | **No** | PCC ('opentf') and CLOMonitor ('opentofu') disagree. Land… |
| extra.lfx_slug | Operator Framework | incubating | operator-sdk | operator-sdk | operator-framework | **No** | PCC ('operator-sdk') and CLOMonitor ('operator-framework'… |
| extra.lfx_slug | OSCAL-COMPASS | sandbox | trestlegrc | trestlegrc | oscal-compass | **No** | PCC ('trestlegrc') and CLOMonitor ('oscal-compass') disag… |
| extra.lfx_slug | Piraeus Datastore | sandbox | piraeus-datastore | piraeus-datastore | piraeus | **No** | PCC ('piraeus-datastore') and CLOMonitor ('piraeus') disa… |
| extra.lfx_slug | Prometheus | graduated | prometheus_del | prometheus | prometheus | **No** | Landscape ('prometheus_del') ≠ PCC ('prometheus'). Landsc… |
| extra.lfx_slug | SpinKube | sandbox | — | — | spinkube | **No** | Landscape missing; CLOMonitor has 'spinkube'. |
| extra.lfx_slug | Tokenetes | sandbox | tratteria | tratteria | tokenetes | **No** | PCC ('tratteria') and CLOMonitor ('tokenetes') disagree. … |
| extra.lfx_slug | WasmEdge Runtime | sandbox | wasmedge-runtime | wasmedge-runtime | wasm-edge | **No** | PCC ('wasmedge-runtime') and CLOMonitor ('wasm-edge') dis… |
| project (maturity) | Service Mesh Performance | archived | archived | sandbox | — | — | Landscape ('archived') ≠ PCC ('sandbox'). |
| repo_url | cert-manager | graduated | https://github.com/cert-manager/cert-manager | https://github.com/jetstack/cert-manager | https://github.com/cert-manager/community | Yes | PCC ('https://github.com/jetstack/cert-manager') and CLOM… |
| repo_url | Drasi | sandbox | http://github.com/drasi-project/drasi-platform | https://github.com/drasi-project | https://github.com/drasi-project/drasi-platform | **No** | Landscape ('http://github.com/drasi-project/drasi-platfor… |
| repo_url | HolmesGPT | sandbox | https://github.com/HolmesGPT/holmesgpt | https://github.com/holmesgpt/ | https://github.com/robusta-dev/holmesgpt | **No** | PCC ('https://github.com/holmesgpt/') and CLOMonitor ('ht… |
| repo_url | KAI Scheduler | sandbox | https://github.com/kai-scheduler/KAI-Scheduler | https://github.com/kai-scheduler/ | https://github.com/NVIDIA/KAI-Scheduler | **No** | PCC ('https://github.com/kai-scheduler/') and CLOMonitor … |
| repo_url | kpt | sandbox | https://github.com/kptdev/kpt | https://github.com/kptdev | https://github.com/GoogleContainerTools/kpt | **No** | PCC ('https://github.com/kptdev') and CLOMonitor ('https:… |
| repo_url | KubeVela | incubating | https://github.com/kubevela/kubevela | https://github.com/kubevela | https://github.com/oam-dev/kubevela | **No** | PCC ('https://github.com/kubevela') and CLOMonitor ('http… |
| repo_url | SpinKube | sandbox | https://github.com/spinframework/spin-operator | — | https://github.com/spinkube/documentation | **No** | Landscape ('https://github.com/spinframework/spin-operato… |

## No datasource match

These are in-scope landscape projects that could not be matched to PCC or CLOMonitor; they are usually candidates for upstream/source alignment PRs.

| Project | Maturity | Path |
|---------|----------|------|
| Service Mesh Interface (SMI) | archived | Orchestration & Management / Service Mesh |
| Volcano-Kthena | incubating | Inference / Framework |
| Cedar | sandbox | Provisioning / Security & Compliance |
| Higress | sandbox | Orchestration & Management / API Gateway |
| Monocle | sandbox | Observability and Analysis / Observability |