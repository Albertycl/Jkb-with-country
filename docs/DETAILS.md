# Jkb-with-country: full details

[Back to the short README](../README.md)

**Live demo:** https://jkb.albertycliu.xyz (made-up seed data, no login)

An ISP status board for network operations. It shows, per site (Alpha and Bravo), country and region, which internet providers (PCCW, TWG-G, Chief, Singtel) have failing probes, and it raises a "Possible Incoming / Outgoing Issue" banner. The data normally comes from a synthetic-monitoring SaaS (JianKongBao) and Cedexis. **This demo runs on made-up seed data**: the external feeds are switched off.

## What it is and why it matters for SRE

- **Who uses it:** a network operations team that wants one screen for "which ISP, where, is broken".
- **SRE skills shown:** containers (non-root backend, health checks, compose), configuration through environment variables (no secrets in Git), a feature flag (`ENABLE_POLLERS`) that switches off external feeds, re-runnable seed data, GitOps delivery with Argo CD, CI/CD with GitHub Actions, and rollback with `git revert`.
- **Deliberately simple:** one backend, one frontend, one database. No authentication on the UI or the read API (see Known limits).

## Architecture

| Part | Tech | Notes |
|---|---|---|
| frontend | Vue 3 + Quasar, served by nginx | nginx proxies same-origin `/api/` to the backend (`API_UPSTREAM`) |
| backend | Flask + SQLAlchemy, gunicorn | runs as a non-root user; creates its tables at start; `/api` is reached only through the frontend |
| database | MariaDB 11 | a separate container; with compose the app uses its own database and user, on K3s it connects as root to its own database `jkb_with_country` (demo setup) |
| delivery | GitHub Actions, GHCR, Argo CD | manifests live in [`Albertycl/gitops-apps`](https://github.com/Albertycl/gitops-apps) under `manifests/jkb-with-country/` |

A request flows: browser, nginx (frontend), `/api/...` to the Flask backend, MariaDB.

## Install and run

### Locally with Docker Compose

Prerequisites: Docker with Compose, and a MariaDB container reachable on the Docker network `netdiag_default` (the compose file joins that existing network).

```bash
# one-time: a network and a database container (skip if you already have them)
docker network create netdiag_default
docker run -d --name netdiag-mariadb-1 --network netdiag_default \
  -e MARIADB_RANDOM_ROOT_PASSWORD=1 \
  -e MARIADB_DATABASE=jkb_with_country -e MARIADB_USER=jkb -e MARIADB_PASSWORD='choose-a-password' \
  mariadb:11.1

cp .env.example .env     # set MYSQL_PASSWORD to the same password
docker compose up --build
```

Open `http://<server-ip>:5436` (change `FRONTEND_PORT` in `.env` to use another port). Stop with `docker compose down`; the data stays in the database container.

Variables: `MYSQL_*` (database), `FRONTEND_PORT`, `ENABLE_POLLERS` (keep `false` for the demo), `SEED_DEMO_DATA` (reload the made-up data on every start; it replaces the sensor tables, so set it to `false` if you point the app at a database with real data). The `JKB_*`, `CEDEXIS_TOKEN` and `INFRA_LOOKUP_URL` values are only needed when `ENABLE_POLLERS=true` and are left empty here. Never commit `.env`.

### On Kubernetes (K3s) with Argo CD

1. Only on a fresh cluster: bootstrap Argo CD once with `kubectl apply -f argocd/root-app.yaml` from the GitOps repo. The root app picks up `apps/jkb-with-country.yaml` and syncs `manifests/jkb-with-country/`.
2. Create the Secret by hand after Argo CD has created the namespace (names and keys only; values are never in Git): `jkb-db` with keys `database-url` and `root-password`.
3. After the first CI run, set the two GHCR packages (`jkb-with-country-backend`, `jkb-with-country-frontend`) to public, otherwise pods show `ImagePullBackOff`.
4. Check: `kubectl get applications -n argocd` shows `Synced` and `Healthy`, and `kubectl get pods -n jkb` shows the pods Ready.

## CI/CD and rollback

A push to `main` runs `.github/workflows/ci.yml`: install and import check, then build and push the two images to GHCR (tagged with the commit SHA and `latest`), then `update-gitops` runs `kustomize edit set image` in the GitOps repo and pushes with a deploy key (`GITOPS_DEPLOY_KEY`). Argo CD syncs the change. To roll back, `git revert` the "deploy <sha>" commit in the GitOps repo; with self-heal on, `kubectl rollout undo` would be undone.

## Monitoring

None is built in. The app exposes no `/metrics`; the container health checks and the Argo CD status are what exist.

## Known limits

- No authentication on the UI or the read API. The public demo is open on purpose: it only shows made-up seed data and the poller/write routes are switched off. Add authentication before using real data.
- CI checks only that the backend imports; the frontend is built (and so checked) when its image is built.
- The feeds are stubbed: the board shows seed data, not live probes.
- The frontend nginx image runs as root.
- The "Incoming vs Outgoing" rule (one failing probe = incoming, two or more = outgoing) is a simple heuristic, not a diagnosis.
