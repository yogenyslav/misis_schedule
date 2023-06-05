from app.loader import create_app
import uvicorn

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        reload=True,
        use_colors=True,
        host="0.0.0.0",
    )
