Inside activated venv
1. Make migration 
` alembic revision --autogenerate --message "message"`
2. Rollout changes `alembic upgrade head`