from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Configure CORS
# For development, you might allow all origins or specific development origins.
# In production, specify your Next.js frontend's domain(s).
origins = [
    "http://localhost:3000",  # Your Next.js frontend development server
    "http://127.0.0.1:3000",
    # Add your production frontend URL(s) here later, e.g., "https://your-nextjs-app.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"], # Allows all headers
)

# Pydantic model for incoming data (for /api/process)
class Item(BaseModel):
    input: str

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI Backend!"}

@app.get("/api/data")
async def get_data():
    """
    Example: Return some data from the backend.
    """
    data = {
        "message": "Data from FastAPI backend!",
        "timestamp": "2025-06-30T16:41:52Z" # Replace with actual dynamic timestamp
    }
    return data

@app.post("/api/process")
async def process_data(item: Item):
    """
    Example: Receive data from frontend, process it, and send a response.
    FastAPI automatically validates the incoming JSON against the Item model.
    """
    processed_message = f"Received: '{item.input}' and processed by FastAPI!"
    return {"status": "success", "processed_message": processed_message}

# You can also include custom error handling or other routes as needed
@app.get("/api/items/{item_id}")
async def read_item(item_id: int):
    if item_id == 404:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id, "description": f"This is item number {item_id}"}


if __name__ == "__main__":
    # To run the app directly from this file for development
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
    # Note: 0.0.0.0 makes it accessible from other machines on the network if needed.
    # Use reload=True for development to auto-restart server on code changes.