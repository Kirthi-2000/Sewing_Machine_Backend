# myapp/tasks.py
from celery import shared_task
from .models import MachineLog, DuplicateLog
from django.utils.dateparse import parse_time

@shared_task
def process_machine_data(data):
    """
    Process the machine data asynchronously.
    """
    # Validate mode
    try:
        mode = int(data.get("mode"))  # Convert mode to integer
    except (TypeError, ValueError):
        return {"status": "error", "message": "Invalid mode format"}

    MODES = {
        1: "Sewing - Machine is On - Production",
        2: "Logout - Off - Idle",
        3: "No Garment - Off - Non-Production",
        4: "Meeting - Off - Non-Production",
        5: "Maintenance - On - Non-Production",
    }

    if mode not in MODES:
        return {"status": "error", "message": "Invalid mode"}

    # Validate login time
    login_time = parse_time(data.get("login_time"))
    start_time = parse_time(data.get("start_time"))
    if login_time and start_time and login_time > start_time:
        return {"status": "error", "message": "Login time must be before start time"}

    # Check for duplicate
    if MachineLog.objects.filter(**data).exists():
        DuplicateLog.objects.create(payload=data)
        return {"status": "duplicate", "message": "Duplicate entry found"}

    # Save log
    try:
        machine_log = MachineLog.objects.create(**data)
        return {"status": "success", "message": "Log saved successfully"}
    except Exception as e:
        return {"status": "error", "message": f"Error saving log: {str(e)}"}
