from fastapi import FastAPI

app = FastAPI(
    title="Hevy AI Coach API",
    description="API que conecta o ChatGPT ao Hevy AI Coach.",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "status": "online",
        "message": "Hevy AI Coach API funcionando!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }