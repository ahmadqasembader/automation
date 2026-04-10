# Landscape data integrity audit

Source: vendored `datasources/landscape.yml` in this repository.

## Scope

CNCF items with `project` (or `extra.project`) in: archived, graduated, incubating, sandbox.

## Lifecycle date rules

| Maturity | Required `extra` date fields |
|----------|-------------------------------|
| sandbox | `accepted` |
| incubating | `accepted`, `incubating` |
| graduated | `accepted`, `incubating`, `graduated` |
| archived | `accepted`, `archived` |

## Legend

- **dates_ok** / **dates_detail**: required lifecycle date keys under `extra:` for this maturity.
- **Yes** / **No** (most columns): that landscape field is non-empty.
- **logo**: **Yes** = `logo:` set to a project asset (not the CNCF placeholder); **cncf logo** = generic `cncf.svg`; **No** = missing/empty.
- **Datasource hints** (where we can source fixes later):
  - **slug**: `pcc_projects.yaml` → `slug`
  - **repo**: `pcc_projects.yaml` → `repository_url`
  - **logo**: `pcc_projects.yaml` → `project_logo` (filename vs placeholder)
  - **devstats**: `clomonitor.yaml` → `devstats_url`; `devstats.html`
  - **clomon**: `clomonitor.yaml` → project `name`
  - **accepted**: `clomonitor.yaml` → `accepted_at`
  - **artwork**: `clomonitor.yaml` → `logo_url`; `artwork.md`

**Projects in scope:** 251

**Lifecycle date failures:** 1

## Matrix (by maturity)

### Graduated

**Count:** 35

| Project | Path | dates_ok | dates_detail | slug | repo | logo | devstats | clomon | accepted | artwork |
|---|---|---|---|---|---|---|---|---|---|---|
| Argo | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| cert-manager | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Cilium | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| CloudEvents | App Definition and Development / Streaming & Messaging | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| containerd | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| CoreDNS | Orchestration & Management / Coordination & Service Discovery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| CRI-O | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Crossplane | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| CubeFS | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Dapr | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Dragonfly | Provisioning / Container Registry | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Envoy | Orchestration & Management / Service Proxy | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| etcd | Orchestration & Management / Coordination & Service Discovery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Falco | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Fluentd | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Flux | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Harbor | Provisioning / Container Registry | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Helm | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| in-toto | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Istio | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Jaeger | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KEDA | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Knative | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KubeEdge | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kubernetes | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kyverno | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Linkerd | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Open Policy Agent (OPA) | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Prometheus | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Rook | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| SPIFFE | Provisioning / Key Management | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| SPIRE | Provisioning / Key Management | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| The Update Framework (TUF) | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| TiKV | App Definition and Development / Database | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Vitess | App Definition and Development / Database | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

### Incubating

**Count:** 36

| Project | Path | dates_ok | dates_detail | slug | repo | logo | devstats | clomon | accepted | artwork |
|---|---|---|---|---|---|---|---|---|---|---|
| Artifact Hub | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Backstage | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Buildpacks | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Chaos Mesh | Observability and Analysis / Chaos Engineering | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Cloud Custodian | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Container Network Interface (CNI) | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Contour | Orchestration & Management / Service Proxy | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Cortex | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Emissary-Ingress | Orchestration & Management / API Gateway | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Flatcar Container Linux | Platform / Certified Kubernetes - Distribution | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Fluid | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gRPC | Orchestration & Management / Remote Procedure Call | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Karmada | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Keycloak | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KServe | CNAI / ML Serving | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kubeflow | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kubescape | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KubeVela | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KubeVirt | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Lima | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Litmus | Observability and Analysis / Chaos Engineering | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Longhorn | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| metal3-io | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| NATS | App Definition and Development / Streaming & Messaging | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Notary Project | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenCost | Observability and Analysis / Continuous Optimization | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenFeature | Observability and Analysis / Feature Flagging | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenFGA | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenKruise | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenTelemetry | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenYurt | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Operator Framework | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Strimzi | App Definition and Development / Streaming & Messaging | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Thanos | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Volcano | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| wasmCloud | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

### Sandbox

**Count:** 154

