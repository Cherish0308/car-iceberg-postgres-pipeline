"""
Main Lambda handler following SOLID principles.
Demonstrates Dependency Inversion: depends on abstractions (protocols), not concretions.
"""
from __future__ import annotations

import json

from s3_reader import S3Reader
from flattener import CarFlattener
from postgres_writer import PostgresWriter
from iceberg_writer import IcebergWriter

from interfaces import Reader, Flattener, Writer


class CarPipeline:
    """
    Orchestrates the car data pipeline.
    Following SRP: Single responsibility of coordinating pipeline flow.
    Following DIP: Depends on abstractions (Reader, Flattener, Writer).
    """

    def __init__(self, reader: Reader, flattener: Flattener, writers: list[Writer]):
        """
        Initialize pipeline with injected dependencies.
        
        Args:
            reader: Any Reader implementation.
            flattener: Any Flattener implementation.
            writers: List of Writer implementations.
        """
        self._reader = reader
        self._flattener = flattener
        self._writers = writers

    def process(self, event: dict[str, any]) -> dict[str, str]:
        """
        Process car data through the pipeline.
        
        Args:
            event: Event containing data source information.
            
        Returns:
            Status dictionary.
        """
        # Read data
        data = self._reader.read(event)

        # Flatten data
        cars, car_details = self._flattener.flatten(data)

        # Write to all configured sinks
        for writer in self._writers:
            # Convert domain objects to dicts
            writer.upsert("cars", [car.to_dict() for car in cars])
            writer.upsert("car_detail", [detail.to_dict() for detail in car_details])

        return {"status": "SUCCESS"}


def lambda_handler(event, context):
    """
    AWS Lambda entry point.
    Demonstrates Dependency Injection and composition.
    """
    # Compose pipeline with concrete implementations
    reader = S3Reader()
    flattener = CarFlattener()
    writers = [
        PostgresWriter(),
        IcebergWriter(),
    ]

    pipeline = CarPipeline(reader, flattener, writers)
    return pipeline.process(event)
