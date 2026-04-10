# Landscape vs datasources diff

**Canonical:** `datasources/pcc_projects.yaml` and `datasources/clomonitor.yaml`. 
When those two disagree, that is called out. **`landscape.yml` should be updated** to match the agreed sources (or you must reconcile PCC vs CLOMonitor first).

## Summary

- **CNCF landscape items in scope:** 251
- **With at least one drift / conflict row:** 188
- **Findings where PCC and CLOMonitor disagree:** 219
- **No PCC and no CLOMonitor match:** 4

## Per-project: landscape vs sources

### CNI-Genie (archived)

- **Path:** Runtime / Cloud Native Network
- **Matched:** PCC=True, CLOMonitor=False (pcc_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/cni-genie/CNI-Genie | https://github.com/CNI-Genie | — | — | Landscape ('https://github.com/cni-genie/CNI-Genie') ≠ PCC ('https://github.com/CNI-Genie'). |

### Keptn (archived)

- **Path:** App Definition and Development / Continuous Integration & Delivery
- **Matched:** PCC=True, CLOMonitor=False (pcc_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/keptn/lifecycle-toolkit | https://github.com/keptn/keptn | — | — | Landscape ('https://github.com/keptn/lifecycle-toolkit') ≠ PCC ('https://github.com/keptn/keptn'). |

### KubeDL (archived)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=False (pcc_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubedl-io/kubedl | https://github.com/kubedl-io | — | — | Landscape ('https://github.com/kubedl-io/kubedl') ≠ PCC ('https://github.com/kubedl-io'). |

### OpenELB (archived)

- **Path:** Orchestration & Management / Service Proxy
- **Matched:** PCC=True, CLOMonitor=False (pcc_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/openelb/openelb | https://github.com/kubesphere/openelb | — | — | Landscape ('https://github.com/openelb/openelb') ≠ PCC ('https://github.com/kubesphere/openelb'). |

### OpenTracing (archived)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=False (pcc_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/opentracing/opentracing-go | https://github.com/opentracing | — | — | Landscape ('https://github.com/opentracing/opentracing-go') ≠ PCC ('https://github.com/opentracing'). |

### sealer (archived)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=False (pcc_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/sealerio/sealer | https://github.com/alibaba/sealer | — | — | Landscape ('https://github.com/sealerio/sealer') ≠ PCC ('https://github.com/alibaba/sealer'). |

### Service Mesh Performance (archived)

- **Path:** Orchestration & Management / Service Mesh
- **Matched:** PCC=True, CLOMonitor=False (lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/service-mesh-performance/service-mesh-… | https://github.com/service-mesh-performance | — | — | Landscape ('https://github.com/service-mesh-performance/service-mesh-performance') ≠ PCC ('https://github.com/service-mesh-performance'). |
| project (maturity) | archived | sandbox | — | — | Landscape ('archived') ≠ PCC ('sandbox'). |

### SuperEdge (archived)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=False (pcc_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/superedge/superedge | https://github.com/superedge | — | — | Landscape ('https://github.com/superedge/superedge') ≠ PCC ('https://github.com/superedge'). |

### Teller (archived)

- **Path:** Provisioning / Key Management
- **Matched:** PCC=True, CLOMonitor=False (pcc_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/tellerops/teller | https://github.com/SpectralOps/teller | — | — | Landscape ('https://github.com/tellerops/teller') ≠ PCC ('https://github.com/SpectralOps/teller'). |

### Argo (graduated)

- **Path:** App Definition and Development / Continuous Integration & Delivery
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/argoproj/argo-cd | https://github.com/argoproj/argoproj | https://github.com/argoproj/argo-cd | **No** | PCC ('https://github.com/argoproj/argoproj') and CLOMonitor ('https://github.com/argoproj/argo-cd') disagree. Landscape ('https://github.com/argoproj/argo-cd') ≠ PCC ('https://github.com/argoproj/argoproj'). |
| extra.accepted | 2020-03-26 | — | 2020-04-07 | — | Landscape ('2020-03-26') ≠ CLOMonitor ('2020-04-07'). |

### cert-manager (graduated)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/cert-manager/cert-manager | https://github.com/jetstack/cert-manager | https://github.com/cert-manager/community | **No** | PCC ('https://github.com/jetstack/cert-manager') and CLOMonitor ('https://github.com/cert-manager/community') disagree. Landscape ('https://github.com/cert-manager/cert-manager') ≠ PCC ('https://github.com/jetstack/cert-manager'). Landscape ('https://github.com/cert-manager/cert-manager') ≠ CLOMonitor ('https://github.com/cert-manager/community'). |

### Cilium (graduated)

- **Path:** Runtime / Cloud Native Network
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/cilium/cilium | https://github.com/cilium/cilium | https://github.com/cilium/ebpf | **No** | PCC ('https://github.com/cilium/cilium') and CLOMonitor ('https://github.com/cilium/ebpf') disagree. Landscape ('https://github.com/cilium/cilium') ≠ CLOMonitor ('https://github.com/cilium/ebpf'). |

### CloudEvents (graduated)

- **Path:** App Definition and Development / Streaming & Messaging
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/cloudevents/spec | https://github.com/cloudevents | https://github.com/cloudevents/spec | **No** | PCC ('https://github.com/cloudevents') and CLOMonitor ('https://github.com/cloudevents/spec') disagree. Landscape ('https://github.com/cloudevents/spec') ≠ PCC ('https://github.com/cloudevents'). |
| extra.accepted | 2018-05-15 | — | 2018-05-22 | — | Landscape ('2018-05-15') ≠ CLOMonitor ('2018-05-22'). |

### containerd (graduated)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/containerd/containerd | https://github.com/containerd | https://github.com/containerd/containerd | **No** | PCC ('https://github.com/containerd') and CLOMonitor ('https://github.com/containerd/containerd') disagree. Landscape ('https://github.com/containerd/containerd') ≠ PCC ('https://github.com/containerd'). |

### CoreDNS (graduated)

- **Path:** Orchestration & Management / Coordination & Service Discovery
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | coredns | core-dns | **No** | PCC slug 'coredns' vs CLOMonitor name 'core-dns' (normalized identifiers differ). |
| repo_url | https://github.com/coredns/coredns | https://github.com/coredns | https://github.com/coredns/coredns | **No** | PCC ('https://github.com/coredns') and CLOMonitor ('https://github.com/coredns/coredns') disagree. Landscape ('https://github.com/coredns/coredns') ≠ PCC ('https://github.com/coredns'). |
| extra.lfx_slug | coredns | coredns | core-dns | **No** | PCC ('coredns') and CLOMonitor ('core-dns') disagree. Landscape ('coredns') ≠ CLOMonitor ('core-dns'). |

### CRI-O (graduated)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/cri-o/cri-o | https://github.com/cri-o | https://github.com/cri-o/cri-o | **No** | PCC ('https://github.com/cri-o') and CLOMonitor ('https://github.com/cri-o/cri-o') disagree. Landscape ('https://github.com/cri-o/cri-o') ≠ PCC ('https://github.com/cri-o'). |

### Crossplane (graduated)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2020-06-25 | — | 2020-06-23 | — | Landscape ('2020-06-25') ≠ CLOMonitor ('2020-06-23'). |

### CubeFS (graduated)

- **Path:** Runtime / Cloud Native Storage
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | chubaofs | chubao-fs | **No** | PCC slug 'chubaofs' vs CLOMonitor name 'chubao-fs' (normalized identifiers differ). |
| repo_url | https://github.com/cubeFS/cubefs | https://github.com/cubefs/cubefs | https://github.com/chubaofs/chubaofs | **No** | PCC ('https://github.com/cubefs/cubefs') and CLOMonitor ('https://github.com/chubaofs/chubaofs') disagree. Landscape ('https://github.com/cubeFS/cubefs') ≠ CLOMonitor ('https://github.com/chubaofs/chubaofs'). |
| extra.lfx_slug | chubaofs | chubaofs | chubao-fs | **No** | PCC ('chubaofs') and CLOMonitor ('chubao-fs') disagree. Landscape ('chubaofs') ≠ CLOMonitor ('chubao-fs'). |
| extra.accepted | 2019-12-16 | — | 2019-12-17 | — | Landscape ('2019-12-16') ≠ CLOMonitor ('2019-12-17'). |

### Dapr (graduated)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/dapr/dapr | https://github.com/dapr | https://github.com/dapr/dapr | **No** | PCC ('https://github.com/dapr') and CLOMonitor ('https://github.com/dapr/dapr') disagree. Landscape ('https://github.com/dapr/dapr') ≠ PCC ('https://github.com/dapr'). |
| extra.accepted | 2021-11-09 | — | 2021-11-03 | — | Landscape ('2021-11-09') ≠ CLOMonitor ('2021-11-03'). |

### Dragonfly (graduated)

- **Path:** Provisioning / Container Registry
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | d7y | dragonfly | **No** | PCC slug 'd7y' vs CLOMonitor name 'dragonfly' (normalized identifiers differ). |
| repo_url | https://github.com/dragonflyoss/dragonfly | https://github.com/dragonflyoss/Dragonfly | https://github.com/dragonflyoss/Dragonfly2 | **No** | PCC ('https://github.com/dragonflyoss/Dragonfly') and CLOMonitor ('https://github.com/dragonflyoss/Dragonfly2') disagree. Landscape ('https://github.com/dragonflyoss/dragonfly') ≠ CLOMonitor ('https://github.com/dragonflyoss/Dragonfly2'). |
| extra.lfx_slug | d7y | d7y | dragonfly | **No** | PCC ('d7y') and CLOMonitor ('dragonfly') disagree. Landscape ('d7y') ≠ CLOMonitor ('dragonfly'). |
| extra.accepted | 2018-11-13 | — | 2018-11-15 | — | Landscape ('2018-11-13') ≠ CLOMonitor ('2018-11-15'). |

### Envoy (graduated)

- **Path:** Orchestration & Management / Service Proxy
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/envoyproxy/envoy | https://github.com/envoyproxy/envoy | https://github.com/envoyproxy/go-control-plane | **No** | PCC ('https://github.com/envoyproxy/envoy') and CLOMonitor ('https://github.com/envoyproxy/go-control-plane') disagree. Landscape ('https://github.com/envoyproxy/envoy') ≠ CLOMonitor ('https://github.com/envoyproxy/go-control-plane'). |

### etcd (graduated)

- **Path:** Orchestration & Management / Coordination & Service Discovery
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/etcd-io/etcd | https://github.com/etcd-io | https://github.com/etcd-io/etcd | **No** | PCC ('https://github.com/etcd-io') and CLOMonitor ('https://github.com/etcd-io/etcd') disagree. Landscape ('https://github.com/etcd-io/etcd') ≠ PCC ('https://github.com/etcd-io'). |

### Fluentd (graduated)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/fluent/fluentd | https://github.com/fluent | https://github.com/fluent/fluent-bit | **No** | PCC ('https://github.com/fluent') and CLOMonitor ('https://github.com/fluent/fluent-bit') disagree. Landscape ('https://github.com/fluent/fluentd') ≠ PCC ('https://github.com/fluent'). Landscape ('https://github.com/fluent/fluentd') ≠ CLOMonitor ('https://github.com/fluent/fluent-bit'). |

### Flux (graduated)

- **Path:** App Definition and Development / Continuous Integration & Delivery
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | fluxcd | flux-project | **No** | PCC slug 'fluxcd' vs CLOMonitor name 'flux-project' (normalized identifiers differ). |
| repo_url | https://github.com/fluxcd/flux2 | https://github.com/fluxcd | https://github.com/fluxcd/community | **No** | PCC ('https://github.com/fluxcd') and CLOMonitor ('https://github.com/fluxcd/community') disagree. Landscape ('https://github.com/fluxcd/flux2') ≠ PCC ('https://github.com/fluxcd'). Landscape ('https://github.com/fluxcd/flux2') ≠ CLOMonitor ('https://github.com/fluxcd/community'). |
| extra.lfx_slug | fluxcd | fluxcd | flux-project | **No** | PCC ('fluxcd') and CLOMonitor ('flux-project') disagree. Landscape ('fluxcd') ≠ CLOMonitor ('flux-project'). |

### Harbor (graduated)

- **Path:** Provisioning / Container Registry
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/goharbor/harbor | https://github.com/goharbor | https://github.com/goharbor/harbor | **No** | PCC ('https://github.com/goharbor') and CLOMonitor ('https://github.com/goharbor/harbor') disagree. Landscape ('https://github.com/goharbor/harbor') ≠ PCC ('https://github.com/goharbor'). |

### Helm (graduated)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/helm/helm | https://github.com/helm | https://github.com/helm/helm | **No** | PCC ('https://github.com/helm') and CLOMonitor ('https://github.com/helm/helm') disagree. Landscape ('https://github.com/helm/helm') ≠ PCC ('https://github.com/helm'). |

### in-toto (graduated)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | intoto | in-toto | **No** | PCC slug 'intoto' vs CLOMonitor name 'in-toto' (normalized identifiers differ). |
| extra.lfx_slug | intoto | intoto | in-toto | **No** | PCC ('intoto') and CLOMonitor ('in-toto') disagree. Landscape ('intoto') ≠ CLOMonitor ('in-toto'). |
| extra.accepted | 2019-08-14 | — | 2019-08-21 | — | Landscape ('2019-08-14') ≠ CLOMonitor ('2019-08-21'). |

### Istio (graduated)

- **Path:** Orchestration & Management / Service Mesh
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/istio/istio | https://github.com/istio | https://github.com/istio/istio | **No** | PCC ('https://github.com/istio') and CLOMonitor ('https://github.com/istio/istio') disagree. Landscape ('https://github.com/istio/istio') ≠ PCC ('https://github.com/istio'). |
| extra.accepted | 2022-09-30 | — | 2022-09-28 | — | Landscape ('2022-09-30') ≠ CLOMonitor ('2022-09-28'). |

### KEDA (graduated)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kedacore/keda | https://github.com/kedacore | https://github.com/kedacore/keda | **No** | PCC ('https://github.com/kedacore') and CLOMonitor ('https://github.com/kedacore/keda') disagree. Landscape ('https://github.com/kedacore/keda') ≠ PCC ('https://github.com/kedacore'). |
| extra.accepted | 2020-03-12 | — | 2020-03-09 | — | Landscape ('2020-03-12') ≠ CLOMonitor ('2020-03-09'). |

### Knative (graduated)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/knative/serving | https://github.com/knative/ | https://github.com/knative/docs/ | **No** | PCC ('https://github.com/knative/') and CLOMonitor ('https://github.com/knative/docs/') disagree. Landscape ('https://github.com/knative/serving') ≠ PCC ('https://github.com/knative/'). Landscape ('https://github.com/knative/serving') ≠ CLOMonitor ('https://github.com/knative/docs/'). |

### KubeEdge (graduated)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | kubeedge | kube-edge | **No** | PCC slug 'kubeedge' vs CLOMonitor name 'kube-edge' (normalized identifiers differ). |
| repo_url | https://github.com/kubeedge/kubeedge | https://github.com/kubeedge/kubeedge | https://github.com/kubeedge/sedna | **No** | PCC ('https://github.com/kubeedge/kubeedge') and CLOMonitor ('https://github.com/kubeedge/sedna') disagree. Landscape ('https://github.com/kubeedge/kubeedge') ≠ CLOMonitor ('https://github.com/kubeedge/sedna'). |
| extra.lfx_slug | kubeedge | kubeedge | kube-edge | **No** | PCC ('kubeedge') and CLOMonitor ('kube-edge') disagree. Landscape ('kubeedge') ≠ CLOMonitor ('kube-edge'). |

### Kubernetes (graduated)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | k8s | kubernetes | **No** | PCC slug 'k8s' vs CLOMonitor name 'kubernetes' (normalized identifiers differ). |
| repo_url | https://github.com/kubernetes/kubernetes | https://github.com/kubernetes | https://github.com/kubernetes/kubernetes | **No** | PCC ('https://github.com/kubernetes') and CLOMonitor ('https://github.com/kubernetes/kubernetes') disagree. Landscape ('https://github.com/kubernetes/kubernetes') ≠ PCC ('https://github.com/kubernetes'). |
| extra.lfx_slug | k8s | k8s | kubernetes | **No** | PCC ('k8s') and CLOMonitor ('kubernetes') disagree. Landscape ('k8s') ≠ CLOMonitor ('kubernetes'). |

### Linkerd (graduated)

- **Path:** Orchestration & Management / Service Mesh
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/linkerd/linkerd2 | https://github.com/linkerd | https://github.com/linkerd/linkerd2-proxy | **No** | PCC ('https://github.com/linkerd') and CLOMonitor ('https://github.com/linkerd/linkerd2-proxy') disagree. Landscape ('https://github.com/linkerd/linkerd2') ≠ PCC ('https://github.com/linkerd'). Landscape ('https://github.com/linkerd/linkerd2') ≠ CLOMonitor ('https://github.com/linkerd/linkerd2-proxy'). |

### Open Policy Agent (OPA) (graduated)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | openpolicyagent | opa | **No** | PCC slug 'openpolicyagent' vs CLOMonitor name 'opa' (normalized identifiers differ). |
| repo_url | https://github.com/open-policy-agent/opa | https://github.com/open-policy-agent | https://github.com/open-policy-agent/conftest | **No** | PCC ('https://github.com/open-policy-agent') and CLOMonitor ('https://github.com/open-policy-agent/conftest') disagree. Landscape ('https://github.com/open-policy-agent/opa') ≠ PCC ('https://github.com/open-policy-agent'). Landscape ('https://github.com/open-policy-agent/opa') ≠ CLOMonitor ('https://github.com/open-policy-agent/conftest'). |
| extra.lfx_slug | openpolicyagent | openpolicyagent | opa | **No** | PCC ('openpolicyagent') and CLOMonitor ('opa') disagree. Landscape ('openpolicyagent') ≠ CLOMonitor ('opa'). |

### Prometheus (graduated)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+pcc_via_clo_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/prometheus/prometheus | https://github.com/prometheus | https://github.com/prometheus/docs | **No** | PCC ('https://github.com/prometheus') and CLOMonitor ('https://github.com/prometheus/docs') disagree. Landscape ('https://github.com/prometheus/prometheus') ≠ PCC ('https://github.com/prometheus'). Landscape ('https://github.com/prometheus/prometheus') ≠ CLOMonitor ('https://github.com/prometheus/docs'). |
| extra.lfx_slug | prometheus_del | prometheus | prometheus | Yes | Landscape ('prometheus_del') ≠ PCC ('prometheus'). Landscape ('prometheus_del') ≠ CLOMonitor ('prometheus'). |

### Rook (graduated)

- **Path:** Runtime / Cloud Native Storage
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/rook/rook | https://github.com/rook | https://github.com/rook/rook | **No** | PCC ('https://github.com/rook') and CLOMonitor ('https://github.com/rook/rook') disagree. Landscape ('https://github.com/rook/rook') ≠ PCC ('https://github.com/rook'). |

### SPIFFE (graduated)

- **Path:** Provisioning / Key Management
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/spiffe/spiffe | https://github.com/spiffe | https://github.com/spiffe/spiffe | **No** | PCC ('https://github.com/spiffe') and CLOMonitor ('https://github.com/spiffe/spiffe') disagree. Landscape ('https://github.com/spiffe/spiffe') ≠ PCC ('https://github.com/spiffe'). |

### The Update Framework (TUF) (graduated)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/theupdateframework/python-tuf | https://github.com/theupdateframework | https://github.com/theupdateframework/specification | **No** | PCC ('https://github.com/theupdateframework') and CLOMonitor ('https://github.com/theupdateframework/specification') disagree. Landscape ('https://github.com/theupdateframework/python-tuf') ≠ PCC ('https://github.com/theupdateframework'). Landscape ('https://github.com/theupdateframework/python-tuf') ≠ CLOMonitor ('https://github.com/theupdateframework/specification'). |

### TiKV (graduated)

- **Path:** App Definition and Development / Database
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/tikv/tikv | https://github.com/tikv | https://github.com/tikv/tikv | **No** | PCC ('https://github.com/tikv') and CLOMonitor ('https://github.com/tikv/tikv') disagree. Landscape ('https://github.com/tikv/tikv') ≠ PCC ('https://github.com/tikv'). |

### Vitess (graduated)

- **Path:** App Definition and Development / Database
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/vitessio/vitess | https://github.com/vitessio | https://github.com/vitessio/vitess | **No** | PCC ('https://github.com/vitessio') and CLOMonitor ('https://github.com/vitessio/vitess') disagree. Landscape ('https://github.com/vitessio/vitess') ≠ PCC ('https://github.com/vitessio'). |

### Artifact Hub (incubating)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/artifacthub/hub | https://github.com/artifacthub | https://github.com/artifacthub/hub | **No** | PCC ('https://github.com/artifacthub') and CLOMonitor ('https://github.com/artifacthub/hub') disagree. Landscape ('https://github.com/artifacthub/hub') ≠ PCC ('https://github.com/artifacthub'). |
| extra.accepted | 2020-06-25 | — | 2020-06-23 | — | Landscape ('2020-06-25') ≠ CLOMonitor ('2020-06-23'). |

### Backstage (incubating)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/backstage/backstage | https://github.com/backstage | https://github.com/backstage/backstage | **No** | PCC ('https://github.com/backstage') and CLOMonitor ('https://github.com/backstage/backstage') disagree. Landscape ('https://github.com/backstage/backstage') ≠ PCC ('https://github.com/backstage'). |

### Buildpacks (incubating)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/buildpacks/pack | https://github.com/buildpacks | https://github.com/buildpacks/community | **No** | PCC ('https://github.com/buildpacks') and CLOMonitor ('https://github.com/buildpacks/community') disagree. Landscape ('https://github.com/buildpacks/pack') ≠ PCC ('https://github.com/buildpacks'). Landscape ('https://github.com/buildpacks/pack') ≠ CLOMonitor ('https://github.com/buildpacks/community'). |

### Chaos Mesh (incubating)

- **Path:** Observability and Analysis / Chaos Engineering
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | ChaosMesh | chaos-mesh | **No** | PCC slug 'ChaosMesh' vs CLOMonitor name 'chaos-mesh' (normalized identifiers differ). |
| repo_url | https://github.com/chaos-mesh/chaos-mesh | https://github.com/Chaos-Mesh | https://github.com/chaos-mesh/chaos-mesh | **No** | PCC ('https://github.com/Chaos-Mesh') and CLOMonitor ('https://github.com/chaos-mesh/chaos-mesh') disagree. Landscape ('https://github.com/chaos-mesh/chaos-mesh') ≠ PCC ('https://github.com/Chaos-Mesh'). |
| extra.lfx_slug | ChaosMesh | ChaosMesh | chaos-mesh | **No** | PCC ('ChaosMesh') and CLOMonitor ('chaos-mesh') disagree. Landscape ('ChaosMesh') ≠ CLOMonitor ('chaos-mesh'). |

### Cloud Custodian (incubating)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | c7n | cloud-custodian | **No** | PCC slug 'c7n' vs CLOMonitor name 'cloud-custodian' (normalized identifiers differ). |
| repo_url | https://github.com/cloud-custodian/cloud-custodian | https://github.com/cloud-custodian | https://github.com/cloud-custodian/cloud-custodian | **No** | PCC ('https://github.com/cloud-custodian') and CLOMonitor ('https://github.com/cloud-custodian/cloud-custodian') disagree. Landscape ('https://github.com/cloud-custodian/cloud-custodian') ≠ PCC ('https://github.com/cloud-custodian'). |
| extra.lfx_slug | c7n | c7n | cloud-custodian | **No** | PCC ('c7n') and CLOMonitor ('cloud-custodian') disagree. Landscape ('c7n') ≠ CLOMonitor ('cloud-custodian'). |
| extra.accepted | 2020-06-25 | — | 2020-06-23 | — | Landscape ('2020-06-25') ≠ CLOMonitor ('2020-06-23'). |

### Contour (incubating)

- **Path:** Orchestration & Management / Service Proxy
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/projectcontour/contour | https://github.com/projectcontour | https://github.com/projectcontour/contour | **No** | PCC ('https://github.com/projectcontour') and CLOMonitor ('https://github.com/projectcontour/contour') disagree. Landscape ('https://github.com/projectcontour/contour') ≠ PCC ('https://github.com/projectcontour'). |

### Emissary-Ingress (incubating)

- **Path:** Orchestration & Management / API Gateway
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | emissary | emissary-ingress | **No** | PCC slug 'emissary' vs CLOMonitor name 'emissary-ingress' (normalized identifiers differ). |
| repo_url | https://github.com/emissary-ingress/emissary | https://github.com/emissary-ingress/ | https://github.com/emissary-ingress/emissary | **No** | PCC ('https://github.com/emissary-ingress/') and CLOMonitor ('https://github.com/emissary-ingress/emissary') disagree. Landscape ('https://github.com/emissary-ingress/emissary') ≠ PCC ('https://github.com/emissary-ingress/'). |
| extra.lfx_slug | emissary | emissary | emissary-ingress | **No** | PCC ('emissary') and CLOMonitor ('emissary-ingress') disagree. Landscape ('emissary') ≠ CLOMonitor ('emissary-ingress'). |
| extra.accepted | 2021-04-13 | — | 2021-04-14 | — | Landscape ('2021-04-13') ≠ CLOMonitor ('2021-04-14'). |

### Flatcar Container Linux (incubating)

- **Path:** Platform / Certified Kubernetes - Distribution
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/flatcar/Flatcar | https://github.com/flatcar | https://github.com/flatcar/Flatcar | **No** | PCC ('https://github.com/flatcar') and CLOMonitor ('https://github.com/flatcar/Flatcar') disagree. Landscape ('https://github.com/flatcar/Flatcar') ≠ PCC ('https://github.com/flatcar'). |

### Fluid (incubating)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/fluid-cloudnative/fluid | https://github.com/Project-Fluid | https://github.com/fluid-cloudnative/fluid | **No** | PCC ('https://github.com/Project-Fluid') and CLOMonitor ('https://github.com/fluid-cloudnative/fluid') disagree. Landscape ('https://github.com/fluid-cloudnative/fluid') ≠ PCC ('https://github.com/Project-Fluid'). |
| extra.accepted | 2021-04-28 | — | 2021-04-27 | — | Landscape ('2021-04-28') ≠ CLOMonitor ('2021-04-27'). |

### gRPC (incubating)

- **Path:** Orchestration & Management / Remote Procedure Call
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/grpc/grpc | https://github.com/grpc | https://github.com/grpc/grpc | **No** | PCC ('https://github.com/grpc') and CLOMonitor ('https://github.com/grpc/grpc') disagree. Landscape ('https://github.com/grpc/grpc') ≠ PCC ('https://github.com/grpc'). |

### Keycloak (incubating)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/keycloak/keycloak | https://github.com/keycloak | https://github.com/keycloak/keycloak | **No** | PCC ('https://github.com/keycloak') and CLOMonitor ('https://github.com/keycloak/keycloak') disagree. Landscape ('https://github.com/keycloak/keycloak') ≠ PCC ('https://github.com/keycloak'). |
| extra.accepted | 2023-04-10 | — | 2023-04-11 | — | Landscape ('2023-04-10') ≠ CLOMonitor ('2023-04-11'). |

### KServe (incubating)

- **Path:** CNAI / ML Serving
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kserve/kserve | https://github.com/kserve/ | https://github.com/kserve/kserve | **No** | PCC ('https://github.com/kserve/') and CLOMonitor ('https://github.com/kserve/kserve') disagree. Landscape ('https://github.com/kserve/kserve') ≠ PCC ('https://github.com/kserve/'). |
| extra.accepted | 2025-09-29 | — | 2025-09-28 | — | Landscape ('2025-09-29') ≠ CLOMonitor ('2025-09-28'). |

### Kubeflow (incubating)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubeflow/kubeflow | https://github.com/kubeflow | https://github.com/kubeflow/kubeflow | **No** | PCC ('https://github.com/kubeflow') and CLOMonitor ('https://github.com/kubeflow/kubeflow') disagree. Landscape ('https://github.com/kubeflow/kubeflow') ≠ PCC ('https://github.com/kubeflow'). |

### KubeVela (incubating)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubevela/kubevela | https://github.com/kubevela | https://github.com/oam-dev/kubevela | **No** | PCC ('https://github.com/kubevela') and CLOMonitor ('https://github.com/oam-dev/kubevela') disagree. Landscape ('https://github.com/kubevela/kubevela') ≠ PCC ('https://github.com/kubevela'). Landscape ('https://github.com/kubevela/kubevela') ≠ CLOMonitor ('https://github.com/oam-dev/kubevela'). |
| extra.accepted | 2021-06-22 | — | 2021-04-05 | — | Landscape ('2021-06-22') ≠ CLOMonitor ('2021-04-05'). |

### KubeVirt (incubating)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubevirt/kubevirt | https://github.com/kubevirt | https://github.com/kubevirt/kubevirt | **No** | PCC ('https://github.com/kubevirt') and CLOMonitor ('https://github.com/kubevirt/kubevirt') disagree. Landscape ('https://github.com/kubevirt/kubevirt') ≠ PCC ('https://github.com/kubevirt'). |
| extra.accepted | 2019-09-06 | — | 2019-09-09 | — | Landscape ('2019-09-06') ≠ CLOMonitor ('2019-09-09'). |

### Lima (incubating)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2022-09-14 | — | 2022-09-13 | — | Landscape ('2022-09-14') ≠ CLOMonitor ('2022-09-13'). |

### Litmus (incubating)

- **Path:** Observability and Analysis / Chaos Engineering
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | litmuschaos | litmus-chaos | **No** | PCC slug 'litmuschaos' vs CLOMonitor name 'litmus-chaos' (normalized identifiers differ). |
| extra.lfx_slug | litmuschaos | litmuschaos | litmus-chaos | **No** | PCC ('litmuschaos') and CLOMonitor ('litmus-chaos') disagree. Landscape ('litmuschaos') ≠ CLOMonitor ('litmus-chaos'). |
| extra.accepted | 2020-06-25 | — | 2020-06-23 | — | Landscape ('2020-06-25') ≠ CLOMonitor ('2020-06-23'). |

### metal3-io (incubating)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | metal3 | metal3-io | **No** | PCC slug 'metal3' vs CLOMonitor name 'metal3-io' (normalized identifiers differ). |
| repo_url | https://github.com/metal3-io/baremetal-operator | https://github.com/metal3-io | https://github.com/metal3-io/community | **No** | PCC ('https://github.com/metal3-io') and CLOMonitor ('https://github.com/metal3-io/community') disagree. Landscape ('https://github.com/metal3-io/baremetal-operator') ≠ PCC ('https://github.com/metal3-io'). Landscape ('https://github.com/metal3-io/baremetal-operator') ≠ CLOMonitor ('https://github.com/metal3-io/community'). |
| extra.lfx_slug | metal3 | metal3 | metal3-io | **No** | PCC ('metal3') and CLOMonitor ('metal3-io') disagree. Landscape ('metal3') ≠ CLOMonitor ('metal3-io'). |

### NATS (incubating)

- **Path:** App Definition and Development / Streaming & Messaging
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/nats-io/nats-server | https://github.com/nats-io | https://github.com/nats-io/nats-server | **No** | PCC ('https://github.com/nats-io') and CLOMonitor ('https://github.com/nats-io/nats-server') disagree. Landscape ('https://github.com/nats-io/nats-server') ≠ PCC ('https://github.com/nats-io'). |

### Notary Project (incubating)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/notaryproject/notation | https://github.com/theupdateframework/notary | https://github.com/notaryproject/notation | **No** | PCC ('https://github.com/theupdateframework/notary') and CLOMonitor ('https://github.com/notaryproject/notation') disagree. Landscape ('https://github.com/notaryproject/notation') ≠ PCC ('https://github.com/theupdateframework/notary'). |

### OpenCost (incubating)

- **Path:** Observability and Analysis / Continuous Optimization
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/opencost/opencost | https://github.com/kubecost/cost-model | https://github.com/opencost/opencost | **No** | PCC ('https://github.com/kubecost/cost-model') and CLOMonitor ('https://github.com/opencost/opencost') disagree. Landscape ('https://github.com/opencost/opencost') ≠ PCC ('https://github.com/kubecost/cost-model'). |
| extra.dev_stats_url | https://opencost.devstats.cncf.io/ | — | https://opencost.teststats.cncf.io/ | — | Landscape ('https://opencost.devstats.cncf.io/') ≠ CLOMonitor ('https://opencost.teststats.cncf.io/'). |
| extra.accepted | 2022-06-17 | — | 2022-06-14 | — | Landscape ('2022-06-17') ≠ CLOMonitor ('2022-06-14'). |

### OpenFeature (incubating)

- **Path:** Observability and Analysis / Feature Flagging
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/open-feature/spec | https://github.com/open-feature | https://github.com/open-feature/spec | **No** | PCC ('https://github.com/open-feature') and CLOMonitor ('https://github.com/open-feature/spec') disagree. Landscape ('https://github.com/open-feature/spec') ≠ PCC ('https://github.com/open-feature'). |
| extra.dev_stats_url | https://openfeature.devstats.cncf.io/ | — | https://openfeature.teststats.cncf.io/ | — | Landscape ('https://openfeature.devstats.cncf.io/') ≠ CLOMonitor ('https://openfeature.teststats.cncf.io/'). |
| extra.accepted | 2022-06-17 | — | 2022-06-14 | — | Landscape ('2022-06-17') ≠ CLOMonitor ('2022-06-14'). |

### OpenFGA (incubating)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2022-09-14 | — | 2022-09-13 | — | Landscape ('2022-09-14') ≠ CLOMonitor ('2022-09-13'). |

### OpenKruise (incubating)

- **Path:** App Definition and Development / Continuous Integration & Delivery
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | openkruise | open-kruise | **No** | PCC slug 'openkruise' vs CLOMonitor name 'open-kruise' (normalized identifiers differ). |
| extra.lfx_slug | openkruise | openkruise | open-kruise | **No** | PCC ('openkruise') and CLOMonitor ('open-kruise') disagree. Landscape ('openkruise') ≠ CLOMonitor ('open-kruise'). |

### OpenTelemetry (incubating)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | opentelemetry | open-telemetry | **No** | PCC slug 'opentelemetry' vs CLOMonitor name 'open-telemetry' (normalized identifiers differ). |
| repo_url | https://github.com/open-telemetry/community | https://github.com/open-telemetry/opentelemetry.io | https://github.com/open-telemetry/community | **No** | PCC ('https://github.com/open-telemetry/opentelemetry.io') and CLOMonitor ('https://github.com/open-telemetry/community') disagree. Landscape ('https://github.com/open-telemetry/community') ≠ PCC ('https://github.com/open-telemetry/opentelemetry.io'). |
| extra.lfx_slug | opentelemetry | opentelemetry | open-telemetry | **No** | PCC ('opentelemetry') and CLOMonitor ('open-telemetry') disagree. Landscape ('opentelemetry') ≠ CLOMonitor ('open-telemetry'). |

### OpenYurt (incubating)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/openyurtio/openyurt | https://github.com/OpenYurt | https://github.com/openyurtio/openyurt | **No** | PCC ('https://github.com/OpenYurt') and CLOMonitor ('https://github.com/openyurtio/openyurt') disagree. Landscape ('https://github.com/openyurtio/openyurt') ≠ PCC ('https://github.com/OpenYurt'). |

### Operator Framework (incubating)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | operator-sdk | operator-framework | **No** | PCC slug 'operator-sdk' vs CLOMonitor name 'operator-framework' (normalized identifiers differ). |
| extra.lfx_slug | operator-sdk | operator-sdk | operator-framework | **No** | PCC ('operator-sdk') and CLOMonitor ('operator-framework') disagree. Landscape ('operator-sdk') ≠ CLOMonitor ('operator-framework'). |

### Strimzi (incubating)

- **Path:** App Definition and Development / Streaming & Messaging
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/strimzi/strimzi-kafka-operator | https://github.com/strimzi | https://github.com/strimzi/strimzi-kafka-bridge | **No** | PCC ('https://github.com/strimzi') and CLOMonitor ('https://github.com/strimzi/strimzi-kafka-bridge') disagree. Landscape ('https://github.com/strimzi/strimzi-kafka-operator') ≠ PCC ('https://github.com/strimzi'). Landscape ('https://github.com/strimzi/strimzi-kafka-operator') ≠ CLOMonitor ('https://github.com/strimzi/strimzi-kafka-bridge'). |

### Thanos (incubating)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2019-07-14 | — | 2019-07-20 | — | Landscape ('2019-07-14') ≠ CLOMonitor ('2019-07-20'). |

### Volcano (incubating)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/volcano-sh/volcano | https://github.com/volcano-sh/volcano | https://github.com/volcano-sh/community | **No** | PCC ('https://github.com/volcano-sh/volcano') and CLOMonitor ('https://github.com/volcano-sh/community') disagree. Landscape ('https://github.com/volcano-sh/volcano') ≠ CLOMonitor ('https://github.com/volcano-sh/community'). |
| extra.accepted | 2020-04-09 | — | 2020-04-10 | — | Landscape ('2020-04-09') ≠ CLOMonitor ('2020-04-10'). |

### wasmCloud (incubating)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | wasmcloud | wasm-cloud | **No** | PCC slug 'wasmcloud' vs CLOMonitor name 'wasm-cloud' (normalized identifiers differ). |
| repo_url | https://github.com/wasmCloud/wasmCloud | https://github.com/wasmCloud | https://github.com/wasmCloud/wasmCloud | **No** | PCC ('https://github.com/wasmCloud') and CLOMonitor ('https://github.com/wasmCloud/wasmCloud') disagree. Landscape ('https://github.com/wasmCloud/wasmCloud') ≠ PCC ('https://github.com/wasmCloud'). |
| extra.lfx_slug | wasmcloud | wasmcloud | wasm-cloud | **No** | PCC ('wasmcloud') and CLOMonitor ('wasm-cloud') disagree. Landscape ('wasmcloud') ≠ CLOMonitor ('wasm-cloud'). |
| extra.accepted | 2021-07-13 | — | 2021-07-12 | — | Landscape ('2021-07-13') ≠ CLOMonitor ('2021-07-12'). |

### Aeraki Mesh (sandbox)

- **Path:** Orchestration & Management / Service Mesh
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | aerakimesh | aeraki-mesh | **No** | PCC slug 'aerakimesh' vs CLOMonitor name 'aeraki-mesh' (normalized identifiers differ). |
| repo_url | https://github.com/aeraki-mesh/aeraki | https://github.com/aeraki-mesh | https://github.com/aeraki-mesh/aeraki | **No** | PCC ('https://github.com/aeraki-mesh') and CLOMonitor ('https://github.com/aeraki-mesh/aeraki') disagree. Landscape ('https://github.com/aeraki-mesh/aeraki') ≠ PCC ('https://github.com/aeraki-mesh'). |
| extra.lfx_slug | aerakimesh | aerakimesh | aeraki-mesh | **No** | PCC ('aerakimesh') and CLOMonitor ('aeraki-mesh') disagree. Landscape ('aerakimesh') ≠ CLOMonitor ('aeraki-mesh'). |
| extra.accepted | 2022-06-17 | — | 2022-06-14 | — | Landscape ('2022-06-17') ≠ CLOMonitor ('2022-06-14'). |

### Agones (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/agones-dev/agones | https://github.com/agones-dev | https://github.com/agones-dev/agones | **No** | PCC ('https://github.com/agones-dev') and CLOMonitor ('https://github.com/agones-dev/agones') disagree. Landscape ('https://github.com/agones-dev/agones') ≠ PCC ('https://github.com/agones-dev'). |
| extra.accepted | 2025-12-21 | — | 2026-03-12 | — | Landscape ('2025-12-21') ≠ CLOMonitor ('2026-03-12'). |

### Akri (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/project-akri/akri | https://github.com/deislabs/akri | https://github.com/project-akri/akri | **No** | PCC ('https://github.com/deislabs/akri') and CLOMonitor ('https://github.com/project-akri/akri') disagree. Landscape ('https://github.com/project-akri/akri') ≠ PCC ('https://github.com/deislabs/akri'). |

### Antrea (sandbox)

- **Path:** Runtime / Cloud Native Network
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2021-04-28 | — | 2021-04-27 | — | Landscape ('2021-04-28') ≠ CLOMonitor ('2021-04-27'). |

### Armada (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2022-07-25 | — | 2022-07-26 | — | Landscape ('2022-07-25') ≠ CLOMonitor ('2022-07-26'). |

### BFE (sandbox)

- **Path:** Orchestration & Management / Service Proxy
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2020-06-25 | — | 2020-06-23 | — | Landscape ('2020-06-25') ≠ CLOMonitor ('2020-06-23'). |

### bootc (sandbox)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/bootc-dev/bootc | https://github.com/containers/bootc | https://github.com/bootc-dev/bootc | **No** | PCC ('https://github.com/containers/bootc') and CLOMonitor ('https://github.com/bootc-dev/bootc') disagree. Landscape ('https://github.com/bootc-dev/bootc') ≠ PCC ('https://github.com/containers/bootc'). |

### Cadence Workflow (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/cadence-workflow/cadence | https://github.com/cadence-workflow | https://github.com/cadence-workflow/cadence | **No** | PCC ('https://github.com/cadence-workflow') and CLOMonitor ('https://github.com/cadence-workflow/cadence') disagree. Landscape ('https://github.com/cadence-workflow/cadence') ≠ PCC ('https://github.com/cadence-workflow'). |

### Capsule (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/projectcapsule/capsule | https://github.com/projectcapsule | https://github.com/projectcapsule/capsule | **No** | PCC ('https://github.com/projectcapsule') and CLOMonitor ('https://github.com/projectcapsule/capsule') disagree. Landscape ('https://github.com/projectcapsule/capsule') ≠ PCC ('https://github.com/projectcapsule'). |

### Carina (sandbox)

- **Path:** Runtime / Cloud Native Storage
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2022-12-14 | — | 2022-12-13 | — | Landscape ('2022-12-14') ≠ CLOMonitor ('2022-12-13'). |

### Cartography (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/cartography-cncf/cartography | https://github.com/cartography-cncf/cartography | https://github.com/lyft/cartography | **No** | PCC ('https://github.com/cartography-cncf/cartography') and CLOMonitor ('https://github.com/lyft/cartography') disagree. Landscape ('https://github.com/cartography-cncf/cartography') ≠ CLOMonitor ('https://github.com/lyft/cartography'). |

### Carvel (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/carvel-dev/ytt | https://carvel.dev | https://github.com/carvel-dev/carvel | **No** | PCC ('https://carvel.dev') and CLOMonitor ('https://github.com/carvel-dev/carvel') disagree. Landscape ('https://github.com/carvel-dev/ytt') ≠ PCC ('https://carvel.dev'). Landscape ('https://github.com/carvel-dev/ytt') ≠ CLOMonitor ('https://github.com/carvel-dev/carvel'). |
| extra.accepted | 2022-09-14 | — | 2022-09-13 | — | Landscape ('2022-09-14') ≠ CLOMonitor ('2022-09-13'). |

### Chaosblade (sandbox)

- **Path:** Observability and Analysis / Chaos Engineering
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | chaosblade | chaos-blade | **No** | PCC slug 'chaosblade' vs CLOMonitor name 'chaos-blade' (normalized identifiers differ). |
| extra.lfx_slug | chaosblade | chaosblade | chaos-blade | **No** | PCC ('chaosblade') and CLOMonitor ('chaos-blade') disagree. Landscape ('chaosblade') ≠ CLOMonitor ('chaos-blade'). |
| extra.accepted | 2021-04-28 | — | 2021-04-27 | — | Landscape ('2021-04-28') ≠ CLOMonitor ('2021-04-27'). |

### CloudNativePG (sandbox)

- **Path:** App Definition and Development / Database
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | cloudnativepg | cloudnative-pg | **No** | PCC slug 'cloudnativepg' vs CLOMonitor name 'cloudnative-pg' (normalized identifiers differ). |
| repo_url | https://github.com/cloudnative-pg/cloudnative-pg | https://github.com/cloudnative-pg | https://github.com/cloudnative-pg/cloudnative-pg | **No** | PCC ('https://github.com/cloudnative-pg') and CLOMonitor ('https://github.com/cloudnative-pg/cloudnative-pg') disagree. Landscape ('https://github.com/cloudnative-pg/cloudnative-pg') ≠ PCC ('https://github.com/cloudnative-pg'). |
| extra.lfx_slug | cloudnativepg | cloudnativepg | cloudnative-pg | **No** | PCC ('cloudnativepg') and CLOMonitor ('cloudnative-pg') disagree. Landscape ('cloudnativepg') ≠ CLOMonitor ('cloudnative-pg'). |

### Clusterpedia (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2022-06-17 | — | 2022-06-14 | — | Landscape ('2022-06-17') ≠ CLOMonitor ('2022-06-14'). |

### CoHDI (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/CoHDI | https://github.com/CoHDI | https://github.com/CoHDI/composable-resource-operator | **No** | PCC ('https://github.com/CoHDI') and CLOMonitor ('https://github.com/CoHDI/composable-resource-operator') disagree. Landscape ('https://github.com/CoHDI') ≠ CLOMonitor ('https://github.com/CoHDI/composable-resource-operator'). |

### composefs (sandbox)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/containers/composefs | https://github.com/containers/composefs | https://github.com/composefs/composefs | **No** | PCC ('https://github.com/containers/composefs') and CLOMonitor ('https://github.com/composefs/composefs') disagree. Landscape ('https://github.com/containers/composefs') ≠ CLOMonitor ('https://github.com/composefs/composefs'). |

### Confidential Containers (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | confcont | confidential-containers | **No** | PCC slug 'confcont' vs CLOMonitor name 'confidential-containers' (normalized identifiers differ). |
| repo_url | https://github.com/confidential-containers/confidential-c… | https://github.com/confidential-containers | https://github.com/confidential-containers/documentation | **No** | PCC ('https://github.com/confidential-containers') and CLOMonitor ('https://github.com/confidential-containers/documentation') disagree. Landscape ('https://github.com/confidential-containers/confidential-containers') ≠ PCC ('https://github.com/confidential-containers'). Landscape ('https://github.com/confidential-containers/confidential-containers') ≠ CLOMonitor ('https://github.com/confidential-containers/documentation'). |
| extra.lfx_slug | confcont | confcont | confidential-containers | **No** | PCC ('confcont') and CLOMonitor ('confidential-containers') disagree. Landscape ('confcont') ≠ CLOMonitor ('confidential-containers'). |

### Connect RPC (sandbox)

- **Path:** Orchestration & Management / Remote Procedure Call
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | connect | connect-rpc | **No** | PCC slug 'connect' vs CLOMonitor name 'connect-rpc' (normalized identifiers differ). |
| repo_url | https://github.com/connectrpc/connect-go | https://github.com/connectrpc | https://github.com/connectrpc/connect-go | **No** | PCC ('https://github.com/connectrpc') and CLOMonitor ('https://github.com/connectrpc/connect-go') disagree. Landscape ('https://github.com/connectrpc/connect-go') ≠ PCC ('https://github.com/connectrpc'). |
| extra.lfx_slug | connect | connect | connect-rpc | **No** | PCC ('connect') and CLOMonitor ('connect-rpc') disagree. Landscape ('connect') ≠ CLOMonitor ('connect-rpc'). |

### container2wasm (sandbox)

- **Path:** Wasm / Orchestration & Management
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/container2wasm/container2wasm | https://github.com/ktock/container2wasm | https://github.com/container2wasm/container2wasm | **No** | PCC ('https://github.com/ktock/container2wasm') and CLOMonitor ('https://github.com/container2wasm/container2wasm') disagree. Landscape ('https://github.com/container2wasm/container2wasm') ≠ PCC ('https://github.com/ktock/container2wasm'). |

### ContainerSSH (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/containerssh/containerssh | https://github.com/containerssh | https://github.com/ContainerSSH/ContainerSSH | **No** | PCC ('https://github.com/containerssh') and CLOMonitor ('https://github.com/ContainerSSH/ContainerSSH') disagree. Landscape ('https://github.com/containerssh/containerssh') ≠ PCC ('https://github.com/containerssh'). |
| extra.accepted | 2022-09-14 | — | 2022-09-13 | — | Landscape ('2022-09-14') ≠ CLOMonitor ('2022-09-13'). |

### Copa (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2023-09-19 | — | 2023-12-19 | — | Landscape ('2023-09-19') ≠ CLOMonitor ('2023-12-19'). |

### Cozystack (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/cozystack/cozystack | https://github.com/aenix-io/cozystack/ | https://github.com/cozystack/cozystack | **No** | PCC ('https://github.com/aenix-io/cozystack/') and CLOMonitor ('https://github.com/cozystack/cozystack') disagree. Landscape ('https://github.com/cozystack/cozystack') ≠ PCC ('https://github.com/aenix-io/cozystack/'). |

### Cozystack (sandbox)

- **Path:** Platform / PaaS/Container Service
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/cozystack/cozystack | https://github.com/aenix-io/cozystack/ | https://github.com/cozystack/cozystack | **No** | PCC ('https://github.com/aenix-io/cozystack/') and CLOMonitor ('https://github.com/cozystack/cozystack') disagree. Landscape ('https://github.com/cozystack/cozystack') ≠ PCC ('https://github.com/aenix-io/cozystack/'). |

### Dalec (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/project-dalec/dalec | https://github.com/project-dalec | https://github.com/project-dalec/dalec | **No** | PCC ('https://github.com/project-dalec') and CLOMonitor ('https://github.com/project-dalec/dalec') disagree. Landscape ('https://github.com/project-dalec/dalec') ≠ PCC ('https://github.com/project-dalec'). |

### Devfile (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/devfile/api | https://github.com/devfile/api | https://github.com/devfile/registry | **No** | PCC ('https://github.com/devfile/api') and CLOMonitor ('https://github.com/devfile/registry') disagree. Landscape ('https://github.com/devfile/api') ≠ CLOMonitor ('https://github.com/devfile/registry'). |
| extra.accepted | 2022-01-11 | — | 2021-01-11 | — | Landscape ('2022-01-11') ≠ CLOMonitor ('2021-01-11'). |

### DevSpace (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/devspace-sh/devspace | https://github.com/loft-sh/devspace | https://github.com/loft-sh/devspace | Yes | Landscape ('https://github.com/devspace-sh/devspace') ≠ PCC ('https://github.com/loft-sh/devspace'). Landscape ('https://github.com/devspace-sh/devspace') ≠ CLOMonitor ('https://github.com/loft-sh/devspace'). |

### Dex (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2020-06-25 | — | 2020-06-23 | — | Landscape ('2020-06-25') ≠ CLOMonitor ('2020-06-23'). |

### Distribution (sandbox)

- **Path:** Provisioning / Container Registry
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | cncf-distribution | distribution | **No** | PCC slug 'cncf-distribution' vs CLOMonitor name 'distribution' (normalized identifiers differ). |
| extra.lfx_slug | cncf-distribution | cncf-distribution | distribution | **No** | PCC ('cncf-distribution') and CLOMonitor ('distribution') disagree. Landscape ('cncf-distribution') ≠ CLOMonitor ('distribution'). |

### Drasi (sandbox)

- **Path:** App Definition and Development / Streaming & Messaging
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | http://github.com/drasi-project/drasi-platform | https://github.com/drasi-project | https://github.com/drasi-project/drasi-platform | **No** | PCC ('https://github.com/drasi-project') and CLOMonitor ('https://github.com/drasi-project/drasi-platform') disagree. Landscape ('http://github.com/drasi-project/drasi-platform') ≠ PCC ('https://github.com/drasi-project'). Landscape ('http://github.com/drasi-project/drasi-platform') ≠ CLOMonitor ('https://github.com/drasi-project/drasi-platform'). |
| extra.accepted | 2025-01-21 | — | 2025-01-24 | — | Landscape ('2025-01-21') ≠ CLOMonitor ('2025-01-24'). |

### Easegress (sandbox)

- **Path:** Orchestration & Management / API Gateway
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/easegress-io/easegress | https://github.com/megaease/easegress | https://github.com/megaease/easegress | Yes | Landscape ('https://github.com/easegress-io/easegress') ≠ PCC ('https://github.com/megaease/easegress'). Landscape ('https://github.com/easegress-io/easegress') ≠ CLOMonitor ('https://github.com/megaease/easegress'). |

### Eraser (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/eraser-dev/eraser | https://github.com/eraser-dev/eraser | https://github.com/Azure/eraser | **No** | PCC ('https://github.com/eraser-dev/eraser') and CLOMonitor ('https://github.com/Azure/eraser') disagree. Landscape ('https://github.com/eraser-dev/eraser') ≠ CLOMonitor ('https://github.com/Azure/eraser'). |
| extra.accepted | 2023-06-30 | — | 2023-06-21 | — | Landscape ('2023-06-30') ≠ CLOMonitor ('2023-06-21'). |

### external-secrets (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | externalsecretsoperator | external-secrets | **No** | PCC slug 'externalsecretsoperator' vs CLOMonitor name 'external-secrets' (normalized identifiers differ). |
| extra.lfx_slug | externalsecretsoperator | externalsecretsoperator | external-secrets | **No** | PCC ('externalsecretsoperator') and CLOMonitor ('external-secrets') disagree. Landscape ('externalsecretsoperator') ≠ CLOMonitor ('external-secrets'). |
| extra.dev_stats_url | https://externalsecretsoperator.devstats.cncf.io/ | — | https://external-secrets.devstats.cncf.io/ | — | Landscape ('https://externalsecretsoperator.devstats.cncf.io/') ≠ CLOMonitor ('https://external-secrets.devstats.cncf.io/'). |

### Headlamp (sandbox)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubernetes-sigs/headlamp | https://github.com/kubernetes-sigs/headlamp | https://github.com/headlamp-k8s/headlamp | **No** | PCC ('https://github.com/kubernetes-sigs/headlamp') and CLOMonitor ('https://github.com/headlamp-k8s/headlamp') disagree. Landscape ('https://github.com/kubernetes-sigs/headlamp') ≠ CLOMonitor ('https://github.com/headlamp-k8s/headlamp'). |

### Hexa (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | hexa | hexapolicyorchestrator | **No** | PCC slug 'hexa' vs CLOMonitor name 'hexapolicyorchestrator' (normalized identifiers differ). |
| repo_url | https://github.com/hexa-org/policy-orchestrator | https://github.com/hexa-org | https://github.com/hexa-org/policy-orchestrator | **No** | PCC ('https://github.com/hexa-org') and CLOMonitor ('https://github.com/hexa-org/policy-orchestrator') disagree. Landscape ('https://github.com/hexa-org/policy-orchestrator') ≠ PCC ('https://github.com/hexa-org'). |
| extra.lfx_slug | hexa | hexa | hexapolicyorchestrator | **No** | PCC ('hexa') and CLOMonitor ('hexapolicyorchestrator') disagree. Landscape ('hexa') ≠ CLOMonitor ('hexapolicyorchestrator'). |

### HolmesGPT (sandbox)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/HolmesGPT/holmesgpt | https://github.com/holmesgpt/ | https://github.com/robusta-dev/holmesgpt | **No** | PCC ('https://github.com/holmesgpt/') and CLOMonitor ('https://github.com/robusta-dev/holmesgpt') disagree. Landscape ('https://github.com/HolmesGPT/holmesgpt') ≠ PCC ('https://github.com/holmesgpt/'). Landscape ('https://github.com/HolmesGPT/holmesgpt') ≠ CLOMonitor ('https://github.com/robusta-dev/holmesgpt'). |
| extra.accepted | 2025-10-08 | — | 2025-10-10 | — | Landscape ('2025-10-08') ≠ CLOMonitor ('2025-10-10'). |

### HwameiStor (sandbox)

- **Path:** Runtime / Cloud Native Storage
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2023-06-22 | — | 2023-06-21 | — | Landscape ('2023-06-22') ≠ CLOMonitor ('2023-06-21'). |

### Hyperlight (sandbox)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/hyperlight-dev/hyperlight | https://github.com/hyperlight-dev/ | https://github.com/hyperlight-dev/hyperlight | **No** | PCC ('https://github.com/hyperlight-dev/') and CLOMonitor ('https://github.com/hyperlight-dev/hyperlight') disagree. Landscape ('https://github.com/hyperlight-dev/hyperlight') ≠ PCC ('https://github.com/hyperlight-dev/'). |

### Inclavare Containers (sandbox)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | inclavarecontainers | inclavare | **No** | PCC slug 'inclavarecontainers' vs CLOMonitor name 'inclavare' (normalized identifiers differ). |
| repo_url | https://github.com/inclavare-containers/inclavare-containers | https://github.com/inclavare-containers/inclavare-containers | https://github.com/alibaba/inclavare-containers | **No** | PCC ('https://github.com/inclavare-containers/inclavare-containers') and CLOMonitor ('https://github.com/alibaba/inclavare-containers') disagree. Landscape ('https://github.com/inclavare-containers/inclavare-containers') ≠ CLOMonitor ('https://github.com/alibaba/inclavare-containers'). |
| extra.lfx_slug | inclavarecontainers | inclavarecontainers | inclavare | **No** | PCC ('inclavarecontainers') and CLOMonitor ('inclavare') disagree. Landscape ('inclavarecontainers') ≠ CLOMonitor ('inclavare'). |

### Inspektor Gadget (sandbox)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | inspektorgadget | inspektor-gadget | **No** | PCC slug 'inspektorgadget' vs CLOMonitor name 'inspektor-gadget' (normalized identifiers differ). |
| repo_url | https://github.com/inspektor-gadget/inspektor-gadget | https://github.com/inspektor-gadget | https://github.com/inspektor-gadget/inspektor-gadget | **No** | PCC ('https://github.com/inspektor-gadget') and CLOMonitor ('https://github.com/inspektor-gadget/inspektor-gadget') disagree. Landscape ('https://github.com/inspektor-gadget/inspektor-gadget') ≠ PCC ('https://github.com/inspektor-gadget'). |
| extra.lfx_slug | inspektorgadget | inspektorgadget | inspektor-gadget | **No** | PCC ('inspektorgadget') and CLOMonitor ('inspektor-gadget') disagree. Landscape ('inspektorgadget') ≠ CLOMonitor ('inspektor-gadget'). |

### k0s (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/k0sproject/k0s | https://github.com/k0sproject | https://github.com/k0sproject/k0s | **No** | PCC ('https://github.com/k0sproject') and CLOMonitor ('https://github.com/k0sproject/k0s') disagree. Landscape ('https://github.com/k0sproject/k0s') ≠ PCC ('https://github.com/k0sproject'). |
| extra.accepted | 2025-01-19 | — | 2025-01-21 | — | Landscape ('2025-01-19') ≠ CLOMonitor ('2025-01-21'). |

### k8gb (sandbox)

- **Path:** Orchestration & Management / Coordination & Service Discovery
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/k8gb-io/k8gb | https://github.com/k8gb-io | https://github.com/k8gb-io/k8gb | **No** | PCC ('https://github.com/k8gb-io') and CLOMonitor ('https://github.com/k8gb-io/k8gb') disagree. Landscape ('https://github.com/k8gb-io/k8gb') ≠ PCC ('https://github.com/k8gb-io'). |

### K8sGPT (sandbox)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/k8sgpt-ai/k8sgpt | https://github.com/k8sgpt-ai | https://github.com/k8sgpt-ai/k8sgpt | **No** | PCC ('https://github.com/k8sgpt-ai') and CLOMonitor ('https://github.com/k8sgpt-ai/k8sgpt') disagree. Landscape ('https://github.com/k8sgpt-ai/k8sgpt') ≠ PCC ('https://github.com/k8sgpt-ai'). |

### kagent (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kagent-dev/kagent | https://github.com/kagent-dev/ | https://github.com/kagent-dev/kagent | **No** | PCC ('https://github.com/kagent-dev/') and CLOMonitor ('https://github.com/kagent-dev/kagent') disagree. Landscape ('https://github.com/kagent-dev/kagent') ≠ PCC ('https://github.com/kagent-dev/'). |

### KAI Scheduler (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kai-scheduler/KAI-Scheduler | https://github.com/kai-scheduler/ | https://github.com/NVIDIA/KAI-Scheduler | **No** | PCC ('https://github.com/kai-scheduler/') and CLOMonitor ('https://github.com/NVIDIA/KAI-Scheduler') disagree. Landscape ('https://github.com/kai-scheduler/KAI-Scheduler') ≠ PCC ('https://github.com/kai-scheduler/'). Landscape ('https://github.com/kai-scheduler/KAI-Scheduler') ≠ CLOMonitor ('https://github.com/NVIDIA/KAI-Scheduler'). |
| extra.accepted | 2025-12-21 | — | 2026-02-08 | — | Landscape ('2025-12-21') ≠ CLOMonitor ('2026-02-08'). |

### Kairos (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kairos-io/kairos | https://github.com/kairos-io | https://github.com/kairos-io/kairos | **No** | PCC ('https://github.com/kairos-io') and CLOMonitor ('https://github.com/kairos-io/kairos') disagree. Landscape ('https://github.com/kairos-io/kairos') ≠ PCC ('https://github.com/kairos-io'). |

### KAITO (sandbox)

- **Path:** CNAI / ML Serving
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kaito-project/kaito | https://github.com/Azure/kaito | https://github.com/Azure/kaito | Yes | Landscape ('https://github.com/kaito-project/kaito') ≠ PCC ('https://github.com/Azure/kaito'). Landscape ('https://github.com/kaito-project/kaito') ≠ CLOMonitor ('https://github.com/Azure/kaito'). |
| extra.accepted | 2024-10-17 | — | 2024-10-11 | — | Landscape ('2024-10-17') ≠ CLOMonitor ('2024-10-11'). |

### Keylime (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/keylime/keylime | https://github.com/keylime | https://github.com/keylime/keylime | **No** | PCC ('https://github.com/keylime') and CLOMonitor ('https://github.com/keylime/keylime') disagree. Landscape ('https://github.com/keylime/keylime') ≠ PCC ('https://github.com/keylime'). |

### Kgateway (sandbox)

- **Path:** Orchestration & Management / API Gateway
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kgateway-dev/kgateway | https://github.com/kgateway-dev | https://github.com/kgateway-dev/kgateway | **No** | PCC ('https://github.com/kgateway-dev') and CLOMonitor ('https://github.com/kgateway-dev/kgateway') disagree. Landscape ('https://github.com/kgateway-dev/kgateway') ≠ PCC ('https://github.com/kgateway-dev'). |

### KitOps (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kitops-ml/kitops | https://github.com/jozu-ai/kitops | https://github.com/jozu-ai/kitops | Yes | Landscape ('https://github.com/kitops-ml/kitops') ≠ PCC ('https://github.com/jozu-ai/kitops'). Landscape ('https://github.com/kitops-ml/kitops') ≠ CLOMonitor ('https://github.com/jozu-ai/kitops'). |

### ko (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2022-12-14 | — | 2022-12-13 | — | Landscape ('2022-12-14') ≠ CLOMonitor ('2022-12-13'). |

### Konveyor (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/konveyor/operator | https://github.com/konveyor | https://github.com/konveyor/community | **No** | PCC ('https://github.com/konveyor') and CLOMonitor ('https://github.com/konveyor/community') disagree. Landscape ('https://github.com/konveyor/operator') ≠ PCC ('https://github.com/konveyor'). Landscape ('https://github.com/konveyor/operator') ≠ CLOMonitor ('https://github.com/konveyor/community'). |

### Koordinator (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/koordinator-sh/koordinator | https://github.com/koordinator-sh | https://github.com/koordinator-sh/koordinator | **No** | PCC ('https://github.com/koordinator-sh') and CLOMonitor ('https://github.com/koordinator-sh/koordinator') disagree. Landscape ('https://github.com/koordinator-sh/koordinator') ≠ PCC ('https://github.com/koordinator-sh'). |

### kpt (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kptdev/kpt | https://github.com/kptdev | https://github.com/GoogleContainerTools/kpt | **No** | PCC ('https://github.com/kptdev') and CLOMonitor ('https://github.com/GoogleContainerTools/kpt') disagree. Landscape ('https://github.com/kptdev/kpt') ≠ PCC ('https://github.com/kptdev'). Landscape ('https://github.com/kptdev/kpt') ≠ CLOMonitor ('https://github.com/GoogleContainerTools/kpt'). |
| extra.accepted | 2023-06-30 | — | 2023-06-21 | — | Landscape ('2023-06-30') ≠ CLOMonitor ('2023-06-21'). |

### Kuadrant (sandbox)

- **Path:** Orchestration & Management / API Gateway
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kuadrant/kuadrant-operator | https://github.com/Kuadrant | https://github.com/kuadrant/kuadrant-operator | **No** | PCC ('https://github.com/Kuadrant') and CLOMonitor ('https://github.com/kuadrant/kuadrant-operator') disagree. Landscape ('https://github.com/kuadrant/kuadrant-operator') ≠ PCC ('https://github.com/Kuadrant'). |

### Kube-OVN (sandbox)

- **Path:** Runtime / Cloud Native Network
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubeovn/kube-ovn | https://github.com/alauda/kube-ovn | https://github.com/kubeovn/kube-ovn | **No** | PCC ('https://github.com/alauda/kube-ovn') and CLOMonitor ('https://github.com/kubeovn/kube-ovn') disagree. Landscape ('https://github.com/kubeovn/kube-ovn') ≠ PCC ('https://github.com/alauda/kube-ovn'). |

### kube-rs (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kube-rs/kube | https://github.com/kube-rs/kube-rs | https://github.com/kube-rs/kube-rs | Yes | Landscape ('https://github.com/kube-rs/kube') ≠ PCC ('https://github.com/kube-rs/kube-rs'). Landscape ('https://github.com/kube-rs/kube') ≠ CLOMonitor ('https://github.com/kube-rs/kube-rs'). |

### KubeClipper (sandbox)

- **Path:** Platform / Certified Kubernetes - Installer
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubeclipper/kubeclipper | https://github.com/Kubeclipper | https://github.com/kubeclipper/kubeclipper | **No** | PCC ('https://github.com/Kubeclipper') and CLOMonitor ('https://github.com/kubeclipper/kubeclipper') disagree. Landscape ('https://github.com/kubeclipper/kubeclipper') ≠ PCC ('https://github.com/Kubeclipper'). |
| extra.accepted | 2023-06-30 | — | 2023-06-29 | — | Landscape ('2023-06-30') ≠ CLOMonitor ('2023-06-29'). |

### KubeElasti (sandbox)

- **Path:** Serverless / Framework
- **Matched:** PCC=False, CLOMonitor=True (clomonitor_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2026-01-03 | — | 2026-01-30 | — | Landscape ('2026-01-03') ≠ CLOMonitor ('2026-01-30'). |

### KubeFleet (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubefleet-dev/kubefleet | https://github.com/kubefleet-dev/ | https://github.com/Azure/fleet | **No** | PCC ('https://github.com/kubefleet-dev/') and CLOMonitor ('https://github.com/Azure/fleet') disagree. Landscape ('https://github.com/kubefleet-dev/kubefleet') ≠ PCC ('https://github.com/kubefleet-dev/'). Landscape ('https://github.com/kubefleet-dev/kubefleet') ≠ CLOMonitor ('https://github.com/Azure/fleet'). |

### Kubewarden (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubewarden/kubewarden-controller | https://github.com/kubewarden | https://github.com/kubewarden/community | **No** | PCC ('https://github.com/kubewarden') and CLOMonitor ('https://github.com/kubewarden/community') disagree. Landscape ('https://github.com/kubewarden/kubewarden-controller') ≠ PCC ('https://github.com/kubewarden'). Landscape ('https://github.com/kubewarden/kubewarden-controller') ≠ CLOMonitor ('https://github.com/kubewarden/community'). |
| extra.dev_stats_url | https://kubewarden.devstats.cncf.io/ | — | https://kubewarden.teststats.cncf.io/ | — | Landscape ('https://kubewarden.devstats.cncf.io/') ≠ CLOMonitor ('https://kubewarden.teststats.cncf.io/'). |
| extra.accepted | 2022-06-17 | — | 2022-06-14 | — | Landscape ('2022-06-17') ≠ CLOMonitor ('2022-06-14'). |

### KUDO (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2020-06-25 | — | 2020-06-23 | — | Landscape ('2020-06-25') ≠ CLOMonitor ('2020-06-23'). |

### Kuma (sandbox)

- **Path:** Orchestration & Management / Service Mesh
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2020-06-25 | — | 2020-06-23 | — | Landscape ('2020-06-25') ≠ CLOMonitor ('2020-06-23'). |

### Kured (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/kubereboot/kured | https://github.com/weaveworks/kured | https://github.com/kubereboot/kured | **No** | PCC ('https://github.com/weaveworks/kured') and CLOMonitor ('https://github.com/kubereboot/kured') disagree. Landscape ('https://github.com/kubereboot/kured') ≠ PCC ('https://github.com/weaveworks/kured'). |
| extra.accepted | 2022-09-14 | — | 2022-09-13 | — | Landscape ('2022-09-14') ≠ CLOMonitor ('2022-09-13'). |

### KusionStack (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/KusionStack/kusion | https://github.com/KusionStack | https://github.com/KusionStack/kusion | **No** | PCC ('https://github.com/KusionStack') and CLOMonitor ('https://github.com/KusionStack/kusion') disagree. Landscape ('https://github.com/KusionStack/kusion') ≠ PCC ('https://github.com/KusionStack'). |
| extra.accepted | 2024-09-12 | — | 2024-10-17 | — | Landscape ('2024-09-12') ≠ CLOMonitor ('2024-10-17'). |

### Logging Operator (Kube Logging) (sandbox)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | logging-operator | kube-logging | **No** | PCC slug 'logging-operator' vs CLOMonitor name 'kube-logging' (normalized identifiers differ). |
| repo_url | https://github.com/kube-logging/logging-operator | https://github.com/kube-logging | https://github.com/kube-logging/logging-operator | **No** | PCC ('https://github.com/kube-logging') and CLOMonitor ('https://github.com/kube-logging/logging-operator') disagree. Landscape ('https://github.com/kube-logging/logging-operator') ≠ PCC ('https://github.com/kube-logging'). |
| extra.lfx_slug | logging-operator | logging-operator | kube-logging | **No** | PCC ('logging-operator') and CLOMonitor ('kube-logging') disagree. Landscape ('logging-operator') ≠ CLOMonitor ('kube-logging'). |

### Meshery (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2021-06-22 | — | 2021-06-21 | — | Landscape ('2021-06-22') ≠ CLOMonitor ('2021-06-21'). |

### Microcks (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/microcks/microcks | https://github.com/meshery/meshery | https://github.com/microcks/microcks | **No** | PCC ('https://github.com/meshery/meshery') and CLOMonitor ('https://github.com/microcks/microcks') disagree. Landscape ('https://github.com/microcks/microcks') ≠ PCC ('https://github.com/meshery/meshery'). |

### ModelPack (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/modelpack/model-spec | https://github.com/CloudNativeAI/model-spec | https://github.com/modelpack/model-spec | **No** | PCC ('https://github.com/CloudNativeAI/model-spec') and CLOMonitor ('https://github.com/modelpack/model-spec') disagree. Landscape ('https://github.com/modelpack/model-spec') ≠ PCC ('https://github.com/CloudNativeAI/model-spec'). |
| extra.accepted | 2025-05-13 | — | 2025-06-03 | — | Landscape ('2025-05-13') ≠ CLOMonitor ('2025-06-03'). |

### Network Service Mesh (sandbox)

- **Path:** Runtime / Cloud Native Network
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | nsm | network-service-mesh | **No** | PCC slug 'nsm' vs CLOMonitor name 'network-service-mesh' (normalized identifiers differ). |
| repo_url | https://github.com/networkservicemesh/api | https://github.com/networkservicemesh | https://github.com/networkservicemesh/site | **No** | PCC ('https://github.com/networkservicemesh') and CLOMonitor ('https://github.com/networkservicemesh/site') disagree. Landscape ('https://github.com/networkservicemesh/api') ≠ PCC ('https://github.com/networkservicemesh'). Landscape ('https://github.com/networkservicemesh/api') ≠ CLOMonitor ('https://github.com/networkservicemesh/site'). |
| extra.lfx_slug | nsm | nsm | network-service-mesh | **No** | PCC ('nsm') and CLOMonitor ('network-service-mesh') disagree. Landscape ('nsm') ≠ CLOMonitor ('network-service-mesh'). |

### NMstate (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=False, CLOMonitor=True (clomonitor_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2026-03-12 | — | 2026-03-23 | — | Landscape ('2026-03-12') ≠ CLOMonitor ('2026-03-23'). |

### OAuth2 Proxy (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/oauth2-proxy/oauth2-proxy | https://github.com/oauth2-proxy | https://github.com/oauth2-proxy/oauth2-proxy | **No** | PCC ('https://github.com/oauth2-proxy') and CLOMonitor ('https://github.com/oauth2-proxy/oauth2-proxy') disagree. Landscape ('https://github.com/oauth2-proxy/oauth2-proxy') ≠ PCC ('https://github.com/oauth2-proxy'). |

### Open Cluster Management (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | openclustermanagement | ocm | **No** | PCC slug 'openclustermanagement' vs CLOMonitor name 'ocm' (normalized identifiers differ). |
| repo_url | https://github.com/open-cluster-management-io/ocm | https://github.com/open-cluster-management-io | https://github.com/open-cluster-management-io/clusteradm | **No** | PCC ('https://github.com/open-cluster-management-io') and CLOMonitor ('https://github.com/open-cluster-management-io/clusteradm') disagree. Landscape ('https://github.com/open-cluster-management-io/ocm') ≠ PCC ('https://github.com/open-cluster-management-io'). Landscape ('https://github.com/open-cluster-management-io/ocm') ≠ CLOMonitor ('https://github.com/open-cluster-management-io/clusteradm'). |
| extra.lfx_slug | openclustermanagement | openclustermanagement | ocm | **No** | PCC ('openclustermanagement') and CLOMonitor ('ocm') disagree. Landscape ('openclustermanagement') ≠ CLOMonitor ('ocm'). |

### OpenChoreo (sandbox)

- **Path:** App Definition and Development / Continuous Integration & Delivery
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/openchoreo/openchoreo | https://github.com/openchoreo | https://github.com/openchoreo/openchoreo | **No** | PCC ('https://github.com/openchoreo') and CLOMonitor ('https://github.com/openchoreo/openchoreo') disagree. Landscape ('https://github.com/openchoreo/openchoreo') ≠ PCC ('https://github.com/openchoreo'). |

### OpenEBS (sandbox)

- **Path:** Runtime / Cloud Native Storage
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/openebs/openebs | https://github.com/openebs | https://github.com/openebs/openebs | **No** | PCC ('https://github.com/openebs') and CLOMonitor ('https://github.com/openebs/openebs') disagree. Landscape ('https://github.com/openebs/openebs') ≠ PCC ('https://github.com/openebs'). |

### OpenEverest (sandbox)

- **Path:** App Definition and Development / Database
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/openeverest/openeverest | https://github.com/openeverest/ | https://github.com/openeverest/openeverest | **No** | PCC ('https://github.com/openeverest/') and CLOMonitor ('https://github.com/openeverest/openeverest') disagree. Landscape ('https://github.com/openeverest/openeverest') ≠ PCC ('https://github.com/openeverest/'). |
| extra.accepted | 2026-03-15 | — | 2026-03-19 | — | Landscape ('2026-03-15') ≠ CLOMonitor ('2026-03-19'). |

### OpenFunction (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/OpenFunction/OpenFunction | https://github.com/OpenFunction | https://github.com/OpenFunction/OpenFunction | **No** | PCC ('https://github.com/OpenFunction') and CLOMonitor ('https://github.com/OpenFunction/OpenFunction') disagree. Landscape ('https://github.com/OpenFunction/OpenFunction') ≠ PCC ('https://github.com/OpenFunction'). |
| extra.accepted | 2022-04-26 | — | 2021-11-09 | — | Landscape ('2022-04-26') ≠ CLOMonitor ('2021-11-09'). |

### openGemini (sandbox)

- **Path:** App Definition and Development / Database
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/openGemini/openGemini | https://github.com/openGemini | https://github.com/openGemini/openGemini | **No** | PCC ('https://github.com/openGemini') and CLOMonitor ('https://github.com/openGemini/openGemini') disagree. Landscape ('https://github.com/openGemini/openGemini') ≠ PCC ('https://github.com/openGemini'). |

### OpenGitOps (sandbox)

- **Path:** App Definition and Development / Continuous Integration & Delivery
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | gitops-wg | open-gitops | **No** | PCC slug 'gitops-wg' vs CLOMonitor name 'open-gitops' (normalized identifiers differ). |
| repo_url | https://github.com/open-gitops/project | https://github.com/open-gitops | https://github.com/open-gitops/project | **No** | PCC ('https://github.com/open-gitops') and CLOMonitor ('https://github.com/open-gitops/project') disagree. Landscape ('https://github.com/open-gitops/project') ≠ PCC ('https://github.com/open-gitops'). |
| extra.lfx_slug | gitops-wg | gitops-wg | open-gitops | **No** | PCC ('gitops-wg') and CLOMonitor ('open-gitops') disagree. Landscape ('gitops-wg') ≠ CLOMonitor ('open-gitops'). |

### OpenTofu (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | opentf | opentofu | **No** | PCC slug 'opentf' vs CLOMonitor name 'opentofu' (normalized identifiers differ). |
| extra.lfx_slug | opentf | opentf | opentofu | **No** | PCC ('opentf') and CLOMonitor ('opentofu') disagree. Landscape ('opentf') ≠ CLOMonitor ('opentofu'). |

### ORAS (sandbox)

- **Path:** Runtime / Cloud Native Storage
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/oras-project/oras | https://github.com/oras-project/ | https://github.com/oras-project/community | **No** | PCC ('https://github.com/oras-project/') and CLOMonitor ('https://github.com/oras-project/community') disagree. Landscape ('https://github.com/oras-project/oras') ≠ PCC ('https://github.com/oras-project/'). Landscape ('https://github.com/oras-project/oras') ≠ CLOMonitor ('https://github.com/oras-project/community'). |
| extra.accepted | 2021-07-13 | — | 2021-06-02 | — | Landscape ('2021-07-13') ≠ CLOMonitor ('2021-06-02'). |

### OSCAL-COMPASS (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | trestlegrc | oscal-compass | **No** | PCC slug 'trestlegrc' vs CLOMonitor name 'oscal-compass' (normalized identifiers differ). |
| repo_url | https://github.com/oscal-compass/compliance-trestle | https://github.com/oscal-compass | https://github.com/oscal-compass/compliance-trestle | **No** | PCC ('https://github.com/oscal-compass') and CLOMonitor ('https://github.com/oscal-compass/compliance-trestle') disagree. Landscape ('https://github.com/oscal-compass/compliance-trestle') ≠ PCC ('https://github.com/oscal-compass'). |
| extra.lfx_slug | trestlegrc | trestlegrc | oscal-compass | **No** | PCC ('trestlegrc') and CLOMonitor ('oscal-compass') disagree. Landscape ('trestlegrc') ≠ CLOMonitor ('oscal-compass'). |
| extra.accepted | 2024-06-21 | — | 2024-07-09 | — | Landscape ('2024-06-21') ≠ CLOMonitor ('2024-07-09'). |

### OVN-Kubernetes (sandbox)

- **Path:** Runtime / Cloud Native Network
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/ovn-kubernetes/ovn-kubernetes | https://github.com/ovn-org/ovn-kubernetes | https://github.com/ovn-kubernetes/ovn-kubernetes | **No** | PCC ('https://github.com/ovn-org/ovn-kubernetes') and CLOMonitor ('https://github.com/ovn-kubernetes/ovn-kubernetes') disagree. Landscape ('https://github.com/ovn-kubernetes/ovn-kubernetes') ≠ PCC ('https://github.com/ovn-org/ovn-kubernetes'). |
| extra.dev_stats_url | https://ovnkubernetes.devstats.cncf.io/ | — | https://ovn-kubernetes.devstats.cncf.io | — | Landscape ('https://ovnkubernetes.devstats.cncf.io/') ≠ CLOMonitor ('https://ovn-kubernetes.devstats.cncf.io'). |

### Oxia (sandbox)

- **Path:** Orchestration & Management / Coordination & Service Discovery
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/oxia-db/oxia | https://github.com/oxia-db | https://github.com/oxia-db/oxia | **No** | PCC ('https://github.com/oxia-db') and CLOMonitor ('https://github.com/oxia-db/oxia') disagree. Landscape ('https://github.com/oxia-db/oxia') ≠ PCC ('https://github.com/oxia-db'). |

### Paralus (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.accepted | 2022-12-14 | — | 2022-12-13 | — | Landscape ('2022-12-14') ≠ CLOMonitor ('2022-12-13'). |

### Parsec (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/parallaxsecond/parsec | https://github.com/parallaxsecond/parsec | https://github.com/parallaxsecond/community | **No** | PCC ('https://github.com/parallaxsecond/parsec') and CLOMonitor ('https://github.com/parallaxsecond/community') disagree. Landscape ('https://github.com/parallaxsecond/parsec') ≠ CLOMonitor ('https://github.com/parallaxsecond/community'). |
| extra.accepted | 2020-06-25 | — | 2020-06-23 | — | Landscape ('2020-06-25') ≠ CLOMonitor ('2020-06-23'). |

### Piraeus Datastore (sandbox)

- **Path:** Runtime / Cloud Native Storage
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | piraeus-datastore | piraeus | **No** | PCC slug 'piraeus-datastore' vs CLOMonitor name 'piraeus' (normalized identifiers differ). |
| repo_url | https://github.com/piraeusdatastore/piraeus-operator | https://github.com/piraeusdatastore/piraeus | https://github.com/piraeusdatastore/piraeus | Yes | Landscape ('https://github.com/piraeusdatastore/piraeus-operator') ≠ PCC ('https://github.com/piraeusdatastore/piraeus'). Landscape ('https://github.com/piraeusdatastore/piraeus-operator') ≠ CLOMonitor ('https://github.com/piraeusdatastore/piraeus'). |
| extra.lfx_slug | piraeus-datastore | piraeus-datastore | piraeus | **No** | PCC ('piraeus-datastore') and CLOMonitor ('piraeus') disagree. Landscape ('piraeus-datastore') ≠ CLOMonitor ('piraeus'). |
| extra.dev_stats_url | — | — | https://piraeus.devstats.cncf.io/ | — | Landscape missing; CLOMonitor has 'https://piraeus.devstats.cncf.io/'. |

### Pixie (sandbox)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/pixie-io/pixie | https://github.com/pixie-labs/pixie | https://github.com/pixie-io/pixie | **No** | PCC ('https://github.com/pixie-labs/pixie') and CLOMonitor ('https://github.com/pixie-io/pixie') disagree. Landscape ('https://github.com/pixie-io/pixie') ≠ PCC ('https://github.com/pixie-labs/pixie'). |
| extra.accepted | 2021-06-22 | — | 2021-06-15 | — | Landscape ('2021-06-22') ≠ CLOMonitor ('2021-06-15'). |

### Podman Container Tools (sandbox)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clo_via_pcc_slug+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| extra.clomonitor_name | podman | — | podman-container-tools | — | Landscape ('podman') ≠ CLOMonitor ('podman-container-tools'). |

### Podman Desktop (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/podman-desktop/podman-desktop | https://github.com/podman-desktop | https://github.com/podman-desktop/podman-desktop | **No** | PCC ('https://github.com/podman-desktop') and CLOMonitor ('https://github.com/podman-desktop/podman-desktop') disagree. Landscape ('https://github.com/podman-desktop/podman-desktop') ≠ PCC ('https://github.com/podman-desktop'). |

### Porter (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/getporter/porter | https://github.com/Porter | https://github.com/getporter/porter | **No** | PCC ('https://github.com/Porter') and CLOMonitor ('https://github.com/getporter/porter') disagree. Landscape ('https://github.com/getporter/porter') ≠ PCC ('https://github.com/Porter'). |

### Radius (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/radius-project/radius | https://github.com/radius-project | https://github.com/radius-project/radius | **No** | PCC ('https://github.com/radius-project') and CLOMonitor ('https://github.com/radius-project/radius') disagree. Landscape ('https://github.com/radius-project/radius') ≠ PCC ('https://github.com/radius-project'). |

### Ratify (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/ratify-project/ratify | https://github.com/deislabs/ratify | https://github.com/ratify-project/ratify | **No** | PCC ('https://github.com/deislabs/ratify') and CLOMonitor ('https://github.com/ratify-project/ratify') disagree. Landscape ('https://github.com/ratify-project/ratify') ≠ PCC ('https://github.com/deislabs/ratify'). |

### Runme Notebooks (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clo_via_pcc_slug+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/runmedev/runme | https://github.com/stateful/runme | https://github.com/runmedev/runme | **No** | PCC ('https://github.com/stateful/runme') and CLOMonitor ('https://github.com/runmedev/runme') disagree. Landscape ('https://github.com/runmedev/runme') ≠ PCC ('https://github.com/stateful/runme'). |
| extra.clomonitor_name | runme | — | runme-notebooks | — | Landscape ('runme') ≠ CLOMonitor ('runme-notebooks'). |
| extra.dev_stats_url | https://runmenotebooks.devstats.cncf.io/ | — | https://runme-notebooks.devstats.cncf.io | — | Landscape ('https://runmenotebooks.devstats.cncf.io/') ≠ CLOMonitor ('https://runme-notebooks.devstats.cncf.io'). |

### SchemaHero (sandbox)

- **Path:** App Definition and Development / Database
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/schemahero/schemahero | https://github.com/schemahero | https://github.com/schemahero/schemahero | **No** | PCC ('https://github.com/schemahero') and CLOMonitor ('https://github.com/schemahero/schemahero') disagree. Landscape ('https://github.com/schemahero/schemahero') ≠ PCC ('https://github.com/schemahero'). |

### Score (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/score-spec/spec | https://score.dev | https://github.com/score-spec/spec | **No** | PCC ('https://score.dev') and CLOMonitor ('https://github.com/score-spec/spec') disagree. Landscape ('https://github.com/score-spec/spec') ≠ PCC ('https://score.dev'). |

### Serverless Devs (sandbox)

- **Path:** Orchestration & Management / Scheduling & Orchestration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | serverlessdevs | serverless-devs | **No** | PCC slug 'serverlessdevs' vs CLOMonitor name 'serverless-devs' (normalized identifiers differ). |
| extra.lfx_slug | serverlessdevs | serverlessdevs | serverless-devs | **No** | PCC ('serverlessdevs') and CLOMonitor ('serverless-devs') disagree. Landscape ('serverlessdevs') ≠ CLOMonitor ('serverless-devs'). |
| extra.accepted | 2022-09-14 | — | 2022-09-13 | — | Landscape ('2022-09-14') ≠ CLOMonitor ('2022-09-13'). |

### Serverless Workflow (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | serverlessworkflow | serverless-workflow | **No** | PCC slug 'serverlessworkflow' vs CLOMonitor name 'serverless-workflow' (normalized identifiers differ). |
| repo_url | https://github.com/serverlessworkflow/specification | https://github.com/serverlessworkflow | https://github.com/serverlessworkflow/specification | **No** | PCC ('https://github.com/serverlessworkflow') and CLOMonitor ('https://github.com/serverlessworkflow/specification') disagree. Landscape ('https://github.com/serverlessworkflow/specification') ≠ PCC ('https://github.com/serverlessworkflow'). |
| extra.lfx_slug | serverlessworkflow | serverlessworkflow | serverless-workflow | **No** | PCC ('serverlessworkflow') and CLOMonitor ('serverless-workflow') disagree. Landscape ('serverlessworkflow') ≠ CLOMonitor ('serverless-workflow'). |

### Shipwright (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/shipwright-io/build | https://github.com/shipwright-io | https://github.com/shipwright-io/community | **No** | PCC ('https://github.com/shipwright-io') and CLOMonitor ('https://github.com/shipwright-io/community') disagree. Landscape ('https://github.com/shipwright-io/build') ≠ PCC ('https://github.com/shipwright-io'). Landscape ('https://github.com/shipwright-io/build') ≠ CLOMonitor ('https://github.com/shipwright-io/community'). |
| extra.dev_stats_url | https://shipwrightcncf.devstats.cncf.io/ | — | https://shipwright.devstats.cncf.io/ | — | Landscape ('https://shipwrightcncf.devstats.cncf.io/') ≠ CLOMonitor ('https://shipwright.devstats.cncf.io/'). |
| extra.accepted | 2024-08-19 | — | 2024-08-30 | — | Landscape ('2024-08-19') ≠ CLOMonitor ('2024-08-30'). |

### SlimFaaS (sandbox)

- **Path:** Serverless / Installable Platform
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/SlimPlanet/SlimFaas | https://github.com/AxaFrance/SlimFaas | https://github.com/AxaFrance/SlimFaas | Yes | Landscape ('https://github.com/SlimPlanet/SlimFaas') ≠ PCC ('https://github.com/AxaFrance/SlimFaas'). Landscape ('https://github.com/SlimPlanet/SlimFaas') ≠ CLOMonitor ('https://github.com/AxaFrance/SlimFaas'). |

### SOPS (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/getsops/sops | https://github.com/mozilla/sops | https://github.com/mozilla/sops | Yes | Landscape ('https://github.com/getsops/sops') ≠ PCC ('https://github.com/mozilla/sops'). Landscape ('https://github.com/getsops/sops') ≠ CLOMonitor ('https://github.com/mozilla/sops'). |

### Spin (sandbox)

- **Path:** Wasm / Application Frameworks
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/spinframework/spin | https://github.com/fermyon/spin | https://github.com/spinframework/spin | **No** | PCC ('https://github.com/fermyon/spin') and CLOMonitor ('https://github.com/spinframework/spin') disagree. Landscape ('https://github.com/spinframework/spin') ≠ PCC ('https://github.com/fermyon/spin'). |

### SpinKube (sandbox)

- **Path:** Wasm / Orchestration & Management
- **Matched:** PCC=False, CLOMonitor=True (clomonitor_name)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/spinframework/spin-operator | — | https://github.com/spinkube/documentation | — | Landscape ('https://github.com/spinframework/spin-operator') ≠ CLOMonitor ('https://github.com/spinkube/documentation'). |
| extra.lfx_slug | — | — | spinkube | — | Landscape missing; CLOMonitor has 'spinkube'. |

### Stacker (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/project-stacker/stacker | https://github.com/project-stacker | https://github.com/project-stacker/stacker | **No** | PCC ('https://github.com/project-stacker') and CLOMonitor ('https://github.com/project-stacker/stacker') disagree. Landscape ('https://github.com/project-stacker/stacker') ≠ PCC ('https://github.com/project-stacker'). |

### Submariner (sandbox)

- **Path:** Runtime / Cloud Native Network
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/submariner-io/submariner | https://github.com/submariner-io/ | https://github.com/submariner-io/submariner | **No** | PCC ('https://github.com/submariner-io/') and CLOMonitor ('https://github.com/submariner-io/submariner') disagree. Landscape ('https://github.com/submariner-io/submariner') ≠ PCC ('https://github.com/submariner-io/'). |
| extra.accepted | 2021-04-28 | — | 2021-04-27 | — | Landscape ('2021-04-28') ≠ CLOMonitor ('2021-04-27'). |

### Telepresence (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/telepresenceio/telepresence | https://github.com/telepresenceio | https://github.com/telepresenceio/telepresence | **No** | PCC ('https://github.com/telepresenceio') and CLOMonitor ('https://github.com/telepresenceio/telepresence') disagree. Landscape ('https://github.com/telepresenceio/telepresence') ≠ PCC ('https://github.com/telepresenceio'). |
| extra.accepted | 2018-05-15 | — | 2018-05-22 | — | Landscape ('2018-05-15') ≠ CLOMonitor ('2018-05-22'). |

### Tinkerbell (sandbox)

- **Path:** Provisioning / Automation & Configuration
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/tinkerbell/tinkerbell | https://github.com/tinkerbell/ | https://github.com/tinkerbell/tinkerbell | **No** | PCC ('https://github.com/tinkerbell/') and CLOMonitor ('https://github.com/tinkerbell/tinkerbell') disagree. Landscape ('https://github.com/tinkerbell/tinkerbell') ≠ PCC ('https://github.com/tinkerbell/'). |

### Tokenetes (sandbox)

- **Path:** Provisioning / Security & Compliance
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | tratteria | tokenetes | **No** | PCC slug 'tratteria' vs CLOMonitor name 'tokenetes' (normalized identifiers differ). |
| repo_url | https://github.com/tokenetes/tokenetes | https://github.com/tokenetes | https://github.com/tokenetes/tokenetes | **No** | PCC ('https://github.com/tokenetes') and CLOMonitor ('https://github.com/tokenetes/tokenetes') disagree. Landscape ('https://github.com/tokenetes/tokenetes') ≠ PCC ('https://github.com/tokenetes'). |
| extra.lfx_slug | tratteria | tratteria | tokenetes | **No** | PCC ('tratteria') and CLOMonitor ('tokenetes') disagree. Landscape ('tratteria') ≠ CLOMonitor ('tokenetes'). |
| extra.accepted | 2025-01-21 | — | 2025-01-16 | — | Landscape ('2025-01-21') ≠ CLOMonitor ('2025-01-16'). |

### Tremor (sandbox)

- **Path:** App Definition and Development / Streaming & Messaging
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/tremor-rs/tremor-runtime | https://github.com/tremor-rs/ | https://github.com/tremor-rs/tremor-runtime | **No** | PCC ('https://github.com/tremor-rs/') and CLOMonitor ('https://github.com/tremor-rs/tremor-runtime') disagree. Landscape ('https://github.com/tremor-rs/tremor-runtime') ≠ PCC ('https://github.com/tremor-rs/'). |

### Trickster (sandbox)

- **Path:** Observability and Analysis / Observability
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/trickstercache/trickster | https://github.com/tricksterproxy/trickster | https://github.com/trickstercache/trickster | **No** | PCC ('https://github.com/tricksterproxy/trickster') and CLOMonitor ('https://github.com/trickstercache/trickster') disagree. Landscape ('https://github.com/trickstercache/trickster') ≠ PCC ('https://github.com/tricksterproxy/trickster'). |

### urunc (sandbox)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/urunc-dev/urunc | https://github.com/urunc-dev | https://github.com/urunc-dev/urunc | **No** | PCC ('https://github.com/urunc-dev') and CLOMonitor ('https://github.com/urunc-dev/urunc') disagree. Landscape ('https://github.com/urunc-dev/urunc') ≠ PCC ('https://github.com/urunc-dev'). |

### Vineyard (sandbox)

- **Path:** Runtime / Cloud Native Storage
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/v6d-io/v6d | https://github.com/v6d-io/ | https://github.com/v6d-io/v6d | **No** | PCC ('https://github.com/v6d-io/') and CLOMonitor ('https://github.com/v6d-io/v6d') disagree. Landscape ('https://github.com/v6d-io/v6d') ≠ PCC ('https://github.com/v6d-io/'). |
| extra.accepted | 2021-04-28 | — | 2021-04-27 | — | Landscape ('2021-04-28') ≠ CLOMonitor ('2021-04-27'). |

### Virtual Kubelet (sandbox)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | virtualkubelet | virtual-kubelet | **No** | PCC slug 'virtualkubelet' vs CLOMonitor name 'virtual-kubelet' (normalized identifiers differ). |
| repo_url | https://github.com/virtual-kubelet/virtual-kubelet | https://github.com/virtual-kubelet | https://github.com/virtual-kubelet/virtual-kubelet | **No** | PCC ('https://github.com/virtual-kubelet') and CLOMonitor ('https://github.com/virtual-kubelet/virtual-kubelet') disagree. Landscape ('https://github.com/virtual-kubelet/virtual-kubelet') ≠ PCC ('https://github.com/virtual-kubelet'). |
| extra.lfx_slug | virtualkubelet | virtualkubelet | virtual-kubelet | **No** | PCC ('virtualkubelet') and CLOMonitor ('virtual-kubelet') disagree. Landscape ('virtualkubelet') ≠ CLOMonitor ('virtual-kubelet'). |

### Visual Studio Code Kubernetes Tools (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | vscodekubernetestools | vscode-kubernetes-tools | **No** | PCC slug 'vscodekubernetestools' vs CLOMonitor name 'vscode-kubernetes-tools' (normalized identifiers differ). |
| repo_url | https://github.com/vscode-kubernetes-tools/vscode-kuberne… | https://github.com/Azure/vscode-kubernetes-tools | https://github.com/vscode-kubernetes-tools/vscode-kuberne… | **No** | PCC ('https://github.com/Azure/vscode-kubernetes-tools') and CLOMonitor ('https://github.com/vscode-kubernetes-tools/vscode-kubernetes-tools') disagree. Landscape ('https://github.com/vscode-kubernetes-tools/vscode-kubernetes-tools') ≠ PCC ('https://github.com/Azure/vscode-kubernetes-tools'). |
| extra.lfx_slug | vscodekubernetestools | vscodekubernetestools | vscode-kubernetes-tools | **No** | PCC ('vscodekubernetestools') and CLOMonitor ('vscode-kubernetes-tools') disagree. Landscape ('vscodekubernetestools') ≠ CLOMonitor ('vscode-kubernetes-tools'). |

### WasmEdge Runtime (sandbox)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| identifiers | — | wasmedge-runtime | wasm-edge | **No** | PCC slug 'wasmedge-runtime' vs CLOMonitor name 'wasm-edge' (normalized identifiers differ). |
| extra.lfx_slug | wasmedge-runtime | wasmedge-runtime | wasm-edge | **No** | PCC ('wasmedge-runtime') and CLOMonitor ('wasm-edge') disagree. Landscape ('wasmedge-runtime') ≠ CLOMonitor ('wasm-edge'). |
| extra.accepted | 2021-04-28 | — | 2021-04-27 | — | Landscape ('2021-04-28') ≠ CLOMonitor ('2021-04-27'). |

### xRegistry (sandbox)

- **Path:** App Definition and Development / Application Definition & Image Build
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/xregistry/server | https://github.com/xregistry | https://github.com/xregistry/spec | **No** | PCC ('https://github.com/xregistry') and CLOMonitor ('https://github.com/xregistry/spec') disagree. Landscape ('https://github.com/xregistry/server') ≠ PCC ('https://github.com/xregistry'). Landscape ('https://github.com/xregistry/server') ≠ CLOMonitor ('https://github.com/xregistry/spec'). |
| extra.accepted | 2025-06-05 | — | 2025-06-03 | — | Landscape ('2025-06-05') ≠ CLOMonitor ('2025-06-03'). |

### youki (sandbox)

- **Path:** Runtime / Container Runtime
- **Matched:** PCC=True, CLOMonitor=True (clomonitor_name+lfx_slug)

| Field | Landscape | PCC | CLOMonitor | PCC≈CLO? | Note |
|-------|-----------|-----|------------|---------|------|
| repo_url | https://github.com/youki-dev/youki | https://github.com/containers/youki | https://github.com/containers/youki | Yes | Landscape ('https://github.com/youki-dev/youki') ≠ PCC ('https://github.com/containers/youki'). Landscape ('https://github.com/youki-dev/youki') ≠ CLOMonitor ('https://github.com/containers/youki'). |

## No datasource match

| Project | Maturity | Path |
|---------|----------|------|
| Service Mesh Interface (SMI) | archived | Orchestration & Management / Service Mesh |
| Cedar | sandbox | Provisioning / Security & Compliance |
| Higress | sandbox | Orchestration & Management / API Gateway |
| Monocle | sandbox | Observability and Analysis / Observability |