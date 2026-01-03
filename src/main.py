from __future__ import annotations

import json

from s3_reader import S3Reader
from flattener import CarFlattener
from postgres_writer import PostgresWriter
from iceberg_writer import IcebergWriter

from interfaces import Reader, Flattener, Writer


class CarPipeline:

    def __init__(self, reader: Reader, flattener: Flattener, writers: list[Writer]):
        self._reader = reader
        self._flattener = flattener
        self._writers = writers

    def process(self, event: dict[str, any]) -> dict[str, str]:
        data = self._reader.read(event)
        cars, car_details = self._flattener.flatten(data)

        for writer in self._writers:
            writer.upsert("cars", [car.to_dict() for car in cars])
            writer.upsert("car_detail", [detail.to_dict() for detail in car_details])

        return {"status": "SUCCESS"}


def lambda_handler(event, context):
    reader = S3Reader()
    flattener = CarFlattener()
    writers = [
        PostgresWriter(),
        IcebergWriter(),
    ]

    pipeline = CarPipeline(reader, flattener, writers)
    return pipeline.process(event)
