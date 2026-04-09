from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import EmailObservation, EmailAction
from tasks import TASKS


class EmailEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        super().__init__()
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.task_index = 0
        self.current_task = None

    def reset(self, seed=None, episode_id=None, **kwargs):
        ep_id = str(episode_id) if episode_id else str(uuid4())
        self._state = State(episode_id=ep_id, step_count=0)

        self.current_task = TASKS[self.task_index % len(TASKS)]
        self.task_index += 1

        return EmailObservation(
            email_text=self.current_task["input"],
            reward=0.5,
            done=False,
            metadata={
                "task": self.current_task["name"]
            }
        )

    def step(self, action: EmailAction, timeout_s=None, **kwargs):
        self._state.step_count += 1

        expected = self.current_task["expected"]
        predicted = action.action

        # 🔥 DIRECT REWARD
        if predicted == expected:
            reward = 0.8
        else:
            reward = 0.3

        return EmailObservation(
            email_text=self.current_task["input"],
            reward=reward,
            done=True,
            metadata={
                "task": self.current_task["name"],
                "expected": expected,
                "predicted": predicted
            }
        )

    @property
    def state(self):
        return self._state