# from uuid import uuid4

# from openenv.core.env_server.interfaces import Environment
# from openenv.core.env_server.types import State

# from models import EmailObservation, EmailAction


# class EmailEnvironment(Environment):

#     SUPPORTS_CONCURRENT_SESSIONS = True

#     def __init__(self):
#         self._state = State(episode_id=str(uuid4()), step_count=0)

#         # ✅ 3 FIXED TASKS (VERY IMPORTANT)
#         self.tasks = [
#             ("Win a FREE iPhone now!!!", "spam"),
#             ("Meeting at 5 PM today", "urgent"),
#             ("Lunch tomorrow?", "normal"),
#         ]

#         self.current = None
#         self.done = False
#         self.task_index = 0  # track task progression

#     def reset(self) -> EmailObservation:
#         self._state = State(episode_id=str(uuid4()), step_count=0)

#         # ✅ cycle through tasks (NOT random)
#         self.current = self.tasks[self.task_index % len(self.tasks)]
#         self.task_index += 1

#         self.done = False

#         return EmailObservation(
#             email_text=self.current[0],
#             reward=0.1,  # ⚠️ must NOT be 0
#             done=False,
#             metadata={
#                 "correct_label": self.current[1],
#                 "task_id": self.task_index
#             }
#         )

#     def step(self, action: EmailAction) -> EmailObservation:
#         self._state.step_count += 1

#         correct = self.current[1]

#         # ✅ VALID REWARD RANGE (0 < reward < 1)
#         if action.action == correct:
#             reward = 0.9
#         elif action.action in ["spam", "urgent", "normal"]:
#             reward = 0.5
#         else:
#             reward = 0.1

#         self.done = True

#         return EmailObservation(
#             email_text=self.current[0],
#             reward=reward,
#             done=True,
#             metadata={
#                 "correct_label": correct,
#                 "predicted": action.action,
#                 "task_id": self.task_index
#             }
#         )

#     @property
#     def state(self) -> State:
#         return self._state

from uuid import uuid4

from openenv.core.env_server.interfaces import Environment
from openenv.core.env_server.types import State

from models import EmailObservation, EmailAction
from tasks import TASKS


class EmailEnvironment(Environment):

    SUPPORTS_CONCURRENT_SESSIONS = True

    def __init__(self):
        self._state = State(episode_id=str(uuid4()), step_count=0)
        self.task_keys = list(TASKS.keys())
        self.current_task = None

    def reset(self) -> EmailObservation:
        self._state = State(episode_id=str(uuid4()), step_count=0)

        # pick task sequentially
        task_name = self.task_keys[self._state.step_count % len(self.task_keys)]
        self.current_task = TASKS[task_name]
        self.current_task_name = task_name

        return EmailObservation(
            email_text=self.current_task["input"],
            reward=0.1,
            done=False,
            metadata={
                "task": task_name,
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
                "task": self.current_task_name,
                "expected": expected,
                "predicted": action.action
            }
        )

    @property
    def state(self) -> State:
        return self._state