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
    # Sports activities
    "Soccer Team": {
        "description": "Join the school soccer team and compete in local leagues",
        "schedule": "Wednesdays and Fridays, 4:00 PM - 5:30 PM",
        "max_participants": 18,
        "participants": ["lucas@mergington.edu", "mia@mergington.edu"]
    },
    "Basketball Club": {
        "description": "Practice basketball skills and play friendly matches",
        "schedule": "Tuesdays, 5:00 PM - 6:30 PM",
        "max_participants": 15,
        "participants": ["liam@mergington.edu", "ava@mergington.edu"]
    },
    # Artistic activities
    "Drama Club": {
        "description": "Act in plays and participate in drama workshops",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 25,
        "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Workshop": {
        "description": "Explore painting, drawing, and sculpture techniques",
        "schedule": "Mondays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["amelia@mergington.edu", "benjamin@mergington.edu"]
    },
    # Intellectual activities
    "Math Olympiad": {
        "description": "Prepare for math competitions and solve challenging problems",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 16,
        "participants": ["charlotte@mergington.edu", "elijah@mergington.edu"]
    },
    "Science Club": {
        "description": "Conduct experiments and explore scientific concepts",
        "schedule": "Fridays, 2:00 PM - 3:30 PM",
        "max_participants": 22,
        "participants": ["jack@mergington.edu", "harper@mergington.edu"]
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
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
    
    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up")
    # Validate max participants not exceeded
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Maximum participants reached") 
    # Add student to participants
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}    
@app.get("/activities/{activity_name}")
def get_activity(activity_name: str):
    """Get details of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activities[activity_name]    

@app.get("/activities/{activity_name}/participants")
def get_activity_participants(activity_name: str):
    """Get participants of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activities[activity_name]["participants"]    
@app.get("/activities/{activity_name}/schedule")
def get_activity_schedule(activity_name: str):
    """Get schedule of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"schedule": activities[activity_name]["schedule"]}  
@app.get("/activities/{activity_name}/description")
def get_activity_description(activity_name: str):
    """Get description of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"description": activities[activity_name]["description"]}    
@app.get("/activities/{activity_name}/max_participants")
def get_activity_max_participants(activity_name: str):      
    """Get maximum participants of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"max_participants": activities[activity_name]["max_participants"]}
@app.get("/activities/{activity_name}/current_participants")
def get_activity_current_participants(activity_name: str):  
    """Get current participants of a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"current_participants": len(activities[activity_name]["participants"])} 
@app.get("/activities/{activity_name}/remaining_spots")                         

def get_activity_remaining_spots(activity_name: str):
    """Get remaining spots in a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    remaining_spots = activities[activity_name]["max_participants"] - len(activities[activity_name]["participants"])
    return {"remaining_spots": remaining_spots}
@app.get("/activities/{activity_name}/is_full")
def is_activity_full(activity_name: str):
    """Check if a specific activity is full"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    is_full = len(activities[activity_name]["participants"]) >= activities[activity_name]["max_participants"]
    return {"is_full": is_full} 
@app.get("/activities/{activity_name}/is_open")
def is_activity_open(activity_name: str):
    """Check if a specific activity is open for signups"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    is_open = len(activities[activity_name]["participants"]) < activities[activity_name]["max_participants"]
    return {"is_open": is_open}
@app.get("/activities/{activity_name}/is_participant")
def is_participant(activity_name: str, email: str):
    """Check if a student is a participant in a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    is_participant = email in activities[activity_name]["participants"]
    return {"is_participant": is_participant}
@app.get("/activities/{activity_name}/participant_count")
def get_participant_count(activity_name: str):
    """Get the count of participants in a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    participant_count = len(activities[activity_name]["participants"])
    return {"participant_count": participant_count}
@app.get("/activities/{activity_name}/participant_emails")
def get_participant_emails(activity_name: str):     
    """Get the emails of participants in a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails": activities[activity_name]["participants"]}
