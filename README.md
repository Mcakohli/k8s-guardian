<<<<<<< Updated upstream
# K8s Guardian — Policy-Enforced, Secure GitOps Engine

A production-hardened Kubernetes platform demonstrating zero-downtime resilience, in-cluster admission policy governance (Policy-as-Code), zero-trust credential encryption, and declarative GitOps continuous delivery with automated drift self-healing.

---

## 🏗️ Architecture Overview

The system runs on a 2-node **Kind** topology (`guardian-control-plane` and `guardian-worker`), enforcing non-root container runtimes, dual-stage health decoupling, Kyverno admission gates, Bitnami Sealed Secrets, and Argo CD automated synchronization.
┌────────────────────────┐
              │   GitHub Repository    │
              │  (k8s-guardian /main)  │
              └───────────┬────────────┘
                          │ GitOps Pull
                          ▼
              ┌────────────────────────┐
              │    Argo CD Engine      │
              │ (Self-Healing / Prune) │
              └───────────┬────────────┘
                          │ Declarative Sync
                          ▼
            ┌────────────────────────────┐
            │   Kubernetes API Server    │
            └─────────────┬──────────────┘
                          │
           Admission Gate │ (Validating Webhook)
                          ▼
              ┌────────────────────────┐
              │   Kyverno Controller   │
              │ (Enforce ClusterPolicy)│
              └───────────┬────────────┘
                          │
                Validated │ Workload Deployed
                          ▼
          ┌────────────────────────────────┐
          │     Worker Node Workloads      │
          │  • k8s-guardian-app (3 pods)   │
          │  • Sealed Secrets Controller   │
          └────────────────────────────────┘

          ---

## 🛡️ Core Engineering Milestones

### 1. Workload Resilience & Zero-Downtime Updates (Tier 1)
* **Probe Triad Decoupling**: Implemented `startupProbe`, `readinessProbe`, and `livenessProbe` to separate process deadlocks from graceful traffic management.
  * **Failure Simulation (`/kill`)**: Triggers an internal 500 error; the Kubelet detects liveness failure and automatically restarts the container.
  * **Traffic Shedding (`/unready`)**: Strips the failing pod from `Endpoints` without restarting the process.
* **Disruption Protection**: Configured `PodDisruptionBudget` (`minAvailable: 2`) across 3 replicas to guarantee high availability during administrative maintenance.
* **Rolling Update Guarantees**: Configured `RollingUpdate` with `maxUnavailable: 0` and `maxSurge: 25%`, ensuring 0 dropped HTTP requests during version updates.

### 2. Admission Governance via Policy-as-Code (Kyverno)
Installed Kyverno in `Enforce` mode to intercept API admission webhooks before manifests reach `etcd`:
* **`require-run-as-non-root`**: Hard-blocks containers attempting to execute as UID 0 (root).
* **`require-pod-resources`**: Eliminates noisy neighbors by mandating CPU/memory requests and limits.
* **`disallow-latest-tag`**: Enforces supply-chain immutability by banning mutable `:latest` tags.

### 3. Zero-Trust Secret Management (Bitnami Sealed Secrets)
* Eliminated raw or Base64 credentials from source control.
* Secrets are encrypted client-side using `kubeseal` with asymmetric encryption (AES-GCM + RSA).
* Only the in-cluster controller (`sealed-secrets-controller`) holds the private decryption key to materialize native `Secret` objects in cluster memory.

### 4. GitOps Continuous Delivery & Drift Correction (Argo CD)
* Configured Argo CD to track `k8s/base` from the GitHub repository as the single source of truth.
* Enforced automated sync with `selfHeal: true` and `prune: true`.
* **Validated Self-Healing**: Tampering with live cluster replicas (`kubectl scale --replicas=1`) is automatically detected by Argo CD, reverting the drift back to 3 replicas within seconds.

---

## 📂 Repository Structure

