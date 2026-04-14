# Landscape vs datasources diff

**Canonical:** `datasources/pcc_projects.yaml` and `datasources/clomonitor.yaml`. 
When those two disagree, that is called out. **`landscape.yml` should be updated** to match the agreed sources (or you must reconcile PCC vs CLOMonitor first).

## Summary

- **CNCF landscape items in scope:** 251
- **With at least one drift / conflict row:** 73
- **Findings where PCC and CLOMonitor disagree:** 56
- **No PCC and no CLOMonitor match:** 4

## Differences (sorted by field)

Each row is one detected mismatch. Sorted by `Field`, then `Project`.

| Field | Project | Maturity | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|---|---|---|---|---|---|---|---|
| extra.accepted | Copa | sandbox | 2023-09-19 | — | 2023-12-19 | — | Landscape ('2023-09-19') ≠ CLOMonitor ('2023-12-19'). |
| extra.accepted | KubeStellar | sandbox | 2023-12-19 | — | 2023-09-19 | — | Landscape ('2023-12-19') ≠ CLOMonitor ('2023-09-19'). |
| extra.clomonitor_name | Podman Container Tools | sandbox | podman | — | podman-container-tools | — | Landscape ('podman') ≠ CLOMonitor ('podman-container-tool… |
| extra.clomonitor_name | Runme Notebooks | sandbox | runme | — | runme-notebooks | — | Landscape ('runme') ≠ CLOMonitor ('runme-notebooks'). |
| extra.dev_stats_url | OpenEverest | sandbox | — | — | https://openeverest.devstats.cncf.io/ | — | Landscape missing; CLOMonitor has 'https://openeverest.de… |
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
| extra.lfx_slug | Prometheus | graduated | prometheus_del | prometheus | prometheus | Yes | Landscape ('prometheus_del') ≠ PCC ('prometheus'). Landsc… |
| extra.lfx_slug | SpinKube | sandbox | — | — | spinkube | — | Landscape missing; CLOMonitor has 'spinkube'. |
| extra.lfx_slug | Tokenetes | sandbox | tratteria | tratteria | tokenetes | **No** | PCC ('tratteria') and CLOMonitor ('tokenetes') disagree. … |
| extra.lfx_slug | WasmEdge Runtime | sandbox | wasmedge-runtime | wasmedge-runtime | wasm-edge | **No** | PCC ('wasmedge-runtime') and CLOMonitor ('wasm-edge') dis… |
| project (maturity) | Service Mesh Performance | archived | archived | sandbox | — | — | Landscape ('archived') ≠ PCC ('sandbox'). |
| repo_url | Akri | sandbox | https://github.com/project-akri/akri | https://github.com/deislabs/akri | https://github.com/project-akri/akri | **No** | PCC ('https://github.com/deislabs/akri') and CLOMonitor (… |
| repo_url | bootc | sandbox | https://github.com/bootc-dev/bootc | https://github.com/containers/bootc | https://github.com/bootc-dev/bootc | **No** | PCC ('https://github.com/containers/bootc') and CLOMonito… |
| repo_url | Cartography | sandbox | https://github.com/cartography-cncf/cartography | https://github.com/cartography-cncf/cartography | https://github.com/lyft/cartography | **No** | PCC ('https://github.com/cartography-cncf/cartography') a… |
| repo_url | cert-manager | graduated | https://github.com/cert-manager/cert-manager | https://github.com/jetstack/cert-manager | https://github.com/cert-manager/community | **No** | PCC ('https://github.com/jetstack/cert-manager') and CLOM… |
| repo_url | composefs | sandbox | https://github.com/containers/composefs | https://github.com/containers/composefs | https://github.com/composefs/composefs | **No** | PCC ('https://github.com/containers/composefs') and CLOMo… |
| repo_url | container2wasm | sandbox | https://github.com/container2wasm/container2wasm | https://github.com/ktock/container2wasm | https://github.com/container2wasm/container2wasm | **No** | PCC ('https://github.com/ktock/container2wasm') and CLOMo… |
| repo_url | Cozystack | sandbox | https://github.com/cozystack/cozystack | https://github.com/aenix-io/cozystack/ | https://github.com/cozystack/cozystack | **No** | PCC ('https://github.com/aenix-io/cozystack/') and CLOMon… |
| repo_url | Cozystack | sandbox | https://github.com/cozystack/cozystack | https://github.com/aenix-io/cozystack/ | https://github.com/cozystack/cozystack | **No** | PCC ('https://github.com/aenix-io/cozystack/') and CLOMon… |
| repo_url | CubeFS | graduated | https://github.com/cubeFS/cubefs | https://github.com/cubefs/cubefs | https://github.com/chubaofs/chubaofs | **No** | PCC ('https://github.com/cubefs/cubefs') and CLOMonitor (… |
| repo_url | DevSpace | sandbox | https://github.com/devspace-sh/devspace | https://github.com/loft-sh/devspace | https://github.com/loft-sh/devspace | Yes | Landscape ('https://github.com/devspace-sh/devspace') ≠ P… |
| repo_url | Drasi | sandbox | http://github.com/drasi-project/drasi-platform | https://github.com/drasi-project | https://github.com/drasi-project/drasi-platform | Yes | Landscape ('http://github.com/drasi-project/drasi-platfor… |
| repo_url | Easegress | sandbox | https://github.com/easegress-io/easegress | https://github.com/megaease/easegress | https://github.com/megaease/easegress | Yes | Landscape ('https://github.com/easegress-io/easegress') ≠… |
| repo_url | Eraser | sandbox | https://github.com/eraser-dev/eraser | https://github.com/eraser-dev/eraser | https://github.com/Azure/eraser | **No** | PCC ('https://github.com/eraser-dev/eraser') and CLOMonit… |
| repo_url | Fluid | incubating | https://github.com/fluid-cloudnative/fluid | https://github.com/Project-Fluid | https://github.com/fluid-cloudnative/fluid | **No** | PCC ('https://github.com/Project-Fluid') and CLOMonitor (… |
| repo_url | Headlamp | sandbox | https://github.com/kubernetes-sigs/headlamp | https://github.com/kubernetes-sigs/headlamp | https://github.com/headlamp-k8s/headlamp | **No** | PCC ('https://github.com/kubernetes-sigs/headlamp') and C… |
| repo_url | HolmesGPT | sandbox | https://github.com/HolmesGPT/holmesgpt | https://github.com/holmesgpt/ | https://github.com/robusta-dev/holmesgpt | **No** | PCC ('https://github.com/holmesgpt/') and CLOMonitor ('ht… |
| repo_url | Inclavare Containers | sandbox | https://github.com/inclavare-containers/inclavare-containers | https://github.com/inclavare-containers/inclavare-containers | https://github.com/alibaba/inclavare-containers | **No** | PCC ('https://github.com/inclavare-containers/inclavare-c… |
| repo_url | KAI Scheduler | sandbox | https://github.com/kai-scheduler/KAI-Scheduler | https://github.com/kai-scheduler/ | https://github.com/NVIDIA/KAI-Scheduler | **No** | PCC ('https://github.com/kai-scheduler/') and CLOMonitor … |
| repo_url | KAITO | sandbox | https://github.com/kaito-project/kaito | https://github.com/Azure/kaito | https://github.com/Azure/kaito | Yes | Landscape ('https://github.com/kaito-project/kaito') ≠ PC… |
| repo_url | KitOps | sandbox | https://github.com/kitops-ml/kitops | https://github.com/jozu-ai/kitops | https://github.com/jozu-ai/kitops | Yes | Landscape ('https://github.com/kitops-ml/kitops') ≠ PCC (… |
| repo_url | kpt | sandbox | https://github.com/kptdev/kpt | https://github.com/kptdev | https://github.com/GoogleContainerTools/kpt | **No** | PCC ('https://github.com/kptdev') and CLOMonitor ('https:… |
| repo_url | Kube-OVN | sandbox | https://github.com/kubeovn/kube-ovn | https://github.com/alauda/kube-ovn | https://github.com/kubeovn/kube-ovn | **No** | PCC ('https://github.com/alauda/kube-ovn') and CLOMonitor… |
| repo_url | KubeFleet | sandbox | https://github.com/kubefleet-dev/kubefleet | https://github.com/kubefleet-dev/ | https://github.com/Azure/fleet | **No** | PCC ('https://github.com/kubefleet-dev/') and CLOMonitor … |
| repo_url | KubeVela | incubating | https://github.com/kubevela/kubevela | https://github.com/kubevela | https://github.com/oam-dev/kubevela | **No** | PCC ('https://github.com/kubevela') and CLOMonitor ('http… |
| repo_url | Kured | sandbox | https://github.com/kubereboot/kured | https://github.com/weaveworks/kured | https://github.com/kubereboot/kured | **No** | PCC ('https://github.com/weaveworks/kured') and CLOMonito… |
| repo_url | Microcks | sandbox | https://github.com/microcks/microcks | https://github.com/meshery/meshery | https://github.com/microcks/microcks | **No** | PCC ('https://github.com/meshery/meshery') and CLOMonitor… |
| repo_url | ModelPack | sandbox | https://github.com/modelpack/model-spec | https://github.com/CloudNativeAI/model-spec | https://github.com/modelpack/model-spec | **No** | PCC ('https://github.com/CloudNativeAI/model-spec') and C… |
| repo_url | Notary Project | incubating | https://github.com/notaryproject/notation | https://github.com/theupdateframework/notary | https://github.com/notaryproject/notation | **No** | PCC ('https://github.com/theupdateframework/notary') and … |
| repo_url | OpenCost | incubating | https://github.com/opencost/opencost | https://github.com/kubecost/cost-model | https://github.com/opencost/opencost | **No** | PCC ('https://github.com/kubecost/cost-model') and CLOMon… |
| repo_url | OpenELB | archived | https://github.com/openelb/openelb | https://github.com/kubesphere/openelb | — | — | Landscape ('https://github.com/openelb/openelb') ≠ PCC ('… |
| repo_url | OpenYurt | incubating | https://github.com/openyurtio/openyurt | https://github.com/OpenYurt | https://github.com/openyurtio/openyurt | **No** | PCC ('https://github.com/OpenYurt') and CLOMonitor ('http… |
| repo_url | OVN-Kubernetes | sandbox | https://github.com/ovn-kubernetes/ovn-kubernetes | https://github.com/ovn-org/ovn-kubernetes | https://github.com/ovn-kubernetes/ovn-kubernetes | **No** | PCC ('https://github.com/ovn-org/ovn-kubernetes') and CLO… |
| repo_url | Pixie | sandbox | https://github.com/pixie-io/pixie | https://github.com/pixie-labs/pixie | https://github.com/pixie-io/pixie | **No** | PCC ('https://github.com/pixie-labs/pixie') and CLOMonito… |
| repo_url | Porter | sandbox | https://github.com/getporter/porter | https://github.com/Porter | https://github.com/getporter/porter | **No** | PCC ('https://github.com/Porter') and CLOMonitor ('https:… |
| repo_url | Ratify | sandbox | https://github.com/ratify-project/ratify | https://github.com/deislabs/ratify | https://github.com/ratify-project/ratify | **No** | PCC ('https://github.com/deislabs/ratify') and CLOMonitor… |
| repo_url | Runme Notebooks | sandbox | https://github.com/runmedev/runme | https://github.com/stateful/runme | https://github.com/runmedev/runme | **No** | PCC ('https://github.com/stateful/runme') and CLOMonitor … |
| repo_url | sealer | archived | https://github.com/sealerio/sealer | https://github.com/alibaba/sealer | — | — | Landscape ('https://github.com/sealerio/sealer') ≠ PCC ('… |
| repo_url | SlimFaaS | sandbox | https://github.com/SlimPlanet/SlimFaas | https://github.com/AxaFrance/SlimFaas | https://github.com/AxaFrance/SlimFaas | Yes | Landscape ('https://github.com/SlimPlanet/SlimFaas') ≠ PC… |
| repo_url | SOPS | sandbox | https://github.com/getsops/sops | https://github.com/mozilla/sops | https://github.com/mozilla/sops | Yes | Landscape ('https://github.com/getsops/sops') ≠ PCC ('htt… |
| repo_url | Spin | sandbox | https://github.com/spinframework/spin | https://github.com/fermyon/spin | https://github.com/spinframework/spin | **No** | PCC ('https://github.com/fermyon/spin') and CLOMonitor ('… |
| repo_url | SpinKube | sandbox | https://github.com/spinframework/spin-operator | — | https://github.com/spinkube/documentation | — | Landscape ('https://github.com/spinframework/spin-operato… |
| repo_url | Teller | archived | https://github.com/tellerops/teller | https://github.com/SpectralOps/teller | — | — | Landscape ('https://github.com/tellerops/teller') ≠ PCC (… |
| repo_url | Trickster | sandbox | https://github.com/trickstercache/trickster | https://github.com/tricksterproxy/trickster | https://github.com/trickstercache/trickster | **No** | PCC ('https://github.com/tricksterproxy/trickster') and C… |
| repo_url | Visual Studio Code Kubernetes Tools | sandbox | https://github.com/vscode-kubernetes-tools/vscode-kuberne… | https://github.com/Azure/vscode-kubernetes-tools | https://github.com/vscode-kubernetes-tools/vscode-kuberne… | **No** | PCC ('https://github.com/Azure/vscode-kubernetes-tools') … |
| repo_url | youki | sandbox | https://github.com/youki-dev/youki | https://github.com/containers/youki | https://github.com/containers/youki | Yes | Landscape ('https://github.com/youki-dev/youki') ≠ PCC ('… |

## No datasource match

These are in-scope landscape projects that could not be matched to PCC or CLOMonitor; they are usually candidates for upstream/source alignment PRs.

| Project | Maturity | Path |
|---------|----------|------|
| Service Mesh Interface (SMI) | archived | Orchestration & Management / Service Mesh |
| Cedar | sandbox | Provisioning / Security & Compliance |
| Higress | sandbox | Orchestration & Management / API Gateway |
| Monocle | sandbox | Observability and Analysis / Observability |