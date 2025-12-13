from fastapi import FastAPI, Request
from play import play
from models import LevelData  # Import LevelData from models

app = FastAPI()


@app.post("/")
async def post(request: LevelData):
    return play(request)


# Run the application with uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=3000)
