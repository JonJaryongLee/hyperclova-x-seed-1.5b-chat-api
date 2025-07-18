import uvicorn
from app.api import app

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        workers=1,
        proxy_headers=True,
        log_level="info"
    )
