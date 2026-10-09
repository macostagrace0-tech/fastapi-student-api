from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(
    title="Student Item API",
    description="Learning FastAPI step by step",
    version="1.0.0",
)

class ItemCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    description: str | None = None
    price: float = Field(gt=0)
    is_active: bool = True

class ItemRead(ItemCreate):
    id: int


@app.get("/")
def root():
    return {"message": "FastAPI is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/items/{item_id}")
def get_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items")
def list_items(limit: int = 10, active: bool = True):
    return {"limit": limit, "active": active}

@app.post("/items", response_model=ItemRead, status_code=201)
def create_item(item: ItemCreate):
    return {"id": 1, **item.model_dump()}


@app.patch("/items/{item_id}")
def update_item(item_id: int):
    return {"message": "update", "item_id": item_id}


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    return {"message": "delete", "item_id": item_id}

@app.get("/demo/{item_id}")
def demo(item_id: int):
    if item_id != 1:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": 1}