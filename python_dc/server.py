from fastapi import FastAPI
from routes.routes import app_nic

app = FastAPI(debug=True)

app.include_router(app_nic)