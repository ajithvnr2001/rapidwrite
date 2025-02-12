from crewai import Agent
from core.glpi import GLPIClient
from langchain.tools import tool
from typing import ClassVar, Any
from pydantic import ConfigDict

class DataExtractorAgent(Agent):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    get_glpi_incident_details: ClassVar[Any]
    glpi_client: GLPIClient

    def __init__(self, glpi_client: GLPIClient):
        super().__init__(
            role='Data Extractor',
            goal='Retrieve data from GLPI',
            backstory='An agent to extract data from GLPI.',
            tools=[self.get_glpi_incident_details],
            verbose=True,
            allow_delegation=False
        )
        self.glpi_client = glpi_client

    @tool
    def get_glpi_incident_details(self, incident_id: int) -> str:
        """Fetches details for a specific incident from GLPI."""
        try:
            incident = self.glpi_client.get_incident(incident_id)
            return str(incident)
        except Exception as e:
            print(f"Error in get_glpi_incident_details: {e}")
            return ""
