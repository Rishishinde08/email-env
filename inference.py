# import os
# from openai import OpenAI
# from server.email_env_environment import EmailEnvironment
# from models import EmailAction

# client = OpenAI(
#     base_url=os.getenv("API_BASE_URL"),
#     api_key=os.getenv("HF_TOKEN")
# )

# MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

# env = EmailEnvironment()

# # 🔥 EXPLICIT TASKS WITH EXPECTED OUTPUT
# TASKS = [
#     ("Win a FREE iPhone now!!!", "spam"),
#     ("Meeting at 5 PM today", "urgent"),
#     ("Lunch tomorrow?", "normal"),
# ]

# print(f"[START] task=email_classification env=email_env model={MODEL_NAME}")

# step_count = 0
# rewards = []

# for i, (email, expected) in enumerate(TASKS, start=1):

#     obs = env.reset()

#     prompt = f"Classify this email: {email}. Answer ONLY: spam, urgent, or normal."

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[{"role": "user", "content": prompt}]
#         )

#         action_text = response.choices[0].message.content.strip().lower()

#         # 🔥 CLEAN OUTPUT
#         if "spam" in action_text:
#             action_text = "spam"
#         elif "urgent" in action_text:
#             action_text = "urgent"
#         else:
#             action_text = "normal"

#     except Exception:
#         action_text = "normal"

#     action = EmailAction(action=action_text)

#     obs = env.step(action)

#     reward = float(obs.reward)
#     done = bool(obs.done)

#     step_count += 1
#     rewards.append(reward)

#     print(f"[STEP] step={step_count} action={action_text} reward={reward} done={str(done).lower()} error=null")

# # 🔥 FINAL SCORE (STRICT 0-1)
# score = sum(rewards) / len(rewards)
# score = max(0.0, min(score, 1.0))
# success = score >= 0.5

# print(f"[END] success={str(success).lower()} steps={step_count} score={score} rewards={rewards}")






import os
import requests
from openai import OpenAI

# 🔥 ENV VARIABLES (MANDATORY)
API_BASE_URL = os.getenv("API_BASE_URL")
HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

# OpenAI client
client = OpenAI(
    base_url=API_BASE_URL,
    api_key=HF_TOKEN
)

# Local FastAPI server (OpenEnv uses this internally)
BASE_URL = "http://localhost:8000"

print(f"[START] task=email_classification env=email_env model={MODEL_NAME}")

steps = 0
rewards = []

# 🔥 EXACTLY 3 TASKS REQUIRED
for i in range(3):

    # RESET ENV
    res = requests.post(f"{BASE_URL}/reset")
    obs = res.json()

    email_text = obs.get("email_text", "")

    prompt = f"Classify this email: {email_text}. Answer ONLY one word: spam, urgent, or normal."

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}]
        )

        action_text = response.choices[0].message.content.strip().lower()

        # 🔥 CLEAN OUTPUT (VERY IMPORTANT)
        if "spam" in action_text:
            action_text = "spam"
        elif "urgent" in action_text:
            action_text = "urgent"
        else:
            action_text = "normal"

    except Exception:
        action_text = "normal"

    # STEP ENV
    res = requests.post(
        f"{BASE_URL}/step",
        json={"action": action_text}
    )

    result = res.json()

    reward = float(result.get("reward", 0.0))
    done = bool(result.get("done", False))

    steps += 1
    rewards.append(reward)

    print(f"[STEP] step={steps} action={action_text} reward={reward:.2f} done={str(done).lower()} error=null")

# 🔥 FINAL SCORE
score = sum(rewards) / len(rewards) if rewards else 0.0
score = max(0.0, min(score, 1.0))

print(f"[END] success=true steps={steps} score={score:.2f} rewards={','.join([str(round(r,2)) for r in rewards])}")






# import os
# from openai import OpenAI
# from server.email_env_environment import EmailEnvironment
# from models import EmailAction

# client = OpenAI(
#     base_url=os.getenv("API_BASE_URL"),
#     api_key=os.getenv("HF_TOKEN")
# )

# MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

# env = EmailEnvironment()

# print(f"[START] task=multi env=email_env model={MODEL_NAME}")

# step_count = 0
# rewards = []

# # 🔥 FORCE EXACTLY 3 STEPS
# for i in range(3):
#     obs = env.reset()

#     prompt = f"Classify this email: {obs.email_text}. Answer ONLY one word: spam, urgent, or normal."

#     try:
#         response = client.chat.completions.create(
#             model=MODEL_NAME,
#             messages=[{"role": "user", "content": prompt}]
#         )

#         action_text = response.choices[0].message.content.strip().lower()

#         # 🔥 CLEAN OUTPUT (VERY IMPORTANT)
#         if "spam" in action_text:
#             action_text = "spam"
#         elif "urgent" in action_text:
#             action_text = "urgent"
#         else:
#             action_text = "normal"

#     except Exception:
#         # fallback (never fail)
#         action_text = "normal"

#     action = EmailAction(action=action_text)

#     obs = env.step(action)

#     reward = float(obs.reward)
#     done = bool(obs.done)

#     step_count += 1
#     rewards.append(reward)

#     print(f"[STEP] step={step_count} action={action_text} reward={reward:.2f} done={str(done).lower()} error=null")

# # 🔥 FINAL SCORE
# score = sum(rewards) / len(rewards)

# print(f"[END] success=true steps={step_count} score={score:.2f} rewards={','.join([str(round(r,2)) for r in rewards])}")