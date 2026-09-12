from fastapi import FastAPI

from app.routers import (
    audit_log_router,
    auth_router,
    chat_router,
    conversation_router,
    document_router,
    memory_router,
    message_router,
    planner_task_router,
    user_preference_router,
    user_router,
)

app = FastAPI(
    title="AI Concierge API",
)

app.include_router(user_router.router)
app.include_router(user_preference_router.router)
app.include_router(conversation_router.router)
app.include_router(message_router.router)
app.include_router(memory_router.router)
app.include_router(document_router.router)
app.include_router(planner_task_router.router)
app.include_router(audit_log_router.router)
app.include_router(auth_router.router)
app.include_router(chat_router.router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}