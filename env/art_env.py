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

    def calculate_logic(self) -> Tuple[float, float]:
        # Actual Price: Material + (Time * Rate) * Complexity
        actual = (self.data['mat'] + self.data['frame'] + (self.data['time'] * 250)) * (1 + self.data['detail']*0.05)
        # Predicted Price: Actual * (Originality + Story Multiplier)
        predicted = actual * (1 + (self.data['orig'] * 0.1) + (self.data['story'] * 0.05))
        return round(predicted, 2), round(actual, 2)

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        pred, act = self.calculate_logic()
        # Reward calculation (1.0 max)
        reward_val = (self.data['orig'] + self.data['story'] + self.data['detail']) / 30.0
        return Observation(features=self.data), Reward(value=reward_val), True, {"pred": pred, "act": act}