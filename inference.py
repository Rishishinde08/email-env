import os
from openai import OpenAI
from server.email_env_environment import EmailEnvironment
from models import EmailAction

client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

env = EmailEnvironment()

tasks = [
    ("easy_spam_detection", "spam"),
    ("medium_classification", "urgent"),
    ("hard_classification", "normal")
]

print(f"[START] task=multi env=email_env model={MODEL_NAME}")

step_count = 0
rewards = []

for task_name, expected in tasks:
    obs = env.reset()

    prompt = f"Classify this email: {obs.email_text} (spam/urgent/normal)"

    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    action_text = response.choices[0].message.content.strip().lower()
    action = EmailAction(action=action_text)

    obs = env.step(action)

    reward = obs.reward
    done = obs.done

    step_count += 1
    rewards.append(reward)

    print(f"[STEP] step={step_count} action={action_text} reward={reward:.2f} done={str(done).lower()} error=null")

# average score
score = sum(rewards) / len(rewards)

print(f"[END] success=true steps={step_count} score={score:.2f} rewards={','.join([str(round(r,2)) for r in rewards])}")