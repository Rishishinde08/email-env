# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

"""
FastAPI application for the Email Env Environment.
"""

from openenv.core.env_server.http_server import create_app

# 🔥 Safe imports (works locally + docker)
try:
    from models import EmailAction, EmailObservation
    from .email_env_environment import EmailEnvironment
except ImportError:
    from models import EmailAction, EmailObservation
    from server.email_env_environment import EmailEnvironment


# 🔥 OpenEnv compatible app (VERY IMPORTANT)
app = create_app(
    EmailEnvironment,
    EmailAction,
    EmailObservation,
    env_name="email_env",
    max_concurrent_envs=1,
)


# 🔥 optional local run support
def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()