| Project | Path | dates_ok | dates_detail | slug | repo | logo | devstats | clomon | accepted | artwork |
|---|---|---|---|---|---|---|---|---|---|---|
| Aeraki Mesh | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Agones | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | cncf logo | Yes | Yes | Yes | No |
| Akri | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Antrea | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Armada | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Athenz | Provisioning / Key Management | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Atlantis | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Bank-Vaults | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| BFE | Orchestration & Management / Service Proxy | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| bootc | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| bpfman | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Cadence Workflow | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Capsule | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Carina | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Cartography | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Carvel | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| CDK for Kubernetes (CDK8s) | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Cedar | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | No | Yes | Yes | No |
| Chaosblade | Observability and Analysis / Chaos Engineering | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| CloudNativePG | App Definition and Development / Database | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Clusternet | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Clusterpedia | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| CoHDI | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | cncf logo | Yes | Yes | Yes | No |
| composefs | Runtime / Container Runtime | pass | ok | Yes | Yes | cncf logo | Yes | Yes | Yes | No |
| Confidential Containers | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Connect RPC | Orchestration & Management / Remote Procedure Call | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| container2wasm | Wasm / Orchestration & Management | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| ContainerSSH | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Copa | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Cozystack | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Cozystack | Platform / PaaS/Container Service | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Dalec | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Devfile | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| DevSpace | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Dex | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Distribution | Provisioning / Container Registry | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Drasi | App Definition and Development / Streaming & Messaging | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Easegress | Orchestration & Management / API Gateway | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Eraser | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| external-secrets | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| hami | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Headlamp | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Hexa | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Higress | Orchestration & Management / API Gateway | pass | ok | No | Yes | Yes | No | No | Yes | No |
| HolmesGPT | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| HwameiStor | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Hyperlight | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Inclavare Containers | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Inspektor Gadget | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Interlink | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| k0s | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| k3s | Platform / Certified Kubernetes - Distribution | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| k8gb | Orchestration & Management / Coordination & Service Discovery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| K8sGPT | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| K8up | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| kagent | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KAI Scheduler | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | cncf logo | Yes | Yes | Yes | No |
| Kairos | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KAITO | CNAI / ML Serving | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kanister | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KCL | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| kcp | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kepler | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Keylime | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kgateway | Orchestration & Management / API Gateway | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KitOps | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kmesh | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| ko | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Konveyor | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Koordinator | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| kpt | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Krkn | Observability and Analysis / Chaos Engineering | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kuadrant | Orchestration & Management / API Gateway | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kuasar | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kube-burner | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kube-OVN | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| kube-rs | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| kube-vip | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | No |
| Kubean | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KubeArmor | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KubeClipper | Platform / Certified Kubernetes - Installer | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KubeElasti | Serverless / Framework | pass | ok | Yes | Yes | cncf logo | Yes | Yes | Yes | No |
| KubeFleet | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kuberhealthy | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KubeSlice | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KubeStellar | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kubewarden | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KUDO | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kuma | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Kured | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| KusionStack | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Logging Operator (Kube Logging) | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| LoxiLB | Orchestration & Management / Service Proxy | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Meshery | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| MetalLB | Orchestration & Management / Service Proxy | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Microcks | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| ModelPack | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Monocle | Observability and Analysis / Observability | fail | missing:accepted | No | Yes | Yes | No | No | No | Yes |
| Network Service Mesh | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| NMstate | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OAuth2 Proxy | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Open Cluster Management | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Open Policy Containers | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenChoreo | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenEBS | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenEverest | App Definition and Development / Database | pass | ok | Yes | Yes | Yes | No | Yes | Yes | No |
| OpenFunction | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| openGemini | App Definition and Development / Database | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenGitOps | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OpenTofu | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| ORAS | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OSCAL-COMPASS | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| OVN-Kubernetes | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Oxia | Orchestration & Management / Coordination & Service Discovery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | No |
| Paralus | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Parsec | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Perses | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| PipeCD | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Piraeus Datastore | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | No | Yes | Yes | Yes |
| Pixie | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Podman Container Tools | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Podman Desktop | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Porter | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Radius | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Ratify | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Runme Notebooks | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| SchemaHero | App Definition and Development / Database | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Score | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Sermant | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Serverless Devs | Orchestration & Management / Scheduling & Orchestration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Serverless Workflow | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Shipwright | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| SlimFaaS | Serverless / Installable Platform | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| SlimToolkit | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| SOPS | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Spiderpool | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Spin | Wasm / Application Frameworks | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| SpinKube | Wasm / Orchestration & Management | pass | ok | No | Yes | Yes | Yes | Yes | Yes | Yes |
| Stacker | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Submariner | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Telepresence | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Tinkerbell | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Tokenetes | Provisioning / Security & Compliance | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Tremor | App Definition and Development / Streaming & Messaging | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Trickster | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| urunc | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Vineyard | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Virtual Kubelet | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Visual Studio Code Kubernetes Tools | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| WasmEdge Runtime | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| werf | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| xRegistry | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| youki | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| zot | Provisioning / Container Registry | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |

### Archived

**Count:** 26

| Project | Path | dates_ok | dates_detail | slug | repo | logo | devstats | clomon | accepted | artwork |
|---|---|---|---|---|---|---|---|---|---|---|
| Brigade | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | No | No | Yes | Yes |
| CNI-Genie | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | No |
| Curiefense | Provisioning / Security & Compliance | pass | ok | Yes | No | Yes | Yes | No | Yes | Yes |
| Curve | Runtime / Cloud Native Storage | pass | ok | Yes | Yes | Yes | No | Yes | Yes | No |
| DevStream | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | No |
| FabEdge | Runtime / Cloud Native Network | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Fonio | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | No | No | Yes | No |
| Keptn | App Definition and Development / Continuous Integration & Delivery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Krator | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | No | Yes | No |
| Krustlet | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | No | No | Yes | No |
| KubeDL | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Merbridge | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Nocalhost | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Open Service Mesh | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | No | No | Yes | Yes |
| OpenELB | Orchestration & Management / Service Proxy | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | No |
| OpenMetrics | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | Yes | No | Yes | Yes |
| OpenTracing | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | No | No | Yes | Yes |
| Pravega | App Definition and Development / Streaming & Messaging | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| rkt | Runtime / Container Runtime | pass | ok | Yes | Yes | Yes | No | No | Yes | Yes |
| sealer | App Definition and Development / Application Definition & Image Build | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | No |
| Service Mesh Interface (SMI) | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | No | No | Yes | No |
| Service Mesh Performance | Orchestration & Management / Service Mesh | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Skooner | Observability and Analysis / Observability | pass | ok | Yes | Yes | Yes | No | Yes | Yes | No |
| SuperEdge | Provisioning / Automation & Configuration | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| Teller | Provisioning / Key Management | pass | ok | Yes | Yes | Yes | No | Yes | Yes | No |
| Xline | Orchestration & Management / Coordination & Service Discovery | pass | ok | Yes | Yes | Yes | Yes | Yes | Yes | No |


## Lifecycle date failures (detail)

| Project | Maturity | Missing |
|---------|----------|---------|
| Monocle | sandbox | `accepted` |