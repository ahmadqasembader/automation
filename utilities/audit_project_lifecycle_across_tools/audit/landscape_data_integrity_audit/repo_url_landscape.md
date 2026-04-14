# Repo URL health check (Landscape vs PCC)

Generated from `landscape_source_diff.json` (`field = repo_url`) with `curl` URL checks.

Rule: when both URLs are GitHub and org/owner matches, repo path differences are treated as aligned.

| Project | Maturity | PCC URL | PCC | Landscape URL | Landscape | Org match | Same final URL | Result | Note |
|---|---|---|---|---|---|---|---|---|---|
| CubeFS | graduated | https://github.com/cubefs/cubefs | ✅ 200 | https://github.com/cubeFS/cubefs | ✅ 200 | Yes | No | Aligned (org match) | GitHub owner `cubefs` matches; repo path ignored. |
| Drasi | sandbox | https://github.com/drasi-project | ✅ 200 | http://github.com/drasi-project/drasi-platform | ❌ URLError | Yes | No | Aligned (org match) | GitHub owner `drasi-project` matches; repo path ignored. |
| Fluid | incubating | https://github.com/Project-Fluid | ✅ 200 | https://github.com/fluid-cloudnative/fluid | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/Project-Fluid` vs Landscape `https://github.com/fluid-cloudnative/fluid`. |
| HolmesGPT | sandbox | https://github.com/holmesgpt/ | ✅ 200 | https://github.com/HolmesGPT/holmesgpt | ✅ 200 | Yes | No | Aligned (org match) | GitHub owner `holmesgpt` matches; repo path ignored. |
| KAI Scheduler | sandbox | https://github.com/kai-scheduler/ | ✅ 200 | https://github.com/kai-scheduler/KAI-Scheduler | ✅ 200 | Yes | No | Aligned (org match) | GitHub owner `kai-scheduler` matches; repo path ignored. |
| kpt | sandbox | https://github.com/kptdev | ✅ 200 | https://github.com/kptdev/kpt | ✅ 200 | Yes | No | Aligned (org match) | GitHub owner `kptdev` matches; repo path ignored. |
| KubeFleet | sandbox | https://github.com/kubefleet-dev/ | ✅ 200 | https://github.com/kubefleet-dev/kubefleet | ✅ 200 | Yes | No | Aligned (org match) | GitHub owner `kubefleet-dev` matches; repo path ignored. |
| KubeVela | incubating | https://github.com/kubevela | ✅ 200 | https://github.com/kubevela/kubevela | ✅ 200 | Yes | No | Aligned (org match) | GitHub owner `kubevela` matches; repo path ignored. |
| Microcks | sandbox | https://github.com/meshery/meshery | ✅ 200 | https://github.com/microcks/microcks | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/meshery/meshery` vs Landscape `https://github.com/microcks/microcks`. |
| Notary Project | incubating | https://github.com/theupdateframework/notary | ✅ 200 | https://github.com/notaryproject/notation | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/notaryproject/notary` vs Landscape `https://github.com/notaryproject/notation`. |
| OpenYurt | incubating | https://github.com/OpenYurt | ✅ 200 | https://github.com/openyurtio/openyurt | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/OpenYurt` vs Landscape `https://github.com/openyurtio/openyurt`. |
| Porter | sandbox | https://github.com/Porter | ✅ 200 | https://github.com/getporter/porter | ✅ 200 | No | No | Mismatch | Different final destinations: PCC `https://github.com/Porter` vs Landscape `https://github.com/getporter/porter`. |
| SpinKube | sandbox | — | ❌ missing | https://github.com/spinframework/spin-operator | ✅ 200 | No | No | Missing URL | One side is missing. |
| Akri | sandbox | https://github.com/deislabs/akri | ✅ 200 | https://github.com/project-akri/akri | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| bootc | sandbox | https://github.com/containers/bootc | ✅ 200 | https://github.com/bootc-dev/bootc | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Cartography | sandbox | https://github.com/cartography-cncf/cartography | ✅ 200 | https://github.com/cartography-cncf/cartography | ✅ 200 | Yes | Yes | Aligned (org match) | GitHub owner `cartography-cncf` matches; repo path ignored. |
| cert-manager | graduated | https://github.com/jetstack/cert-manager | ✅ 200 | https://github.com/cert-manager/cert-manager | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| composefs | sandbox | https://github.com/containers/composefs | ✅ 200 | https://github.com/containers/composefs | ✅ 200 | Yes | Yes | Aligned (org match) | GitHub owner `containers` matches; repo path ignored. |
| container2wasm | sandbox | https://github.com/ktock/container2wasm | ✅ 200 | https://github.com/container2wasm/container2wasm | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Cozystack | sandbox | https://github.com/aenix-io/cozystack/ | ✅ 200 | https://github.com/cozystack/cozystack | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| DevSpace | sandbox | https://github.com/loft-sh/devspace | ✅ 200 | https://github.com/devspace-sh/devspace | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Easegress | sandbox | https://github.com/megaease/easegress | ✅ 200 | https://github.com/easegress-io/easegress | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Eraser | sandbox | https://github.com/eraser-dev/eraser | ✅ 200 | https://github.com/eraser-dev/eraser | ✅ 200 | Yes | Yes | Aligned (org match) | GitHub owner `eraser-dev` matches; repo path ignored. |
| Headlamp | sandbox | https://github.com/kubernetes-sigs/headlamp | ✅ 200 | https://github.com/kubernetes-sigs/headlamp | ✅ 200 | Yes | Yes | Aligned (org match) | GitHub owner `kubernetes-sigs` matches; repo path ignored. |
| Inclavare Containers | sandbox | https://github.com/inclavare-containers/inclavare-containers | ✅ 200 | https://github.com/inclavare-containers/inclavare-containers | ✅ 200 | Yes | Yes | Aligned (org match) | GitHub owner `inclavare-containers` matches; repo path ignored. |
| KAITO | sandbox | https://github.com/Azure/kaito | ✅ 200 | https://github.com/kaito-project/kaito | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| KitOps | sandbox | https://github.com/jozu-ai/kitops | ✅ 200 | https://github.com/kitops-ml/kitops | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Kube-OVN | sandbox | https://github.com/alauda/kube-ovn | ✅ 200 | https://github.com/kubeovn/kube-ovn | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Kured | sandbox | https://github.com/weaveworks/kured | ✅ 200 | https://github.com/kubereboot/kured | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| ModelPack | sandbox | https://github.com/CloudNativeAI/model-spec | ✅ 200 | https://github.com/modelpack/model-spec | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| OpenCost | incubating | https://github.com/kubecost/cost-model | ✅ 200 | https://github.com/opencost/opencost | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| OpenELB | archived | https://github.com/kubesphere/openelb | ✅ 200 | https://github.com/openelb/openelb | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| OVN-Kubernetes | sandbox | https://github.com/ovn-org/ovn-kubernetes | ✅ 200 | https://github.com/ovn-kubernetes/ovn-kubernetes | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Pixie | sandbox | https://github.com/pixie-labs/pixie | ✅ 200 | https://github.com/pixie-io/pixie | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Ratify | sandbox | https://github.com/deislabs/ratify | ✅ 200 | https://github.com/ratify-project/ratify | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Runme Notebooks | sandbox | https://github.com/stateful/runme | ✅ 200 | https://github.com/runmedev/runme | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| sealer | archived | https://github.com/alibaba/sealer | ✅ 200 | https://github.com/sealerio/sealer | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| SlimFaaS | sandbox | https://github.com/AxaFrance/SlimFaas | ✅ 200 | https://github.com/SlimPlanet/SlimFaas | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| SOPS | sandbox | https://github.com/mozilla/sops | ✅ 200 | https://github.com/getsops/sops | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Spin | sandbox | https://github.com/fermyon/spin | ✅ 200 | https://github.com/spinframework/spin | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Teller | archived | https://github.com/SpectralOps/teller | ✅ 200 | https://github.com/tellerops/teller | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Trickster | sandbox | https://github.com/tricksterproxy/trickster | ✅ 200 | https://github.com/trickstercache/trickster | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| Visual Studio Code Kubernetes Tools | sandbox | https://github.com/Azure/vscode-kubernetes-tools | ✅ 200 | https://github.com/vscode-kubernetes-tools/vscode-kubernetes-tools | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
| youki | sandbox | https://github.com/containers/youki | ✅ 200 | https://github.com/youki-dev/youki | ✅ 200 | No | Yes | Aligned (same final URL) | URLs converge to same effective destination. |