@app.get("/activities/{activity_name}/participant_details")
def get_participant_details(activity_name: str):
    """Get details of participants in a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_details": [{"email": email} for email in activities[activity_name]["participants"]]}
@app.get("/activities/{activity_name}/participant_emails_count")
def get_participant_emails_count(activity_name: str):               
    """Get the count of participant emails in a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_count": len(activities[activity_name]["participants"])}
@app.get("/activities/{activity_name}/participant_emails_list")
def get_participant_emails_list(activity_name: str):
    """Get a list of participant emails in a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_list": activities[activity_name]["participants"]}   
@app.get("/activities/{activity_name}/participant_emails_string") 
def get_participant_emails_string(activity_name: str):
    """Get a string of participant emails in a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_string": ", ".join(activities[activity_name]["participants"])}
@app.get("/activities/{activity_name}/participant_emails_json")       
def get_participant_emails_json(activity_name: str):
    """Get participant emails in JSON format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_json": activities[activity_name]["participants"]}
@app.get("/activities/{activity_name}/participant_emails_csv")
def get_participant_emails_csv(activity_name: str):
    """Get participant emails in CSV format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_csv": ",".join(activities[activity_name]["participants"])}
@app.get("/activities/{activity_name}/participant_emails_tsv")
def get_participant_emails_tsv(activity_name: str):     
    """Get participant emails in TSV format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_tsv": "\t".join(activities[activity_name]["participants"])}
@app.get("/activities/{activity_name}/participant_emails_html")
def get_participant_emails_html(activity_name: str):        
    """Get participant emails in HTML format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_html": "<br>".join(activities[activity_name]["participants"])}
@app.get("/activities/{activity_name}/participant_emails_xml") 
def get_participant_emails_xml(activity_name: str):
    """Get participant emails in XML format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    emails = activities[activity_name]["participants"]
    xml_data = "<participants>" + "".join(f"<email>{email}</email>" for email in emails) + "</participants>"
    return {"participant_emails_xml": xml_data} 
@app.get("/activities/{activity_name}/participant_emails_yaml")
def get_participant_emails_yaml(activity_name: str): 
    """Get participant emails in YAML format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    import yaml
    emails = activities[activity_name]["participants"]
    yaml_data = yaml.dump({"participants": emails})
    return {"participant_emails_yaml": yaml_data}   
@app.get("/activities/{activity_name}/participant_emails_markdown")
def get_participant_emails_markdown(activity_name: str):    
    """Get participant emails in Markdown format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    markdown_data = "\n".join(f"- {email}" for email in activities[activity_name]["participants"])
    return {"participant_emails_markdown": markdown_data} 
@app.get("/activities/{activity_name}/participant_emails_plaintext")
def get_participant_emails_plaintext(activity_name: str): 
    """Get participant emails in plaintext format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_plaintext": "\n".join(activities[activity_name]["participants"])}               
@app.get("/activities/{activity_name}/participant_emails_json_list")
def get_participant_emails_json_list(activity_name: str):
    """Get participant emails in JSON list format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_json_list": activities[activity_name]["participants"]}
@app.get("/activities/{activity_name}/participant_emails_json_object")
def get_participant_emails_json_object(activity_name: str):
    """Get participant emails in JSON object format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_json_object": {"emails": activities[activity_name]["participants"]}}
@app.get("/activities/{activity_name}/participant_emails_json_string")
def get_participant_emails_json_string(activity_name: str):
    """Get participant emails in JSON string format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_json_string": json.dumps(activities[activity_name]["participants"])}
@app.get("/activities/{activity_name}/participant_emails_json_array")
def get_participant_emails_json_array(activity_name: str):
    """Get participant emails in JSON array format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_json_array": activities[activity_name]["participants"]}
@app.get("/activities/{activity_name}/participant_emails_json_object_list")
def get_participant_emails_json_object_list(activity_name: str):
    """Get participant emails in JSON object list format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_json_object_list": [{"email": email} for email in activities[activity_name]["participants"]]}
@app.get("/activities/{activity_name}/participant_emails_json_object_array")
def get_participant_emails_json_object_array(activity_name: str):
    """Get participant emails in JSON object array format for a specific activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    return {"participant_emails_json_object_array": [{"email": email} for email in activities[activity_name]["participants"]]}
