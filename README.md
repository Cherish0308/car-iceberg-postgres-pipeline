# Car Data Pipeline - SOLID Implementation

This project implements a data pipeline that reads car data from S3, flattens nested JSON, and writes to Postgres and Iceberg tables.

## SOLID Principles Applied

### 1. Single Responsibility Principle (SRP)
- **`S3Reader`**: Only responsible for reading from S3
- **`CarFlattener`**: Only responsible for flattening nested JSON into Car/CarDetail entities
- **`PostgresWriter`**: Only responsible for Postgres upserts
- **`IcebergWriter`**: Only responsible for Iceberg upserts
- **`CarPipeline`**: Only orchestrates the flow, doesn't know implementation details

### 2. Open/Closed Principle (OCP)
- Abstract `Reader`, `Flattener`, `Writer` protocols defined
- New readers (FileReader, KafkaReader) can be added without modifying existing code
- New writers (RedshiftWriter, SnowflakeWriter) can be added by implementing Writer protocol

### 3. Liskov Substitution Principle (LSP)
- Any `Writer` implementation can substitute another without breaking `CarPipeline`
- All writers accept the same contract: `upsert(table_name, records)`

### 4. Interface Segregation Principle (ISP)
- Separate protocols for Reader, Flattener, Writer
- Each component only depends on the interface it needs

### 5. Dependency Inversion Principle (DIP)
- `CarPipeline` depends on abstractions (protocols), not concrete classes
- Concrete implementations injected at runtime
- Easy to mock for testing

## Running Locally

```bash
# Install dependencies
poetry install

# Set up Postgres tables
psql postgresql://user:pass@localhost:5432/db -f setup_tables.sql

# Run pipeline
python run_real.py
```

## Running in AWS Lambda

```bash
# Package for Lambda
./build_lambda_zip.sh

# Upload lambda.zip to Lambda function
# Set environment variable: ENV=prod
```

## Iceberg Setup

For production Iceberg, use AWS Glue Catalog or configure PyIceberg with appropriate catalog in `config_prod.ini`.

Local Iceberg requires:
1. SQLAlchemy 2.0+
2. PyArrow
3. `pip install 'pyiceberg[sql-sqlite]'`

Current implementation focuses on Postgres; Iceberg integration can be enabled by uncommenting lines in `main.py`.
