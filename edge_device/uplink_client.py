import requests

SERVER_URL = "http://localhost:8000/api/events"


def send_event(event):
    """Send event to the backend server"""
    files = None

    if event.get("image"):
        files = {
            "image": open(event["image"], "rb")
        }

    data = {
        "camera_id": event["camera_id"],
        "timestamp": event["timestamp"],
        "type": event["type"],
        "count": event["count"]
    }

    try:
        r = requests.post(SERVER_URL, data=data, files=files)

        if r.status_code == 200:
            print("Event uploaded successfully:", r.status_code)
        else:
            print("Upload failed with status:", r.status_code)

    except Exception as e:
        print("Upload failed:", e)

