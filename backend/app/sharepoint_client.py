import msal
import requests
from app.config import settings

def get_graph_token():
    if not settings.AZURE_CLIENT_ID or not settings.AZURE_CLIENT_SECRET:
        return None
    app = msal.ConfidentialClientApplication(
        settings.AZURE_CLIENT_ID,
        authority=f"https://login.microsoftonline.com/{settings.AZURE_TENANT_ID}",
        client_credential=settings.AZURE_CLIENT_SECRET
    )
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return result.get("access_token")

def sync_booking_to_sharepoint(booking):
    token = get_graph_token()
    if not token or not settings.SHAREPOINT_SITE_ID or not settings.SHAREPOINT_LIST_ID:
        print(f"[SHAREPOINT MOCK] Record logged locally for Ref: {booking.booking_reference}")
        return None

    url = f"https://graph.microsoft.com/v1.0/sites/{settings.SHAREPOINT_SITE_ID}/lists/{settings.SHAREPOINT_LIST_ID}/items"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "fields": {
            "Title": booking.faculty_name,
            "FacultyEmail": booking.email,
            "Venue": booking.venue,
            "Department": booking.department,
            "EventDetails": booking.event_details,
            "StartDateTime": booking.start_datetime.isoformat(),
            "EndDateTime": booking.end_datetime.isoformat(),
            "BookingStatus": booking.status,
            "ReferenceID": booking.booking_reference
        }
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 201:
            return response.json().get("id")
    except Exception as e:
        print(f"[SHAREPOINT SYNC ERROR]: {e}")
    return None