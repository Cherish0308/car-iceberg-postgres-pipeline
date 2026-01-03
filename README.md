# Car Data Pipeline

Production data pipeline for car data ingestion, transformation, and persistence across Iceberg/S3 and PostgreSQL.

## Overview

Reads nested JSON from AWS S3, flattens into normalized tables, and persists to Apache Iceberg (Parquet in S3) and PostgreSQL with UPSERT semantics. Deployable to AWS Lambda.

## Requirements Met

- AWS S3 integration
- AWS Lambda deployment
- Local PostgreSQL database
- Python configparser for dev/prod configs
- SQLAlchemy ^2.0 with psycopg2-binary ^2.9
- Apache Iceberg table format
- Poetry build system
- Poetry Lambda ZIP creation
- Unit tests with pytest

## Architecture

```
S3 JSON (nested)
    ↓
[S3Reader] → raw dict
    ↓
[CarFlattener] → (Car[], CarDetail[])
    ↓
├─ [IcebergWriter] → S3 Parquet
└─ [PostgresWriter] → Postgres
    ↓
SUCCESS response
```

## Modules

| Module | Purpose |
|--------|---------|
| s3_reader.py | Read JSON from S3 |
| flattener.py | Transform nested → flat |
| iceberg_writer.py | Persist to Iceberg/S3 |
| postgres_writer.py | Persist to PostgreSQL |
| main.py | Pipeline orchestration |
| domain.py | Data models |
| interfaces.py | Protocol abstractions |
| config.py | Configuration management |

## Data Model

**cars table**
- car_id (PK)
- brand_name
- country
- model_name
- model_year

**car_detail table**
- car_id (PK)
- engine_type
- displacement
- horsepower
- top_speed
- zero_to_sixty
- length
- weight
- fuel_economy
- safety_features

## Setup

### Prerequisites
- Python 3.12+
- Poetry 1.7+
- PostgreSQL
- AWS credentials

### Installation
```bash
poetry install
```

### Run Tests
```bash
poetry run pytest tests/ -v
```

## Configuration

### Development (config_dev.ini)
- Postgres: localhost:5432/bootcamp
- S3: carproject-bucket/iceberg-warehouse/
- Catalog: SQLite with S3 storage

### Production (config_prod.ini)
- Postgres: prod-host:5432/car_db
- S3: prod-iceberg-warehouse/
- Catalog: AWS Glue

### Switching Environments
```bash
ENV=dev poetry run python ...
ENV=prod poetry run python ...
```

## Lambda Deployment

### Build
```bash
./scripts/build_lambda_zip.sh
```

### Deploy
```bash
aws lambda update-function-code \
  --function-name car-pipeline \
  --zip-file fileb://lambda.zip
```

## Project Stats

- Source: ~300 lines
- Python files: 8
- Tests: 8 (100% pass)
- Type hints: 100%

## Pipeline Status

| Component | Status |
|-----------|--------|
| Cars table | ✅ Active (150 records) |
| Car details | ✅ Active (150 records) |
| Iceberg (S3) | ✅ Active (6 Parquet files) |
| PostgreSQL | ✅ Ready |

## Known Limitations

1. **Iceberg Delete**: PyIceberg doesn't support delete on append tables
   - Current: Append-only with idempotent re-runs
   - Alternative: Spark-based UPSERT for production

2. **Glue Catalog**: Requires AWS Glue permissions
   - Current: SQLite catalog with S3 storage

## Dependencies

**Core:**
- boto3 ^1.34
- sqlalchemy ^2.0
- psycopg2-binary ^2.9
- pyiceberg ^0.6
- configparser ^7.2
- pyarrow ^22.0
- numpy ^2.4

**Dev:**
- pytest ^8.0
- setuptools ^80.9

## Code Quality

- 100% type hints
- SOLID principles
- Dependency injection
- Protocol-based abstractions
- Self-documenting code
- Python 3.12+ compatible

## Testing

```bash
poetry run pytest tests/ -v
```

## Security

- Credentials via environment variables / IAM roles
- Secrets in config files
- S3: minimal IAM permissions
- Database: connection pooling

## Contributing

1. Feature branch
2. Add tests
3. All tests pass
4. 100% type hints
5. Submit PR

## License

MIT

## Repo

https://github.com/Cherish0308/car-data-pipeline

