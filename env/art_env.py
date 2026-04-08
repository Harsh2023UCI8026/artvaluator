from pydantic import BaseModel
from typing import Dict, Any, Optional

class Action(BaseModel):
    predicted_price: float
    description: str

class Observation(BaseModel):
    predicted_price: float
    true_price: float
    features: Optional[Dict[str, Any]] = None

class Reward(BaseModel):
    value: float

class ArtEnv:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.done = False
        self.true_price = 0.0
        self.factors = {}

    def reset(self) -> Observation:
        from utils.pricing import calculate_true_price
        # Ensure your utils/pricing.py has this function
        self.true_price, self.factors = calculate_true_price(self.data)
        self.done = False
        return Observation(predicted_price=0.0, true_price=self.true_price, features=self.data)

    def step(self, action: Action):
        # Calculate error-based reward
        error = abs(action.predicted_price - self.true_price)
        reward_value = max(0.0, 1.0 - (error / (self.true_price + 1e-6)))
        
        # Meaningful feedback logic: penalize very short descriptions
        if len(action.description.split()) < 5:
            reward_value *= 0.5

        self.done = True
        obs = Observation(predicted_price=action.predicted_price, true_price=self.true_price)
        reward = Reward(value=float(reward_value))
        
        info = {"error": error, "factors": self.factors}
        return obs, reward, self.done, info

    def state(self):
        return {"true_price": self.true_price, "done": self.done}