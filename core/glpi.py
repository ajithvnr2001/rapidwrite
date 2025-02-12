import requests
from core.config import settings  # Ensure this is correctly set up

class GLPIClient:
    def __init__(self):
        self.base_url = settings.glpi_url
        self.app_token = settings.glpi_app_token
        self.user_token = settings.glpi_user_token
        self.session_token = None
        self.headers = {
            "Content-Type": "application/json",
            "App-Token": self.app_token,
        }
        self.init_session()

    def init_session(self):
        url = f"{self.base_url}/apirest.php/initSession"
        headers = self.headers.copy()
        headers["Authorization"] = f"user_token {self.user_token}"
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        self.session_token = response.json().get("session_token")
        self.headers["Session-Token"] = self.session_token
        print(f"GLPI session initialized. Session Token: {self.session_token}")

    def close_session(self):
        if self.session_token:
            url = f"{self.base_url}/apirest.php/killSession"
            requests.get(url, headers=self.headers, verify=False)
            self.session_token = None
            print("GLPI session closed.")

    def _make_request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url}/apirest.php/{endpoint}"
        response = requests.request(method, url, headers=self.headers, params=params, json=data, verify=False)
        response.raise_for_status()
        return response.json()

    def get_incident(self, incident_id):
        return self._make_request("GET", f"Ticket/{incident_id}", params={"expand_dropdowns": "true"})

    def get_ticket_solution(self, ticket_id):
        solutions = self._make_request("GET", f"Ticket/{ticket_id}/ITILSolution")
        return solutions[-1]["content"] if solutions else ""
    
    def close_session(self) -> None:
        if not self.session_token:
            return

        url = f"{self.base_url}/apirest.php/killSession"  # Correct endpoint
        try:
            response = requests.get(url, headers=self.headers, verify=False)
            response.raise_for_status()
            print("GLPI session closed.")
        except requests.exceptions.RequestException as e:
            print(f"Error closing GLPI session: {e}")
        finally:
            self.session_token = None
            self.headers.pop("Session-Token", None)
