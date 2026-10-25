---
title: spectral_pca_kmeans_manifold
category: reasoning
engine: spectral_pca_kmeans
summary: Engine 20 PCA (68.6% var) & K-Means++ Cluster `C1_OOB_SERIAL_LOOPBACK_APPLIANCE` (Chokepoint: `Node:<TARGET_IP>`)
tags: [reasoning, spectral_pca_kmeans, pca, kmeans, spectral-laplacian, manifold, clustering]
updated: 2026-10-25 14:50:17
---
# spectral_pca_kmeans_manifold

> **Engine:** `spectral_pca_kmeans` | **Summary:** Engine 20 PCA (68.6% var) & K-Means++ Cluster `C1_OOB_SERIAL_LOOPBACK_APPLIANCE` (Chokepoint: `Node:<TARGET_IP>`)  
> **Backlink:** [[00_MEMORY_INDEX]] | **Updated:** `2026-10-25 14:50:17`

### Engine 20: SVD Principal Component Analysis (PCA), K-Means++ & Spectral Laplacian
- **Active K-Means++ Cluster Assignment**: **`C1_OOB_SERIAL_LOOPBACK_APPLIANCE`** — *Local L2 Reachable + TCP Refused (Exit 7) + OOB Serial Appliance* (Silhouette = `0.451`)
- **Cluster Strategic Focus**: Pivot to out-of-band serial console (/dev/ttyUSB0 / COM) or non-standard TCP port scan.
- **SVD PCA Cumulative Variance (Top 3 PCs)**: **`68.6%`** across `29` manifold states
  - **PC1 (`28.9%` var)**: Driven by `f3_target_in_local_l2` (+0.60), `f4_cross_subnet_l3_hop` (-0.42), `f1_default_or_static_route` (+0.36)
  - **PC2 (`23.7%` var)**: Driven by `f9_oob_serial_attached` (-0.56), `f8_open_tcp_port_verified` (+0.49), `f7_tcp_conn_refused_exit7` (-0.43)
  - **Low-Variance Noise Features (Ignore/Deprioritize)**: `f0_local_iface_cidr, f11_l7_goal_verified, f2_l2_arp_reachable`
- **Manifold Outlier / Anomaly Check**: `MANIFOLD_INLIER` (Mahalanobis $D_M = 0.780$, PCA Residual = `0.751`)
- **Spectral Graph Laplacian ($\lambda_2 = 0.734$)**: Chokepoint Cut-Vertices = `['Node:<TARGET_IP>']`
