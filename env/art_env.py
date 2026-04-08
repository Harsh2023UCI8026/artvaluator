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

#     def calculate_valuation(self) -> Tuple[float, float]:
#         # HARD TASK LOGIC: Actual vs Predicted Price
#         # Actual Price: Purely mathematical (Material + Labor)
#         labor_rate = 350  # Rs per hour
#         base_cost = self.data.get('mat', 0) + self.data.get('frame', 0)
#         labor_cost = self.data.get('time', 0) * labor_rate
#         actual_price = (base_cost + labor_cost) * (1 + self.data.get('detail', 0) * 0.05)
        
#         # Predicted Price: Market value based on Narrative & Uniqueness
#         # Inke beech difference 0 nahi hoga because demand differs from cost
#         market_multiplier = 1 + (self.data.get('orig', 0) * 0.1) + (self.data.get('story', 0) * 0.15)
#         predicted_price = actual_price * market_multiplier
        
#         return round(predicted_price, 2), round(actual_price, 2)

#     def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
#         pred, act = self.calculate_valuation()
        
#         # Total Reward calculation (Max 1.0)
#         # Based on quality of originality, story, and detail
#         reward_score = (self.data.get('orig', 0) + self.data.get('story', 0) + self.data.get('detail', 0)) / 30.0
        
#         info = {
#             "pred": pred,
#             "act": act,
#             "justification": "Actual price is based on cost/labor, while Predicted is driven by emotional narrative and uniqueness."
#         }
        
#         return Observation(features=self.data), Reward(value=reward_score), True, info














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

#     def calculate_valuation(self) -> Tuple[float, float]:
#         # HARD TASK LOGIC: Actual vs Predicted Price
#         # Actual Price: Based on hard costs and labor
#         labor_rate = 350  # Per hour rate
#         base_costs = self.data.get('mat', 0) + self.data.get('frame', 0)
#         labor_total = self.data.get('time', 0) * labor_rate
        
#         # Skill and complexity multiplier
#         skill_factor = 1 + (self.data.get('detail', 0) * 0.05)
#         actual_price = (base_costs + labor_total) * skill_factor
        
#         # Predicted Price: Market value based on 'Story' and 'Originality'
#         # Difference remains non-zero because emotions drive market price
#         market_multiplier = 1 + (self.data.get('orig', 0) * 0.12) + (self.data.get('story', 0) * 0.15)
#         predicted_price = actual_price * market_multiplier
        
#         return round(predicted_price, 2), round(actual_price, 2)

#     def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
#         pred, act = self.calculate_valuation()
        
#         # Reward calculation based on depth of data provided (Max 1.0)
#         reward_val = (self.data.get('orig', 0) + self.data.get('story', 0) + self.data.get('detail', 0)) / 30.0
        
#         info = {
#             "pred": pred,
#             "act": act,
#             "justification": "Actual price reflects cost and labor, whereas Predicted price captures the intangible value of narrative and uniqueness."
#         }
        
#         return Observation(features=self.data), Reward(value=reward_val), True, info














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
        # Ensure data is always a dictionary
        self.data = data if data else {}

    def calculate_logic(self) -> Tuple[float, float]:
        # HARD TASK: Actual vs Predicted
        # Safely get values with defaults to avoid KeyError
        mat = self.data.get('mat', 0)
        frame = self.data.get('frame', 0)
        time = self.data.get('time', 0)
        detail = self.data.get('detail', 0)
        orig = self.data.get('orig', 0)
        story = self.data.get('story', 0)

        # Actual = (Material + Labor) * Complexity
        actual_price = (mat + frame + (time * 300)) * (1 + detail * 0.05)
        
        # Predicted = Actual * (Uniqueness + Narrative Multiplier)
        # Difference remains non-zero for justification
        predicted_price = actual_price * (1 + (orig * 0.10) + (story * 0.12))
        
        return round(predicted_price, 2), round(actual_price, 2)

    def step(self, action: Action) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        pred, act = self.calculate_logic()
        
        # Total Reward logic (Max 1.0)
        reward_val = (self.data.get('orig', 0) + self.data.get('story', 0) + self.data.get('detail', 0)) / 30.0
        
        info = {
            "pred": pred,
            "act": act,
            "msg": "Actual is cost-based; Predicted is value-based."
        }
        return Observation(features=self.data), Reward(value=reward_val), True, info