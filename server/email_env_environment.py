from uuid import uuid4
import random

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import EmailObservation, EmailAction


class EmailEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.emails = [
            ("Win a FREE iPhone now!!!", "spam"),
            ("Meeting at 5 PM today", "urgent"),
            ("Lunch tomorrow?", "normal"),
        ]

        self.current = None
        self.done = False

    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        self.current = random.choice(self.emails)
        self.done = False

        return EmailObservation(
            email_text=self.current[0],
            reward=0.0,
            done=False,
            metadata={"correct_label": self.current[1]}
        )

    def step(self, action: EmailAction) -> EmailObservation:
        self._state.step_count += 1

        correct = self.current[1]

        

        if action.action == correct:
         reward = 0.9
        elif action.action in ["spam", "urgent", "normal"]:
         reward = 0.5
        else:
         reward = 0.1
        self.done = True

        return EmailObservation(
            email_text=self.current[0],
            reward=reward,
            done=True,
            metadata={
                "correct_label": correct,
                "predicted": action.action
            }
        )

    @property
    def state(self) -> State:
        return self._state