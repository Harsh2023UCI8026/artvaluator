# env/art_env.py

from pydantic import BaseModel
from utils.pricing import calculate_true_price


class Action(BaseModel):
    predicted_price: float
    description: str


class Observation(BaseModel):
    predicted_price: float
    true_price: float


class Reward(BaseModel):
    value: float


class ArtEnv:

    def __init__(self, data):
        self.data = data
        self.done = False
        self.true_price = None

    def reset(self):
        self.true_price, self.factors = calculate_true_price(self.data)
        self.done = False

        return Observation(predicted_price=0, true_price=self.true_price)

    def step(self, action):
        error = abs(action.predicted_price - self.true_price)

        reward_value = max(0, 1 - error / self.true_price)

        self.done = True

        return (
            Observation(
                predicted_price=action.predicted_price,
                true_price=self.true_price
            ),
            Reward(value=reward_value),
            self.done,
            {
                "error": error,
                "factors": self.factors
            }
        )

    def state(self):
        return {
            "true_price": self.true_price,
            "done": self.done
        }