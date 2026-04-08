from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import EmailObservation, EmailAction
from tasks import TASKS


class EmailEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.tasks_data = [
            ("easy_spam_detection", "Win a FREE iPhone now!!!", "spam"),
            ("medium_classification", "Meeting at 5 PM today", "urgent"),
            ("hard_classification", "Lunch tomorrow?", "normal"),
        ]

        self.task_index = 0
        self.current = None

    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.current = self.tasks_data[self.task_index % len(self.tasks_data)]
        self.task_index += 1

        return EmailObservation(
            email_text=self.current[1],
            reward=0.5,
            done=False,
            metadata={
                "task": self.current[0],
                "expected": self.current[2]
            }
        )

    # ✅ CORRECTLY INSIDE CLASS
    def step(self, action: EmailAction) -> EmailObservation:
        self._state.step_count += 1

        task_name = self.current[0]
        expected = self.current[2]

        reward = TASKS[task_name](action.action, expected)

        return EmailObservation(
            email_text=self.current[1],
            reward=reward,
            done=True,
            metadata={
                "task": task_name,
                "expected": expected,
                "predicted": action.action
            }
        )

    @property
    def state(self) -> State:
        return self._state