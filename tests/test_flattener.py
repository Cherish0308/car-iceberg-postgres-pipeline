"""
Unit tests for the car pipeline.
Demonstrates how SOLID principles make testing easy through dependency injection.
"""
import sys
sys.path.insert(0, 'src')

import pytest
from domain import Car, CarDetail
from flattener import CarFlattener


class TestCarFlattener:
    """Test suite for CarFlattener following SOLID principles."""

    def test_flatten_single_car(self):
        """Test flattening a single car entry."""
        flattener = CarFlattener()
        
        json_data = {
            "cars": [
                {
                    "name": "Tesla",
                    "country": "USA",
                    "models": [
                        {
                            "name": "Model 3",
                            "year": 2024,
                            "specifications": {
                                "engine": {
                                    "type": "Electric",
                                    "displacement": "N/A",
                                    "horsepower": 283
                                },
                                "performance": {
                                    "topSpeed": 145,
                                    "zeroToSixty": "5.8 seconds"
                                },
                                "dimensions": {
                                    "length": "4694 mm",
                                    "weight": "1611 kg"
                                },
                                "features": {
                                    "fuelEconomy": "132 MPGe",
                                    "safety": ["Autopilot", "AEB"]
                                }
                            }
                        }
                    ]
                }
            ]
        }

        cars, car_details = flattener.flatten(json_data)

        assert len(cars) == 1
        assert len(car_details) == 1
        
        car = cars[0]
        assert isinstance(car, Car)
        assert car.brand_name == "Tesla"
        assert car.model_name == "Model 3"
        assert car.model_year == 2024
        assert car.country == "USA"
        
        detail = car_details[0]
        assert isinstance(detail, CarDetail)
        assert detail.engine_type == "Electric"
        assert detail.horsepower == 283
        assert detail.safety_features == "Autopilot,AEB"

    def test_flatten_multiple_cars(self):
        """Test flattening multiple car entries."""
        flattener = CarFlattener()
        
        json_data = {
            "cars": [
                {
                    "name": "Toyota",
                    "country": "Japan",
                    "models": [
                        {
                            "name": "Camry",
                            "year": 2024,
                            "specifications": {
                                "engine": {"type": "Hybrid", "displacement": "2.5L", "horsepower": 208},
                                "performance": {"topSpeed": 130, "zeroToSixty": "7.5 seconds"},
                                "dimensions": {"length": "4885 mm", "weight": "1520 kg"},
                                "features": {"fuelEconomy": "52 mpg", "safety": ["Lane Assist"]}
                            }
                        }
                    ]
                },
                {
                    "name": "Honda",
                    "country": "Japan",
                    "models": [
                        {
                            "name": "Accord",
                            "year": 2024,
                            "specifications": {
                                "engine": {"type": "Hybrid", "displacement": "2.0L", "horsepower": 204},
                                "performance": {"topSpeed": 125, "zeroToSixty": "7.3 seconds"},
                                "dimensions": {"length": "4970 mm", "weight": "1490 kg"},
                                "features": {"fuelEconomy": "48 mpg", "safety": ["Collision Mitigation"]}
                            }
                        }
                    ]
                }
            ]
        }

        cars, car_details = flattener.flatten(json_data)

        assert len(cars) == 2
        assert len(car_details) == 2
        assert cars[0].brand_name == "Toyota"
        assert cars[1].brand_name == "Honda"

    def test_car_id_generation_is_deterministic(self):
        """Test that car_id is consistently generated for same input."""
        flattener = CarFlattener()
        
        json_data = {
            "cars": [
                {
                    "name": "Ford",
                    "country": "USA",
                    "models": [
                        {
                            "name": "F-150",
                            "year": 2024,
                            "specifications": {
                                "engine": {"type": "V6", "displacement": "3.5L", "horsepower": 400},
                                "performance": {"topSpeed": 120, "zeroToSixty": "5.5 seconds"},
                                "dimensions": {"length": "5890 mm", "weight": "2200 kg"},
                                "features": {"fuelEconomy": "20 mpg", "safety": ["360 Camera"]}
                            }
                        }
                    ]
                }
            ]
        }

        cars1, _ = flattener.flatten(json_data)
        cars2, _ = flattener.flatten(json_data)

        assert cars1[0].car_id == cars2[0].car_id

    def test_car_to_dict(self):
        """Test Car domain model to_dict method."""
        car = Car(
            car_id="test123",
            brand_name="Tesla",
            country="USA",
            model_name="Model 3",
            model_year=2024
        )

        result = car.to_dict()

        assert result["car_id"] == "test123"
        assert result["brand_name"] == "Tesla"
        assert result["model_year"] == 2024

    def test_car_detail_to_dict(self):
        """Test CarDetail domain model to_dict method."""
        detail = CarDetail(
            car_id="test123",
            engine_type="Electric",
            displacement="N/A",
            horsepower=283,
            top_speed=145,
            zero_to_sixty="5.8s",
            length="4694 mm",
            weight="1611 kg",
            fuel_economy="132 MPGe",
            safety_features="Autopilot,AEB"
        )

        result = detail.to_dict()

        assert result["car_id"] == "test123"
        assert result["engine_type"] == "Electric"
        assert result["horsepower"] == 283
