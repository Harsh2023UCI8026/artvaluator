# import pydantic
# from typing import Dict, Any, Tuple

# class Action(pydantic.BaseModel):
#     predicted_price: float
#     description: str

# class Observation(pydantic.BaseModel):
#     features: Dict[str, Any]

# class Reward(pydantic.BaseModel):
#     value: float

# class ArtEnv:
#     def __init__(self, data: Dict[str, Any]):
#         self.data = data

#     def calculate_prices(self) -> Tuple[float, float]:
#         # Actual Price = Base Cost + (Time * Rate) * Detail Multiplier
#         labor_rate = 300 # Rs per hour
#         actual = (self.data['mat'] + (self.data['time'] * labor_rate)) * (1 + self.data['detail'] * 0.05)
        
#         # Predicted Price = Actual * (Story + Originality Multiplier)
#         # Isse difference 0 nahi aayega
#         market_multiplier = 1 + (self.data['orig'] * 0.1) + (self.data['story'] * 0.08)
#         predicted = actual * market_multiplier
        
#         return round(predicted, 2), round(actual, 2)

#     def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
#         pred, act = self.calculate_prices()
#         # Reward calculation scale 0-1
#         reward_val = (self.data['orig'] + self.data['story'] + self.data['detail']) / 30.0
#         return Observation(features=self.data), Reward(value=reward_val), True, {"pred": pred, "act": act}












# import pydantic
# from typing import Dict, Any, Tuple

# class Action(pydantic.BaseModel):
#     predicted_price: float
#     description: str

# class Observation(pydantic.BaseModel):
#     features: Dict[str, Any]

# class Reward(pydantic.BaseModel):
#     value: float

# class ArtEnv:
#     def __init__(self, data: Dict[str, Any]):
#         self.data = data

#     def calculate_prices(self) -> Tuple[float, float]:
#         # Actual Cost = Material + (Hours * Skill Rate)
#         labor_rate = 300 
#         base_actual = self.data['mat'] + (self.data['time'] * labor_rate)
#         actual_price = base_actual * (1 + self.data['detail'] * 0.05)
        
#         # Predicted Price = Market Sentiment based on Story and Originality
#         # Isse difference hamesha non-zero rahega
#         multiplier = 1 + (self.data['orig'] * 0.12) + (self.data['story'] * 0.08)
#         predicted_price = actual_price * multiplier
        
#         return round(predicted_price, 2), round(actual_price, 2)

#     def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
#         pred, act = self.calculate_prices()
#         # Quality score out of 1.0
#         reward_val = (self.data['orig'] + self.data['story'] + self.data['detail']) / 30.0
        
#         return Observation(features=self.data), Reward(value=reward_val), True, {"pred": pred, "act": act}











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

    def calculate_valuation(self) -> Tuple[float, float]:
        # Actual Mathematical Price logic
        # Formula: (Material + Frame + (Time * Labor Rate)) * Complexity Factor
        labor_rate = 350 # Per hour cost
        base_cost = self.data['mat'] + self.data['frame']
        labor_total = self.data['time'] * labor_rate
        complexity_mult = 1 + (self.data['detail'] * 0.05)
        
        actual_price = (base_cost + labor_total) * complexity_mult
        
        # Predicted Market Price logic (Insaan ki emotion/story ki value)
        # Isme originality aur story depth add hoti hai
        # Difference 0 nahi aayega kyunki market sentiment cost se alag hota hai
        sentiment_bonus = 1 + (self.data['orig'] * 0.12) + (self.data['story'] * 0.15)
        predicted_price = actual_price * sentiment_bonus
        
        return round(predicted_price, 2), round(actual_price, 2)

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        pred, act = self.calculate_valuation()
        
        # Rewards based on quality of inputs (Max 1.0)
        reward_score = (self.data['orig'] + self.data['story'] + self.data['detail']) / 30.0
        
        info = {"pred": pred, "act": act}
        return Observation(features=self.data), Reward(value=reward_score), True, info