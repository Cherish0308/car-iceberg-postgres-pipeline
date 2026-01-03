from __future__ import annotations

class Car:

    def __init__(
        self,
        car_id: str,
        brand_name: str,
        country: str,
        model_name: str,
        model_year: int,
    ) -> None:
        self.car_id = car_id
        self.brand_name = brand_name
        self.country = country
        self.model_name = model_name
        self.model_year = model_year

    def to_dict(self) -> dict[str, any]:
        return {
            "car_id": self.car_id,
            "brand_name": self.brand_name,
            "country": self.country,
            "model_name": self.model_name,
            "model_year": self.model_year,
        }


class CarDetail:

    def __init__(
        self,
        car_id: str,
        engine_type: str,
        displacement: str,
        horsepower: int,
        top_speed: any,
        zero_to_sixty: str,
        length: str,
        weight: str,
        fuel_economy: str,
        safety_features: str,
    ) -> None:
        self.car_id = car_id
        self.engine_type = engine_type
        self.displacement = displacement
        self.horsepower = horsepower
        self.top_speed = top_speed
        self.zero_to_sixty = zero_to_sixty
        self.length = length
        self.weight = weight
        self.fuel_economy = fuel_economy
        self.safety_features = safety_features

    def to_dict(self) -> dict[str, any]:
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
