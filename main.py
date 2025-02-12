from crewai import Crew, Task, Process
from agents.data_extractor import DataExtractorAgent
from core.glpi import GLPIClient

# Initialize GLPI client
glpi_client = GLPIClient()

# Initialize the DataExtractorAgent
data_extractor_agent = DataExtractorAgent(glpi_client=glpi_client)

# Define a single task
extract_incident_task = Task(
    description="Extract details for GLPI incident ID 123",  # HARDCODE A VALID ID
    agent=data_extractor_agent,
    expected_output="Raw data of the incident",
)

# Create a crew with just the one agent and task
crew = Crew(
    agents=[data_extractor_agent],
    tasks=[extract_incident_task],
    process=Process.sequential,
    verbose=2,  # Keep verbose logging
)

# Run the crew
result = crew.kickoff()
print(result)

# Close GLPI session (important to do this, even in the minimal example)
glpi_client.close_session()
