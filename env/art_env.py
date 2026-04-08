import pydantic
from typing import Dict, Any, Tuple

class Action(pydantic.BaseModel):
    predicted_price: float
    description: str

class Observation(pydantic.BaseModel):
    features: Dict[str, Any]

class Reward(pydantic.BaseModel):
    value: float

class ArtEnv:
    def __init__(self, data: Dict[str, Any]):
        self.data = data

    def calculate_prices(self) -> Tuple[float, float]:
        # Actual Price = Base Cost + (Time * Rate) * Detail Multiplier
        labor_rate = 300 # Rs per hour
        actual = (self.data['mat'] + (self.data['time'] * labor_rate)) * (1 + self.data['detail'] * 0.05)
        
        # Predicted Price = Actual * (Story + Originality Multiplier)
        # Isse difference 0 nahi aayega
        market_multiplier = 1 + (self.data['orig'] * 0.1) + (self.data['story'] * 0.08)
        predicted = actual * market_multiplier
        
        return round(predicted, 2), round(actual, 2)

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        pred, act = self.calculate_prices()
        # Reward calculation scale 0-1
        reward_val = (self.data['orig'] + self.data['story'] + self.data['detail']) / 30.0
        return Observation(features=self.data), Reward(value=reward_val), True, {"pred": pred, "act": act}