from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/times_two/{number}")
def times_two(number: int):
    return {"result": number * 2}
