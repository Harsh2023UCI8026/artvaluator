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

    def reset(self) -> Observation:
        return Observation(features=self.data)

    def compute_valuation(self) -> Tuple[float, float]:
        # Logic for Actual Mathematical Price
        hard_costs = self.data['material_cost'] + self.data['frame_cost']
        labor_value = self.data['time_spent'] * 200  # Rs 200/hour base labor
        skill_multiplier = 1 + (self.data['detail_level'] * 0.1)
        
        actual_price = (hard_costs + labor_value) * skill_multiplier
        
        # Logic for Predicted Market Value
        # Emotional story and originality drive market hype
        market_hype = 1 + (self.data['originality'] * 0.05) + (self.data['story_score'] * 0.15)
        predicted_price = actual_price * market_hype
        
        return round(predicted_price, 2), round(actual_price, 2)

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        predicted, actual = self.compute_valuation()
        
        # Reward based on data quality provided by user
        total_reward = (self.data['originality'] + self.data['detail_level'] + self.data['story_score']) / 30.0
        
        info = {
            "predicted_price": predicted,
            "actual_price": actual
        }
        
        return self.reset(), Reward(value=total_reward), True, info