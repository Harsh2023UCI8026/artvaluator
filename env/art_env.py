# from pydantic import BaseModel
# from typing import Dict, Any, Optional

# class Action(BaseModel):
#     predicted_price: float
#     description: str

# class Observation(BaseModel):
#     predicted_price: float
#     true_price: float
#     features: Optional[Dict[str, Any]] = None

# class Reward(BaseModel):
#     value: float

# class ArtEnv:
#     def __init__(self, data: Dict[str, Any]):
#         self.data = data
#         self.done = False
#         self.true_price = 0.0
#         self.factors = {}

#     def reset(self) -> Observation:
#         from utils.pricing import calculate_true_price
#         # Ensure your utils/pricing.py has this function
#         self.true_price, self.factors = calculate_true_price(self.data)
#         self.done = False
#         return Observation(predicted_price=0.0, true_price=self.true_price, features=self.data)

#     def step(self, action: Action):
#         # Calculate error-based reward
#         error = abs(action.predicted_price - self.true_price)
#         reward_value = max(0.0, 1.0 - (error / (self.true_price + 1e-6)))
        
#         # Meaningful feedback logic: penalize very short descriptions
#         if len(action.description.split()) < 5:
#             reward_value *= 0.5

#         self.done = True
#         obs = Observation(predicted_price=action.predicted_price, true_price=self.true_price)
#         reward = Reward(value=float(reward_value))
        
#         info = {"error": error, "factors": self.factors}
#         return obs, reward, self.done, info

#     def state(self):
#         return {"true_price": self.true_price, "done": self.done}










import pydantic
from enum import Enum
from typing import Dict, Any, Tuple

class Action(pydantic.BaseModel):
    predicted_price: float
    description: str

class Observation(pydantic.BaseModel):
    features: Dict[str, Any]
    market_stats: Dict[str, float]

class Reward(pydantic.BaseModel):
    value: float

class ArtEnv:
    def __init__(self, data: Dict[str, Any]):
        self.data = data
        self.done = False

    def reset(self) -> Observation:
        return Observation(
            features=self.data,
            market_stats={"current_demand": 0.8}
        )

    def calculate_prices(self) -> Tuple[float, float]:
        # Logic for Actual Price (Cost-based)
        base_cost = self.data['material_cost'] + self.data['frame_cost']
        labor_cost = self.data['time_spent'] * 250 # 250 per hour labor rate
        actual_price = base_cost + labor_cost
        
        # Adding uniqueness and detail multiplier to Actual Price
        actual_price *= (1 + (self.data['detail_level'] * 0.05) + (self.data['originality'] * 0.1))
        
        # Logic for Predicted Market Value (Demand/Emotional based)
        # Market value is often higher or lower than cost based on story depth
        predicted_market_value = actual_price * (1 + (self.data['story_score'] * 0.08))
        
        return round(predicted_market_value, 2), round(actual_price, 2)

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        pred_market, actual_cost = self.calculate_prices()
        
        # Reward logic based on how well the agent descriptions or predictions align
        # For simplicity in this UI version, we return a score based on data quality
        reward_val = (self.data['originality'] + self.data['story_score']) / 20.0
        
        info = {
            "predicted_price": pred_market,
            "actual_price": actual_cost,
            "difference": abs(pred_market - actual_cost)
        }
        
        self.done = True
        return self.reset(), Reward(value=reward_val), self.done, info