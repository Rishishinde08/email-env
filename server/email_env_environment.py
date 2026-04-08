from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State
from openenv.core.rubrics.base import Rubric
from openenv.core.rubrics.containers import RubricDict

from models import EmailObservation, EmailAction
from tasks import TASKS


class TaskGrader(Rubric):
    def __init__(self, grader_fn, expected):
        super().__init__()
        self.grader_fn = grader_fn
        self.expected = expected

    def forward(self, action: EmailAction, observation: EmailObservation) -> float:
        try:
            return float(self.grader_fn(action.action, self.expected))
        except Exception:
            return 0.5


class EmailEnvRubric(RubricDict):
    def forward(self, action: EmailAction, observation: EmailObservation) -> float:
        task_name = str(observation.metadata.get("task", ""))
        if task_name in self:
            return self[task_name](action, observation)
        return 0.5


class EmailEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        super().__init__()
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.task_index = 0
        self.current_task = None

        # ✅ FIXED rubric mapping
        rubrics = {}
        for task in TASKS:
            rubrics[str(task["name"])] = TaskGrader(task["grader"], task["expected"])

        self.rubric = EmailEnvRubric(rubrics)

    def reset(self, seed=None, episode_id=None, **kwargs) -> EmailObservation:
        super()._reset_rubric()
        ep_id = str(episode_id) if episode_id else str(uuid4())
        self._state = State(episode_id=ep_id, step_count=0)

        self.current_task = TASKS[self.task_index % len(TASKS)]
        self.task_index += 1

        return EmailObservation(
            email_text=self.current_task["input"],
            reward=0.5,
            done=False,
            metadata={
                "task": str(self.current_task["name"]),
                "expected": self.current_task["expected"]
            }
        )

    def step(self, action: EmailAction, timeout_s=None, **kwargs) -> EmailObservation:
        self._state.step_count += 1

        expected = self.current_task["expected"]

        obs = EmailObservation(
            email_text=self.current_task["input"],
            reward=0.5,
            done=True,
            metadata={
                "task": str(self.current_task["name"]),
                "expected": expected,
                "predicted": action.action
            }
        )

        reward = self._apply_rubric(action, obs)

        # ✅ SAFE RANGE (never 0)
        reward = float(reward)
        if reward <= 0.0:
            reward = 0.2
        elif reward >= 1.0:
            reward = 0.9

        obs.reward = reward

        return obs

    @property
    def state(self) -> State:
        return self._state