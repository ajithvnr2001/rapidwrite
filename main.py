from crewai import Agent, Task, Crew, Process
from core.glpi import GLPIClient
from agents.data_extractor import DataExtractorAgent

# Initialize the GLPI client
glpi_client = GLPIClient()

# Initialize the DataExtractorAgent
data_extractor_agent = DataExtractorAgent(glpi_client=glpi_client)

# Define a single task to fetch incident details
extract_incident_task = Task(
    description="Fetch details for incident ID 123",  # Hardcoded for simplicity
    agent=data_extractor_agent,
    expected_output="Raw data of the incident"
)

# Create a crew with just the one agent and task
crew = Crew(
    agents=[data_extractor_agent],
    tasks=[extract_incident_task],
    process=Process.sequential,
    verbose=2
)

# Run the crew and print the result
result = crew.kickoff()
print(result)

glpi_client.close_session()
