from fastapi import FastAPI

app = FastAPI(
    title="AI Concierge",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "AI Concierge API"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }
