import configparser
import os

config = configparser.ConfigParser()
env = os.getenv("ENV", "dev")
config.read(f"config_{env}.ini")

POSTGRES_URL = config["postgres"]["url"]
S3_BUCKET = config["aws"]["bucket"]
AWS_REGION = config["aws"]["region"]
ICEBERG_WAREHOUSE = config["iceberg"]["warehouse"]
GLUE_ENABLED = config.getboolean("iceberg", "glue_enabled", fallback=False)
GLUE_CATALOG_NAME = config.get("iceberg", "glue_catalog_name", fallback="AwsDataCatalog")