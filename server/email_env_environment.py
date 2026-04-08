from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import EmailObservation, EmailAction
from tasks import TASKS


class EmailEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.task_index = 0
        self.current_task = None

    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.current_task = TASKS[self.task_index % len(TASKS)]
        self.task_index += 1

        return EmailObservation(
            email_text=self.current_task["input"],
            reward=0.5,
            done=False,
            metadata={
                "task": self.current_task["name"],
                "expected": self.current_task["expected"]
            }
        )

    def step(self, action: EmailAction) -> EmailObservation:
        self._state.step_count += 1

        expected = self.current_task["expected"]
        grader_fn = self.current_task["grader"]

        reward = grader_fn(action.action, expected)

        return EmailObservation(
            email_text=self.current_task["input"],
            reward=reward,
            done=True,
            metadata={
                "task": self.current_task["name"],
                "expected": expected,
                "predicted": action.action
            }
        )

    @property
    def state(self) -> State:
        return self._state