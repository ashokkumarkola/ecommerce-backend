from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": f"Welcome to Ecommerce Backend API!"}