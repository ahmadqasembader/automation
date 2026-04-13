# Landscape vs PCC Repo URL Validation

Checked the `repo_url` differences from `landscape_source_diff.json` by requesting each URL with redirects enabled on 2026-04-13.

- Projects checked: 44
- Landscape URLs working: 44/44
- PCC URLs working: 43/44

| Project | Maturity | Landscape | Landscape status | PCC | PCC status | Same final destination? |
|---|---|---|---|---|---|---|
| SpinKube | sandbox | https://github.com/spinframework/spin-operator | ✅ 200 | — | ❌ missing | N/A |
| kpt | sandbox | https://github.com/kptdev/kpt | ✅ 200 | https://github.com/kptdev | ✅ 200 | No |
| OpenYurt | incubating | https://github.com/openyurtio/openyurt | ✅ 200 | https://github.com/OpenYurt | ✅ 200 | No |
| Notary Project | incubating | https://github.com/notaryproject/notation | ✅ 200 | https://github.com/theupdateframework/notary -> https://github.com/notaryproject/notary | ✅ 200 redirected | No |
| CubeFS | graduated | https://github.com/cubeFS/cubefs | ✅ 200 | https://github.com/cubefs/cubefs | ✅ 200 | No |
| Fluid | incubating | https://github.com/fluid-cloudnative/fluid | ✅ 200 | https://github.com/Project-Fluid | ✅ 200 | No |
| KAI Scheduler | sandbox | https://github.com/kai-scheduler/KAI-Scheduler | ✅ 200 | https://github.com/kai-scheduler/ | ✅ 200 | No |
| KubeFleet | sandbox | https://github.com/kubefleet-dev/kubefleet | ✅ 200 | https://github.com/kubefleet-dev/ | ✅ 200 | No |
| Drasi | sandbox | http://github.com/drasi-project/drasi-platform -> https://github.com/drasi-project/drasi-platform | ✅ 200 redirected | https://github.com/drasi-project | ✅ 200 | No |
| KubeVela | incubating | https://github.com/kubevela/kubevela | ✅ 200 | https://github.com/kubevela | ✅ 200 | No |
| Microcks | sandbox | https://github.com/microcks/microcks | ✅ 200 | https://github.com/meshery/meshery | ✅ 200 | No |
| Porter | sandbox | https://github.com/getporter/porter | ✅ 200 | https://github.com/Porter | ✅ 200 | No |
| HolmesGPT | sandbox | https://github.com/HolmesGPT/holmesgpt | ✅ 200 | https://github.com/holmesgpt/ | ✅ 200 | No |
| Akri | sandbox | https://github.com/project-akri/akri | ✅ 200 | https://github.com/deislabs/akri -> https://github.com/project-akri/akri | ✅ 200 redirected | Yes |
| KitOps | sandbox | https://github.com/kitops-ml/kitops | ✅ 200 | https://github.com/jozu-ai/kitops -> https://github.com/kitops-ml/kitops | ✅ 200 redirected | Yes |
| Runme Notebooks | sandbox | https://github.com/runmedev/runme | ✅ 200 | https://github.com/stateful/runme -> https://github.com/runmedev/runme | ✅ 200 redirected | Yes |
| Cartography | sandbox | https://github.com/cartography-cncf/cartography | ✅ 200 | https://github.com/cartography-cncf/cartography | ✅ 200 | Yes |
| cert-manager | graduated | https://github.com/cert-manager/cert-manager | ✅ 200 | https://github.com/jetstack/cert-manager -> https://github.com/cert-manager/cert-manager | ✅ 200 redirected | Yes |
| Ratify | sandbox | https://github.com/ratify-project/ratify -> https://github.com/notaryproject/ratify | ✅ 200 redirected | https://github.com/deislabs/ratify -> https://github.com/notaryproject/ratify | ✅ 200 redirected | Yes |
| SOPS | sandbox | https://github.com/getsops/sops | ✅ 200 | https://github.com/mozilla/sops -> https://github.com/getsops/sops | ✅ 200 redirected | Yes |
| Teller | archived | https://github.com/tellerops/teller | ✅ 200 | https://github.com/SpectralOps/teller -> https://github.com/tellerops/teller | ✅ 200 redirected | Yes |
| composefs | sandbox | https://github.com/containers/composefs -> https://github.com/composefs/composefs | ✅ 200 redirected | https://github.com/containers/composefs -> https://github.com/composefs/composefs | ✅ 200 redirected | Yes |
| bootc | sandbox | https://github.com/bootc-dev/bootc | ✅ 200 | https://github.com/containers/bootc -> https://github.com/bootc-dev/bootc | ✅ 200 redirected | Yes |
| Inclavare Containers | sandbox | https://github.com/inclavare-containers/inclavare-containers | ✅ 200 | https://github.com/inclavare-containers/inclavare-containers | ✅ 200 | Yes |
| youki | sandbox | https://github.com/youki-dev/youki | ✅ 200 | https://github.com/containers/youki -> https://github.com/youki-dev/youki | ✅ 200 redirected | Yes |
| Kube-OVN | sandbox | https://github.com/kubeovn/kube-ovn | ✅ 200 | https://github.com/alauda/kube-ovn -> https://github.com/kubeovn/kube-ovn | ✅ 200 redirected | Yes |
| OVN-Kubernetes | sandbox | https://github.com/ovn-kubernetes/ovn-kubernetes | ✅ 200 | https://github.com/ovn-org/ovn-kubernetes -> https://github.com/ovn-kubernetes/ovn-kubernetes | ✅ 200 redirected | Yes |
| Cozystack | sandbox | https://github.com/cozystack/cozystack | ✅ 200 | https://github.com/aenix-io/cozystack/ -> https://github.com/cozystack/cozystack | ✅ 200 redirected | Yes |
| Eraser | sandbox | https://github.com/eraser-dev/eraser | ✅ 200 | https://github.com/eraser-dev/eraser | ✅ 200 | Yes |
| Kured | sandbox | https://github.com/kubereboot/kured | ✅ 200 | https://github.com/weaveworks/kured -> https://github.com/kubereboot/kured | ✅ 200 redirected | Yes |
| OpenELB | archived | https://github.com/openelb/openelb | ✅ 200 | https://github.com/kubesphere/openelb -> https://github.com/openelb/openelb | ✅ 200 redirected | Yes |
| Easegress | sandbox | https://github.com/easegress-io/easegress | ✅ 200 | https://github.com/megaease/easegress -> https://github.com/easegress-io/easegress | ✅ 200 redirected | Yes |
| DevSpace | sandbox | https://github.com/devspace-sh/devspace | ✅ 200 | https://github.com/loft-sh/devspace -> https://github.com/devspace-sh/devspace | ✅ 200 redirected | Yes |
| ModelPack | sandbox | https://github.com/modelpack/model-spec | ✅ 200 | https://github.com/CloudNativeAI/model-spec -> https://github.com/modelpack/model-spec | ✅ 200 redirected | Yes |
| sealer | archived | https://github.com/sealerio/sealer | ✅ 200 | https://github.com/alibaba/sealer -> https://github.com/sealerio/sealer | ✅ 200 redirected | Yes |
| Visual Studio Code Kubernetes Tools | sandbox | https://github.com/vscode-kubernetes-tools/vscode-kubernetes-tools | ✅ 200 | https://github.com/Azure/vscode-kubernetes-tools -> https://github.com/vscode-kubernetes-tools/vscode-kubernetes-tools | ✅ 200 redirected | Yes |
| SlimFaaS | sandbox | https://github.com/SlimPlanet/SlimFaas | ✅ 200 | https://github.com/AxaFrance/SlimFaas -> https://github.com/SlimPlanet/SlimFaas | ✅ 200 redirected | Yes |
| OpenCost | incubating | https://github.com/opencost/opencost | ✅ 200 | https://github.com/kubecost/cost-model -> https://github.com/opencost/opencost | ✅ 200 redirected | Yes |
| Headlamp | sandbox | https://github.com/kubernetes-sigs/headlamp | ✅ 200 | https://github.com/kubernetes-sigs/headlamp | ✅ 200 | Yes |
| Pixie | sandbox | https://github.com/pixie-io/pixie | ✅ 200 | https://github.com/pixie-labs/pixie -> https://github.com/pixie-io/pixie | ✅ 200 redirected | Yes |
| Trickster | sandbox | https://github.com/trickstercache/trickster | ✅ 200 | https://github.com/tricksterproxy/trickster -> https://github.com/trickstercache/trickster | ✅ 200 redirected | Yes |
| Spin | sandbox | https://github.com/spinframework/spin | ✅ 200 | https://github.com/fermyon/spin -> https://github.com/spinframework/spin | ✅ 200 redirected | Yes |
| container2wasm | sandbox | https://github.com/container2wasm/container2wasm | ✅ 200 | https://github.com/ktock/container2wasm -> https://github.com/container2wasm/container2wasm | ✅ 200 redirected | Yes |
| KAITO | sandbox | https://github.com/kaito-project/kaito | ✅ 200 | https://github.com/Azure/kaito -> https://github.com/kaito-project/kaito | ✅ 200 redirected | Yes |

## Non-Matching PCC Breakdown

This groups the entries that are not `Yes` in `Same final destination?`.

### 1) PCC missing entirely

- SpinKube

### 2) PCC points to an org/user page (not a repository path)

- kpt: https://github.com/kptdev
- OpenYurt: https://github.com/OpenYurt
- Fluid: https://github.com/Project-Fluid
- KAI Scheduler: https://github.com/kai-scheduler/
- KubeFleet: https://github.com/kubefleet-dev/
- Drasi: https://github.com/drasi-project
- KubeVela: https://github.com/kubevela
- Porter: https://github.com/Porter
- HolmesGPT: https://github.com/holmesgpt/

### 3) PCC points to a different valid repository

- Notary Project: https://github.com/theupdateframework/notary -> https://github.com/notaryproject/notary (Landscape uses https://github.com/notaryproject/notation)
- CubeFS: https://github.com/cubefs/cubefs (Landscape uses https://github.com/cubeFS/cubefs)
- Microcks: https://github.com/meshery/meshery (Landscape uses https://github.com/microcks/microcks)