```text
├── app/
│   ├── Dockerfile           # Multi-stage build, unprivileged user (UID 10001), read-only root FS
│   ├── requirements.txt     # Pinned dependencies (FastAPI, Uvicorn)
│   └── src/
│       └── main.py          # Instrumented probe simulator (/healthz, /ready, /kill, /unready)
├── argocd/
│   └── application.yaml     # Argo CD Application manifest tracking HEAD
├── k8s/
│   ├── base/
│   │   ├── deployment.yaml  # 3 Replicas, RollingUpdate strategy, resource limits, probes
│   │   ├── pdb.yaml         # PodDisruptionBudget (minAvailable: 2)
│   │   └── service.yaml     # ClusterIP Service abstraction
│   ├── policies/
│   │   ├── disallow-latest-tag.yaml  # Kyverno policy banning :latest
│   │   ├── disallow-root.yaml        # Kyverno policy enforcing runAsNonRoot
│   │   └── require-resources.yaml    # Kyverno policy mandating requests/limits
│   └── secrets/
│       └── sealed-secret.yaml        # Asymmetrically encrypted secret manifest
└── kind-cluster.yaml        # 2-node local Kind cluster topology configuration
🚀 Quickstart & Reproduction
Prerequisites
Docker Desktop & WSL 2

kubectl, kind, and kubeseal CLI utilities

1. Cluster Setup & Workload Packaging
Bash
# Provision the local 2-node cluster
kind create cluster --name guardian --config kind-cluster.yaml

# Build hardened image and load into nodes
docker build -t k8s-guardian:v1.0.0 ./app
kind load docker-image k8s-guardian:v1.0.0 --name guardian
=======
@'

>> # K8s Guardian — Policy-Enforced, Secure GitOps Engine

>>

>> A production-hardened Kubernetes platform demonstrating zero-downtime resilience, in-cluster admission policy governance (Policy-as-Code), zero-trust credential encryption, and declarative GitOps continuous delivery with automated drift self-healing.

>>

>> ---

>>

>> ## 🏗️ Architecture Overview

>>

>> The system runs on a 2-node \*\*Kind\*\* topology (`guardian-control-plane` and `guardian-worker`), enforcing non-root container runtimes, dual-stage health decoupling, Kyverno admission gates, Bitnami Sealed Secrets, and Argo CD automated synchronization^C

PS C:\\Users\\rkkor\\Desktop\\cloud-engineering\\k8s-poka yoke> Get-Process -Name kubectl -ErrorAction SilentlyContinue^C

PS C:\\Users\\rkkor\\Desktop\\cloud-engineering\\k8s-poka yoke> @'

>> # K8s Guardian — Policy-Enforced, Secure GitOps Engine

>>

>> A production-hardened Kubernetes platform demonstrating zero-downtime resilience, in-cluster admission policy governance (Policy-as-Code), zero-trust credential encryption, and declarative GitOps continuous delivery with automated drift self-healing.

>>

>> ---

>>

>> ## 🏗️ Architecture Overview

>>

>> The system runs on a 2-node \*\*Kind\*\* topology (`guardian-control-plane` and `guardian-worker`), enforcing non-root container runtimes, dual-stage health decoupling, Kyverno admission gates, Bitnami Sealed Secrets, and Argo CD automated synchronization.

>> ┌────────────────────────┐

>>               │   GitHub Repository    │

>>               │  (k8s-guardian /main)  │

>>               └───────────┬────────────┘

>>                           │ GitOps Pull

>>                           ▼

>>               ┌────────────────────────┐

>>               │    Argo CD Engine      │

>>               │ (Self-Healing / Prune) │

>>               └───────────┬────────────┘

>>                           │ Declarative Sync

>>                           ▼

>>             ┌────────────────────────────┐

>>             │   Kubernetes API Server    │

>>             └─────────────┬──────────────┘

>>                           │

>>            Admission Gate │ (Validating Webhook)

>>                           ▼

>>               ┌────────────────────────┐

>>               │   Kyverno Controller   │

>>               │ (Enforce ClusterPolicy)│

>>               └───────────┬────────────┘

>>                           │

>>                 Validated │ Workload Deployed

>>                           ▼

>>           ┌────────────────────────────────┐

>>           │     Worker Node Workloads      │

>>           │  • k8s-guardian-app (3 pods)   │

>>           │  • Sealed Secrets Controller   │

>>           └────────────────────────────────┘

>> ---

>>

>> ## 🛡️ Core Engineering Milestones

>>

>> ### 1. Workload Resilience \& Zero-Downtime Updates (Tier 1)

>> \* \*\*Probe Triad Decoupling\*\*: Implemented `startupProbe`, `readinessProbe`, and `livenessProbe` to separate process deadlocks from graceful traffic management.

>>   \* \*\*Failure Simulation (`/kill`)\*\*: Triggers an internal 500 error; the Kubelet detects liveness failure and automatically restarts the container.

>>   \* \*\*Traffic Shedding (`/unready`)\*\*: Strips the failing pod from `Endpoints` without restarting the process.

>> \* \*\*Disruption Protection\*\*: Configured `PodDisruptionBudget` (`minAvailable: 2`) across 3 replicas to guarantee high availability during administrative maintenance.

>> \* \*\*Rolling Update Guarantees\*\*: Configured `RollingUpdate` with `maxUnavailable: 0` and `maxSurge: 25%`, ensuring 0 dropped HTTP requests during version updates.

>>

>> ### 2. Admission Governance via Policy-as-Code (Kyverno)

>> Installed Kyverno in `Enforce` mode to intercept API admission webhooks before manifests reach `etcd`:

>> \* \*\*`require-run-as-non-root`\*\*: Hard-blocks containers attempting to execute as UID 0 (root).

>> \* \*\*`require-pod-resources`\*\*: Eliminates noisy neighbors by mandating CPU/memory requests and limits.

>> \* \*\*`disallow-latest-tag`\*\*: Enforces supply-chain immutability by banning mutable `:latest` tags.

>>

>> ### 3. Zero-Trust Secret Management (Bitnami Sealed Secrets)

>> \* Eliminated raw or Base64 credentials from source control.

>> \* Secrets are encrypted client-side using `kubeseal` with asymmetric encryption (AES-GCM + RSA).

>> \* Only the in-cluster controller (`sealed-secrets-controller`) holds the private decryption key to materialize native `Secret` objects in cluster memory.

>>

>> ### 4. GitOps Continuous Delivery \& Drift Correction (Argo CD)

>> \* Configured Argo CD to track `k8s/base` from the GitHub repository as the single source of truth.

>> \* Enforced automated sync with `selfHeal: true` and `prune: true`.

>> \* \*\*Validated Self-Healing\*\*: Tampering with live cluster replicas (`kubectl scale --replicas=1`) is automatically detected by Argo CD, reverting the drift back to 3 replicas within seconds.

>>

>> ---

>>

>> ## 📂 Repository Structure

>>

>> ```text

