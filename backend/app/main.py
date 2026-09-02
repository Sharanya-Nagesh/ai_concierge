from fastapi import FastAPI

from app.routers.user_router import router as user_router
from app.routers.user_preference_router import (
    router as user_preference_router,
)
from app.routers.conversation_router import (
    router as conversation_router,
)
from app.routers.message_router import router as message_router
from app.routers.memory_router import router as memory_router
from app.routers.document_router import router as document_router
from app.routers.planner_task_router import (
    router as planner_task_router,
)
from app.routers.audit_log_router import (
    router as audit_log_router,
)
from app.routers.auth_router import router as auth_router

app = FastAPI(
    title="AI Concierge API",
)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(user_router)
app.include_router(user_preference_router)
app.include_router(conversation_router)
app.include_router(message_router)
app.include_router(memory_router)
app.include_router(document_router)
app.include_router(planner_task_router)
app.include_router(audit_log_router)
app.include_router(auth_router)