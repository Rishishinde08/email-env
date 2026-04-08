import os
from openai import OpenAI
from server.email_env_environment import EmailEnvironment
env = EmailEnvironment()
from models import EmailAction



client = OpenAI(
    base_url=os.getenv("API_BASE_URL"),
    api_key=os.getenv("HF_TOKEN")
)

MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")

env = EmailEnv()

print(f"[START] task=email env=email_env model={MODEL_NAME}")

obs = env.reset()

prompt = f"Classify this email: {obs.email_text} (spam/urgent/normal)"

response = client.chat.completions.create(
    model=MODEL_NAME,
    messages=[{"role": "user", "content": prompt}]
)

action_text = response.choices[0].message.content.strip().lower()

action = EmailAction(action=action_text)

obs, reward, done, _ = env.step(action)

print(f"[STEP] step=1 action={action_text} reward={reward:.2f} done={str(done).lower()} error=null")
print(f"[END] success=true steps=1 score={reward:.2f} rewards={reward:.2f}")

