from fastapi import FastAPI

app = FastAPI(title="TenantCore")

@app.get("/health")
def health_check():
    return {"status": "ok"}

