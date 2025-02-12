from crewai import Crew, Task, Process
from agents.data_extractor import DataExtractorAgent
from agents.data_processor import DataProcessorAgent
from agents.query_handler import QueryHandlerAgent
from agents.pdf_generator import PDFGeneratorAgent
from agents.search_indexer import SearchIndexerAgent
from core.glpi import GLPIClient
from core.config import settings
from typing import Dict
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
import json
from crewai import Crew, Task, Process
from agents.data_extractor import DataExtractorAgent
from agents.data_processor import DataProcessorAgent
from agents.query_handler import QueryHandlerAgent
from agents.pdf_generator import PDFGeneratorAgent
from agents.search_indexer import SearchIndexerAgent
from core.glpi import GLPIClient
from core.config import settings
from typing import Dict
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
import json
from crewai import Crew, Task, Process
from agents.data_extractor import DataExtractorAgent
from agents.data_processor import DataProcessorAgent
from agents.query_handler import QueryHandlerAgent
from agents.pdf_generator import PDFGeneratorAgent
from agents.search_indexer import SearchIndexerAgent
from core.glpi import GLPIClient
from core.config import settings
from typing import Dict
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
import json

from crewai import Crew, Task, Process
from agents.data_extractor import DataExtractorAgent
from agents.data_processor import DataProcessorAgent
from agents.query_handler import QueryHandlerAgent
from agents.pdf_generator import PDFGeneratorAgent
from agents.search_indexer import SearchIndexerAgent
from core.glpi import GLPIClient
from core.config import settings
from typing import Dict
from fastapi import FastAPI, Request, HTTPException
from datetime import datetime
import json
from crewai import Crew, Task, Process
from agents.data_extractor import DataExtractorAgent
from core.glpi import GLPIClient
from typing import Dict
from fastapi import FastAPI, Request, HTTPException  # Keep FastAPI for now
import json

app = FastAPI()

# Initialize GLPI client OUTSIDE the function
glpi_client = GLPIClient()

# Initialize ONLY the DataExtractorAgent, passing glpi_client.
data_extractor_agent = DataExtractorAgent(glpi_client=glpi_client)


def run_autopdf(incident_id: int = 123) -> None:  # Simplified for testing
    """Runs a simplified workflow with just the data extraction."""

    extract_incident_task = Task(
        description=f"Extract details for GLPI incident ID {incident_id}",
        agent=data_extractor_agent,
        expected_output="Raw data of the incident",
    )

    crew = Crew(
        agents=[data_extractor_agent],  # Only one agent
        tasks=[extract_incident_task],  # Only one task
        process=Process.sequential,
        verbose=2,
    )

    result = crew.kickoff()
    print(result)  # Print the result for verification


@app.post("/webhook")  # Keep the webhook for testing
async def glpi_webhook(request: Request):
    """Handles incoming webhooks from GLPI (simplified)."""
    try:
        body = await request.body()
        data = json.loads(body.decode())
        if not isinstance(data, list):
            raise HTTPException(status_code=400, detail="Invalid webhook payload format")
        for event in data:
            if 'event' not in event or 'itemtype' not in event or 'items_id' not in event:
                raise HTTPException(status_code=400, detail="Missing required fields in event")
            if event['itemtype'] == 'Ticket':
                incident_id = int(event['items_id'])
                if event['event'] in ('add', 'update'):
                    print("*"*50)
                    print(f"Received event: {event['event']} for Ticket ID: {incident_id}")
                    print("*"*50)
                    run_autopdf(incident_id)  # Call with a default incident ID
                else:
                    print(f"Ignoring event type: {event['event']} for Ticket")

        return {"message": "Webhook received and processed"}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON payload")
    except Exception as e:
        print(f"Error in webhook: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")


@app.get("/")
async def root():
    return {"message": "AutoPDF is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port="8000")
