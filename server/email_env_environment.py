from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import EmailObservation, EmailAction


class EmailEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.current = None

        self.tasks = [
            ("Win a FREE iPhone now!!!", "spam"),
            ("Meeting at 5 PM today", "urgent"),
            ("Lunch tomorrow?", "normal"),
        ]

        self.task_index = 0

    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.current = self.tasks[self.task_index % len(self.tasks)]
        self.task_index += 1

        return EmailObservation(
            email_text=self.current[0],
            reward=0.1,
            done=False,
            metadata={"expected": self.current[1]}
        )

    def step(self, action: EmailAction) -> EmailObservation:
        self._state.step_count += 1

        expected = self.current[1]

        if action.action == expected:
            reward = 0.9
        elif action.action in ["spam", "urgent", "normal"]:
            reward = 0.5
        else:
            reward = 0.1

        return EmailObservation(
            email_text=self.current[0],
            reward=reward,
            done=True,
            metadata={
                "expected": expected,
                "predicted": action.action
            }
        )

    @property
    def state(self) -> State:
        return self._state