# eligibility-service

eligibility-service — domain: insurance

- **Port:** 8800
- **Language:** Python 3.11 + Flask
- **Database:** `insurance` (Postgres, table `eligibility`)
- **Event bus:** Kafka

## API

| Method    | Path                       |
|-----------|----------------------------|
| GET       | `/api/eligibility/`          |
| POST      | `/api/eligibility/`          |
| GET       | `/api/eligibility/<id>`      |
| PUT/PATCH | `/api/eligibility/<id>`      |
| DELETE    | `/api/eligibility/<id>`      |
| GET       | `/health`                  |
| GET       | `/ready`                   |

## Events

**Publishes:** (none)
**Subscribes:** patient.created

## HTTP peer dependencies

- `payer-directory`
- `payer-edi-connect`
- `audit-log-service`

## Local dev

```bash
pip install -e ../../libs/py-healthcare-common
pip install -r requirements.txt
cp .env.example .env
(cd ../../infra && docker compose up -d postgres kafka kafka-init)
python -m app.main
```

## Tests

```bash
pytest
```
