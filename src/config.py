import configparser
import os

config = configparser.ConfigParser()
env = os.getenv("ENV", "dev")

config.read(f"config_{env}.ini")

POSTGRES_URL = config["postgres"]["url"]
S3_BUCKET = config["aws"]["bucket"]
ICEBERG_WAREHOUSE = config["iceberg"]["warehouse"]