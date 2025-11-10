"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    # Sports-related activities (2)
    "Soccer Team": {
        "description": "Competitive soccer team practice and matches",
        "schedule": "Mondays and Thursdays, 4:00 PM - 6:00 PM",
        "max_participants": 22,
        "participants": ["alex@mergington.edu", "harper@mergington.edu"]
    },
    "Track and Field": {
        "description": "Running, jumping and throwing events training",
        "schedule": "Tuesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    # Artistic activities (2)
    "Drama Club": {
        "description": "Acting, stagecraft and school productions",
        "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
        "max_participants": 30,
        "participants": ["nora@mergington.edu", "jack@mergington.edu"]
    },
    "Art Studio": {
        "description": "Drawing, painting and mixed-media workshops",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 18,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    # Intellectual activities (2)
    "Debate Team": {
        "description": "Competitive debating and public speaking practice",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 16,
        "participants": ["sophia_r@mergington.edu", "noah@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and science fair project support",
        "schedule": "Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["isabella@mergington.edu", "ethan@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
   
    # Get the specific activity
    activity = activities[activity_name]
    # Normalize and validate student is not already signed up
    email = email.strip().lower()
    if any(email == p.strip().lower() for p in activity["participants"]):
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")
     # Validate student is not already signed up
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full") 
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