>> ├── app/

>> │   ├── Dockerfile           # Multi-stage build, unprivileged user (UID 10001), read-only root FS

>> │   ├── requirements.txt     # Pinned dependencies (FastAPI, Uvicorn)

>> │   └── src/

>> │       └── main.py          # Instrumented probe simulator (/healthz, /ready, /kill, /unready)

>> ├── argocd/

>> │   └── application.yaml     # Argo CD Application manifest tracking HEAD

>> ├── k8s/

>> │   ├── base/

>> │   │   ├── deployment.yaml  # 3 Replicas, RollingUpdate strategy, resource limits, probes

>> │   │   ├── pdb.yaml         # PodDisruptionBudget (minAvailable: 2)

>> │   │   └── service.yaml     # ClusterIP Service abstraction

>> │   ├── policies/

>> │   │   ├── disallow-latest-tag.yaml  # Kyverno policy banning :latest

>> │   │   ├── disallow-root.yaml        # Kyverno policy enforcing runAsNonRoot

>> │   │   └── require-resources.yaml    # Kyverno policy mandating requests/limits

>> │   └── secrets/

>> │       └── sealed-secret.yaml        # Asymmetrically encrypted secret manifest

>> └── kind-cluster.yaml        # 2-node local Kind cluster topology configuration 

>>>>>>> Stashed changes
