"""
Integration tests demonstrating Dependency Injection with mocks.
Shows how SOLID principles make testing easy.
"""
import sys
sys.path.insert(0, 'src')

import pytest
from unittest.mock import Mock, MagicMock
from typing import Dict, Any

from main import CarPipeline
from domain import Car, CarDetail


class MockReader:
    """Mock Reader for testing."""
    
    def __init__(self, data):
        self.data = data
    
    def read(self, event):
        return self.data


class MockFlattener:
    """Mock Flattener for testing."""
    
    def __init__(self, cars, details):
        self.cars = cars
        self.details = details
    
    def flatten(self, data):
        return self.cars, self.details


class MockWriter:
    """Mock Writer for testing."""
    
    def __init__(self):
        self.calls = []
    
    def upsert(self, table, records):
        self.calls.append({"table": table, "records": records})


class TestCarPipeline:
    """Test suite for CarPipeline demonstrating DIP."""

    def test_pipeline_with_mocked_dependencies(self):
        """Test that pipeline correctly coordinates components."""
        # Arrange: Create mocks
        test_cars = [
            Car("id1", "Tesla", "USA", "Model 3", 2024),
            Car("id2", "Toyota", "Japan", "Camry", 2024)
        ]
        test_details = [
            CarDetail("id1", "Electric", "N/A", 283, 145, "5.8s", 
                     "4694mm", "1611kg", "132MPGe", "Autopilot"),
            CarDetail("id2", "Hybrid", "2.5L", 208, 130, "7.5s", 
                     "4885mm", "1520kg", "52mpg", "Lane Assist")
        ]

        reader = MockReader({"test": "data"})
        flattener = MockFlattener(test_cars, test_details)
        writer = MockWriter()

        pipeline = CarPipeline(reader, flattener, [writer])

        # Act
        result = pipeline.process({"key": "test.json"})

        # Assert
        assert result["status"] == "SUCCESS"
        assert len(writer.calls) == 2  # cars and car_details
        
        # Verify cars were written
        cars_call = [c for c in writer.calls if c["table"] == "cars"][0]
        assert len(cars_call["records"]) == 2
        assert cars_call["records"][0]["brand_name"] == "Tesla"
        
        # Verify details were written
        details_call = [c for c in writer.calls if c["table"] == "car_detail"][0]
        assert len(details_call["records"]) == 2
        assert details_call["records"][0]["engine_type"] == "Electric"

    def test_pipeline_with_multiple_writers(self):
        """Test that pipeline writes to all configured writers."""
        # Arrange
        test_cars = [Car("id1", "Ford", "USA", "F-150", 2024)]
        test_details = [CarDetail("id1", "V6", "3.5L", 400, 120, "5.5s",
                                  "5890mm", "2200kg", "20mpg", "360 Camera")]

        reader = MockReader({})
        flattener = MockFlattener(test_cars, test_details)
        writer1 = MockWriter()
        writer2 = MockWriter()

        pipeline = CarPipeline(reader, flattener, [writer1, writer2])

        # Act
        pipeline.process({})

        # Assert: Both writers should be called
        assert len(writer1.calls) == 2
        assert len(writer2.calls) == 2

    def test_pipeline_handles_empty_data(self):
        """Test pipeline with no cars."""
        # Arrange
        reader = MockReader({})
        flattener = MockFlattener([], [])
        writer = MockWriter()

        pipeline = CarPipeline(reader, flattener, [writer])

        # Act
        result = pipeline.process({})

        # Assert
        assert result["status"] == "SUCCESS"
        assert len(writer.calls) == 2  # Still called, but with empty lists
