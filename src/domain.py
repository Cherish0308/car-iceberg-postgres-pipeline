"""
Domain models for the car pipeline.
Following SRP: Each class has one responsibility - representing a domain entity.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Car:
    """Immutable car entity."""
    car_id: str
    brand_name: str
    country: str
    model_name: str
    model_year: int

    def to_dict(self) -> dict[str, any]:
        """Convert to dictionary for database operations."""
        return {
            "car_id": self.car_id,
            "brand_name": self.brand_name,
            "country": self.country,
            "model_name": self.model_name,
            "model_year": self.model_year,
        }


@dataclass(frozen=True)
class CarDetail:
    """Immutable car detail entity."""
    car_id: str
    engine_type: str
    displacement: str
    horsepower: int
    top_speed: any  # Can be int or string based on data
    zero_to_sixty: str
    length: str
    weight: str
    fuel_economy: str
    safety_features: str

    def to_dict(self) -> dict[str, any]:
        """Convert to dictionary for database operations."""
        return {
            "car_id": self.car_id,
            "engine_type": self.engine_type,
            "displacement": self.displacement,
            "horsepower": self.horsepower,
            "top_speed": self.top_speed,
            "zero_to_sixty": self.zero_to_sixty,
            "length": self.length,
            "weight": self.weight,
            "fuel_economy": self.fuel_economy,
            "safety_features": self.safety_features,
        }
