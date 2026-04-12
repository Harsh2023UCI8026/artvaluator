from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# -------------------------------
# Models (OpenEnv required format)
# -------------------------------

class Observation(BaseModel):
    echoed_message: str


class Action(BaseModel):
    message: str


class StepResponse(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict


# -------------------------------
# Simple Environment Logic
# -------------------------------

class SimpleEnv:
    def __init__(self):
        self.done = False

    def reset(self):
        self.done = False
        return Observation(echoed_message="")

    def step(self, action: Action):
        message = action.message

        # reward logic (same as your inference)
        reward = len(message) * 0.1

        # simple stop condition
        if len(message) > 50:
            self.done = True

        return StepResponse(
            observation=Observation(echoed_message=message),
            reward=reward,
            done=self.done,
            info={}
        )


env = SimpleEnv()

# -------------------------------
# REQUIRED ENDPOINTS
# -------------------------------

@app.post("/reset")
async def reset():
    obs = env.reset()
    return {
        "observation": obs,
        "reward": 0.0,
        "done": False,
        "info": {}
    }


@app.post("/step")
async def step(action: Action):
    result = env.step(action)
    return result


@app.get("/state")
async def state():
    return {
        "done": env.done
    }