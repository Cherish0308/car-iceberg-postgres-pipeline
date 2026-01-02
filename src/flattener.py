"""
Flattener implementation following SRP and OCP.
SRP: Only responsible for flattening nested JSON into domain entities.
OCP: New flattening strategies can be added by creating new Flattener classes.
"""
from __future__ import annotations

import hashlib
from collections.abc import Sequence

from domain import Car, CarDetail
from interfaces import Flattener


def _generate_car_id(brand: str, model: str, year: int) -> str:
    """Generate deterministic car ID from key fields."""
    raw = f"{brand}_{model}_{year}"
    return hashlib.md5(raw.encode()).hexdigest()


class CarFlattener(Flattener):
    """
    Flattens nested car JSON into Car and CarDetail entities.
    Following SRP: Single responsibility of transforming nested data.
    """

    def flatten(self, json_data: dict[str, any]) -> tuple[Sequence[Car], Sequence[CarDetail]]:
        """Flatten nested JSON into normalized Car and CarDetail objects."""
        cars = []
        car_details = []

        for brand in json_data["cars"]:
            for model in brand["models"]:
                car_id = _generate_car_id(
                    brand["name"], model["name"], model["year"]
                )

                cars.append(
                    Car(
                        car_id=car_id,
                        brand_name=brand["name"],
                        country=brand["country"],
                        model_name=model["name"],
                        model_year=model["year"],
                    )
                )

                specs = model["specifications"]
                car_details.append(
                    CarDetail(
                        car_id=car_id,
                        engine_type=specs["engine"]["type"],
                        displacement=specs["engine"]["displacement"],
                        horsepower=specs["engine"]["horsepower"],
                        top_speed=specs["performance"]["topSpeed"],
                        zero_to_sixty=specs["performance"]["zeroToSixty"],
                        length=specs["dimensions"]["length"],
                        weight=specs["dimensions"]["weight"],
                        fuel_economy=specs["features"]["fuelEconomy"],
                        safety_features=",".join(specs["features"]["safety"]),
                    )
                )

        return cars, car_details