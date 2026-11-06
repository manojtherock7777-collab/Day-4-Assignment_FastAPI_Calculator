from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal

# 1. Initialize the FastAPI app instance
app = FastAPI(
    title="Simple Calculator API",
    description="A basic arithmetic calculator API built with FastAPI.",
    version="1.0.0"
)

# 2. Define the Pydantic schema for the POST requests
class CalculationRequest(BaseModel):
    num1: float = Field(..., description="The first number")
    num2: float = Field(..., description="The second number")
    operation: Literal["add", "subtract", "multiply", "divide"] = Field(
        ..., 
        description="The math operation to perform"
    )

# 3. Helper function to process the math logic
def perform_math(num1: float, num2: float, operation: str) -> float:
    if operation == "add":
        return num1 + num2
    elif operation == "subtract":
        return num1 - num2
    elif operation == "multiply":
        return num1 * num2
    elif operation == "divide":
        if num2 == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Division by zero is not allowed."
            )
        return num1 / num2
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid operation configuration."
        )

# --- Endpoints ---

@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint displaying API availability."""
    return {"message": "Welcome to the FastAPI Calculator API! Go to /docs to test it out."}

@app.post("/calculate", tags=["Calculator"])
def calculate_post(request: CalculationRequest):
    """
    Perform a calculation via POST payload.
    Valid operations: 'add', 'subtract', 'multiply', 'divide'.
    """
    result = perform_math(request.num1, request.num2, request.operation)
    return {
        "num1": request.num1,
        "num2": request.num2,
        "operation": request.operation,
        "result": result
    }

@app.get("/calculate", tags=["Calculator"])
def calculate_get(
    num1: float, 
    num2: float, 
    operation: Literal["add", "subtract", "multiply", "divide"]
):
    """
    Perform a calculation via GET query parameters.
    Example: `/calculate?num1=10&num2=5&operation=multiply`
    """
    result = perform_math(num1, num2, operation)
    return {
        "num1": num1,
        "num2": num2,
        "operation": operation,
        "result": result
    }
