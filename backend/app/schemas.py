"""
schemas.py
----------
This file defines the "shape" of the data that flows in and out of our API.

We use Pydantic models for this. Pydantic automatically validates incoming
JSON data against these rules, and returns a clear error message if
something doesn't match (e.g. age is negative, or gender is not "male").

Think of this file as a contract between the frontend and the backend.
"""

from enum import Enum
from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums restrict a field to a fixed set of valid choices.
# If the frontend sends anything outside of these values, FastAPI will
# automatically reject the request with a helpful error message.
# ---------------------------------------------------------------------------

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class ActivityLevel(str, Enum):
    SEDENTARY = "sedentary"
    LIGHTLY_ACTIVE = "lightly_active"
    MODERATELY_ACTIVE = "moderately_active"
    VERY_ACTIVE = "very_active"
    EXTREMELY_ACTIVE = "extremely_active"


class Goal(str, Enum):
    CUT = "cut"
    MAINTENANCE = "maintenance"
    LEAN_BULK = "lean_bulk"
    BULK = "bulk"


# ---------------------------------------------------------------------------
# Request model: what the frontend must send us in the POST body.
# ---------------------------------------------------------------------------

class UserInput(BaseModel):
    # Field(...) means the value is required.
    # gt / ge / le enforce sensible real-world limits so the math never
    # produces nonsense results (e.g. negative calories).
    age: int = Field(..., gt=0, le=120, description="Age in years (1-120)")
    gender: Gender = Field(..., description="Biological sex used for the BMR formula")
    height_cm: float = Field(..., gt=50, le=272, description="Height in centimetres")
    weight_kg: float = Field(..., gt=20, le=400, description="Weight in kilograms")
    activity_level: ActivityLevel = Field(..., description="Weekly activity level")
    goal: Goal = Field(..., description="Fitness goal")

    class Config:
        json_schema_extra = {
            "example": {
                "age": 25,
                "gender": "male",
                "height_cm": 178,
                "weight_kg": 75,
                "activity_level": "moderately_active",
                "goal": "maintenance",
            }
        }


# ---------------------------------------------------------------------------
# Response sub-models: these describe each "card" of the results dashboard.
# Splitting the response into small models keeps main.py easy to read.
# ---------------------------------------------------------------------------

class BMIResult(BaseModel):
    value: float
    category: str


class MacroGrams(BaseModel):
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float


class MealPlan(BaseModel):
    breakfast: MacroGrams
    lunch: MacroGrams
    dinner: MacroGrams
    snacks: MacroGrams


class WeightRange(BaseModel):
    min_kg: float
    max_kg: float


class NutritionResult(BaseModel):
    bmi: BMIResult
    bmr: float
    tdee: float
    goal_calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    water_liters: float
    healthy_weight_range: WeightRange
    meal_plan: MealPlan
