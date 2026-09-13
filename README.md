# K8s Guardian — Production-Hardened Kubernetes Platform & GitOps Engine

[![Kubernetes](https://img.shields.io/badge/kubernetes-v1.31-blue.svg)](https://kubernetes.io/)
[![Kyverno](https://img.shields.io/badge/kyverno-v1.12-green.svg)](https://kyverno.io/)
[![ArgoCD](https://img.shields.io/badge/argocd-v2.12-orange.svg)](https://argo-cd.readthedocs.io/)
[![Bitnami Sealed Secrets](https://img.shields.io/badge/sealed--secrets-v0.27-red.svg)](https://github.com/bitnami-labs/sealed-secrets)

A production-grade Kubernetes platform designed to solve common cloud-native deployment risks: cold-start latency deadlocks, unprivileged container security boundaries, unmanaged API admission drift, and credential leaks in public Git repositories.

---

## 📌 Why I Built This (Problem & Solution)

Most baseline Kubernetes deployments fail in production when under real-world stress:
* **Container Start Latency:** Processes often get killed prematurely by aggressive liveness probes before initializing database handles or runtime caches.
* **Privilege Breakouts:** Default images frequently execute as `root` (UID 0), allowing potential container-escape vulnerabilities.
* **Configuration Drift:** Out-of-band manual interventions (`kubectl scale`, `kubectl edit`) bypass audit logs and desynchronize the cluster state from Git.

**K8s Guardian** introduces an automated DevSecOps platform on a multi-node topology:
1. Decouples liveness failures from graceful readiness traffic shedding.
2. Enforces non-bypassable admission policies directly at the Kubernetes API webhook using **Kyverno**.
3. Stores asymmetrically encrypted secrets safely in Git using **Bitnami Sealed Secrets**.
4. Implements declarative continuous delivery and automated drift self-healing using **Argo CD**.

---

## 🏗️ Architecture Topology
┌────────────────────────┐
              │   GitHub Repository    │
              │  (k8s-guardian /main)  │
              └───────────┬────────────┘
                          │ Declarative GitOps Pull
                          ▼
              ┌────────────────────────┐
              │    Argo CD Engine      │
              │ (Self-Healing / Prune) │
              └───────────┬────────────┘
                          │ Reconciliation Loop
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
                          │ Validated Manifests
                          ▼
          ┌────────────────────────────────┐
          │     Worker Node Workloads      │
          │  • k8s-guardian-app (3 pods)   │
          │  • Sealed Secrets Controller   │
          └────────────────────────────────┘

---

## 🛡️ Core Architecture & Resilience Proof

### 1. Workload Resilience & Zero-Downtime Rollouts
* **Dual-Stage Probe Decoupling:** Implemented `startupProbe`, `readinessProbe`, and `livenessProbe` to decouple process termination from graceful endpoint traffic removal.
* **Rolling Update Guarantees:** Configured `strategy.rollingUpdate` (`maxUnavailable: 0`, `maxSurge: 25%`) and a `PodDisruptionBudget` (`minAvailable: 2`).
* **Continuous Traffic Verification:** Validated that streaming requests to `/` during an image upgrade (`v1.0.0` → `v1.1.0`) yielded **zero dropped connections and 100% 200 OK responses**.
  * Evidence: See [`docs/screenshots/Screenshot (1503).png`](docs/screenshots/Screenshot%20(1503).png) and [`docs/screenshots/Screenshot (1504).png`](docs/screenshots/Screenshot%20(1504).png).
* **Fault Injection Testing:**
  * Calling `/kill` intentionally trips the `/healthz` probe, causing the Kubelet to automatically kill and restart the single affected container (`RESTARTS: 1`).
  * Calling `/unready` trips `/ready`, causing the endpoint controller to cleanly drop the pod IP from 3 down to 2 active service endpoints without terminating the process.

### 2. Policy-as-Code Admission Control (Kyverno)
Installed Kyverno in `Enforce` mode to block insecure resources at the API webhook before manifests reach `etcd`:
* **`require-run-as-non-root`:** Blocks workloads running as UID 0 (`root`).
* **`require-pod-resources`:** Mandates explicit CPU/memory `requests` and `limits` to eliminate noisy neighbors.
* **`disallow-latest-tag`:** Rejects mutable `:latest` tags to guarantee immutable, traceable releases.
* **Negative Test Canary:** Tested using `k8s/tests/bad-root.yaml`, which is hard-blocked at the API gate with `admission webhook denied the request: Running as root is forbidden`.

### 3. Zero-Trust Secrets Management (Bitnami Sealed Secrets)
* Eliminated plaintext or Base64 secret storage in source control.
* Applied asymmetric encryption (AES-GCM + RSA) via the `kubeseal` CLI tool.
* Manifests are committed safely as `SealedSecret` custom resources; only the in-cluster controller (`sealed-secrets-controller`) in `kube-system` holds the private decryption key to materialize the native `Secret` in memory.

### 4. GitOps Delivery & Self-Healing (Argo CD)
* Configured Argo CD to track `k8s/base` from the remote repository as the single source of truth.
* Configured automated sync policies with `selfHeal: true` and `prune: true`.
* **Drift Remediation Test:** Manually tampering with live replicas (`kubectl scale deployment/k8s-guardian-app --replicas=1`) is automatically detected by the reconciliation controller, reverting the drift and restoring all 3 replicas within seconds.

---

## 📂 Repository Structure

```text
├── app/
│   ├── Dockerfile           # Multi-stage build, unprivileged user (UID 10001), read-only root FS
│   ├── requirements.txt     # Pinned dependencies (FastAPI, Uvicorn)
│   └── src/
│       └── main.py          # Instrumented probe simulator (/healthz, /ready, /kill, /unready)
├── argocd/
│   └── application.yaml     # Argo CD Application manifest tracking HEAD (selfHeal + prune)
├── docs/
│   └── screenshots/         # Verified terminal execution logs & architecture proof
├── k8s/
│   ├── base/
│   │   ├── deployment.yaml  # 3 Replicas, RollingUpdate strategy, resource limits, probes
│   │   ├── pdb.yaml         # PodDisruptionBudget (minAvailable: 2)
│   │   └── service.yaml     # ClusterIP Service abstraction
│   ├── policies/
│   │   ├── disallow-latest-tag.yaml  # Kyverno policy banning :latest
│   │   ├── disallow-root.yaml        # Kyverno policy enforcing runAsNonRoot
│   │   └── require-resources.yaml    # Kyverno policy mandating requests/limits
│   ├── secrets/
│   │   └── sealed-secret.yaml        # Asymmetrically encrypted secret manifest
│   └── tests/
│       ├── bad-latest.yaml           # Canary testing mutable tag policy
│       ├── bad-resources.yaml        # Canary testing missing resource limits
│       ├── bad-root.yaml             # Canary testing root execution denial
│       └── compliant.yaml            # Validated baseline manifest
├── kind-cluster.yaml        # 2-node local Kind cluster topology configuration
└── .gitignore               # Excludes secrets, binaries, and local build artifacts
