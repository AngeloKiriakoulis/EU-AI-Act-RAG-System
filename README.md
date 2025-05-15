# EU AI Act RAG System

A lightweight Retrieval-Augmented Generation (RAG) system designed to answer user questions about the European Union AI Act.

This project combines FastAPI, PostgreSQL, Voyage AI embeddings, and Google Gemini 1.5 Pro to deliver accurate answers based on EU legislative text.

---

## 📦 Project Structure

| Service         | Description |
|-----------------|-------------|
| `fastapi-app`   | Handles user questions, retrieves relevant document chunks, and returns answers using Gemini |
| `db`            | Main PostgreSQL DB for embedded text chunks |
| `logs-db`       | Secondary PostgreSQL DB for logging user queries and response metadata |
| `pgadmin4` (optional) | UI to explore both databases |

---

## 🛠️ Tech Stack

- Python 3.12
- FastAPI
- PostgreSQL (x2)
- Docker & Docker Compose (optional)
- MicroK8s (for Kubernetes-based production deployments)
- Voyage AI (for text embeddings)
- Google Gemini 1.5 Pro (for answer generation)

---

## 🚀 Local Development Options

### Option 1: 🐳 Docker Compose (Quick Start)

#### 1. Clone the Repository

```bash
git clone https://github.com/AngeloKiriakoulis/eu.git
cd eu
```

#### 2. Create a `.env` file

```env
# Main DB
DB_NAME=eu_act
DB_USER=postgres
DB_PASSWORD=yourpassword
DB_PORT=5432

# Logs DB
LOGS_DB=eu_logs
LOGS_USER=postgres
LOGS_PASSWORD=yourpassword
LOGS_DB_PORT=5432
LOGS_HOST=logs_db

# APIs
VOYAGE_API_KEY=your_voyage_api_key
GOOGLE_API_KEY=your_google_api_key
```

#### 3. Start the system

```bash
docker compose up --build
```

#### 4. PgAdmin Access

- Navigate to: `http://localhost:5050`
- Default login: `pgadmin4@admin.com` / `admin`
- Manually add connections to:
  - `db` (`eu_act`)
  - `logs_db` (`eu_logs`)

---

### Option 2: ☸️ Deploy to MicroK8s (Kubernetes Mode)

> Recommended for real-world cluster-based environments.

#### 1. Install MicroK8s (Ubuntu)

```bash
sudo snap install microk8s --classic
sudo microk8s enable dns storage
```

Optional (but useful):

```bash
sudo microk8s enable ingress
```

#### 2. Apply Kubernetes Manifests

In the `k8s/` folder:

- `pv.yaml`, `pvc.yaml`: Persistent volumes
- `deployment.yaml`: Deploys FastAPI + Postgres DBs
- `services.yaml`: Exposes services (NodePort by default)

Run:

```bash
kubectl apply -f k8s/
```

#### 3. Access the FastAPI App

Use `kubectl get svc` to find the correct NodePort, then visit:

```text
http://<MicroK8s-IP>:<NodePort>
```

Example:

```
http://172.19.205.48:31262
```

---

## 🔌 API Endpoints

### `POST /api/ask`

**Request**

```json
{
  "text": "What is the AI Act?"
}
```

**Response**

```json
{
  "answer": "The AI Act regulates the use of AI in the EU...",
  "chunks": [
    {
      "text": "Relevant chunk text...",
      "metadata": {...},
      "distance": 0.14
    }
  ]
}
```

---

### `GET /health`

```json
{ "status": "ok" }
```

### `GET /info`

```json
{
  "model": "gemini-1.5-pro",
  "embedding_model": "voyage-2",
  "chunk_limit": 3
}
```

---

## 🗃️ Logs Database Schema

```sql
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    top_chunks JSONB,
    distances FLOAT[]
);
```

---

## 🙌 Credits

Created by **Aggelos** — designed to be a robust, developer-friendly system for exploring real-world legislation using state-of-the-art GenAI techniques.

---

## 🧠 Future Enhancements

- Helm chart packaging
- TLS/Ingress + domain setup
- Autoscaling and HPA configs
- Prometheus + Grafana observability stack
- PostgreSQL HA with persistent volumes
