from fastapi import FastAPI, Request, Response, HTTPException, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import logging
import json
import os
from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.routes import experiments, deploy, monitor, governance
from fastapi.responses import FileResponse

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Phoenix MLOps Platform",
    description="MLOps platform for managing ML workflows",
    version="1.0.0"
)
# Debug: Print current working directory
print("Current working directory:", os.getcwd())

# Debug: Check if template directory exists
template_dir = "app/templates"
print(f"Template directory exists: {os.path.exists(template_dir)}")

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates with debug info
templates = Jinja2Templates(directory=template_dir)

# Include the experiments router with the correct prefix
app.include_router(
    experiments.router,
    prefix="/api/v1",
    tags=["experiments"]
)

# Add Pydantic model for notebook creation
class NotebookCreate(BaseModel):
    name: str
    template: str
    environment: str
    region: str
    framework: str
    description: Optional[str] = None
    
    # Add validation
    from pydantic import validator
    
    @validator('name')
    def validate_name(cls, v):
        if not v.isalnum() and not '_' in v:
            raise ValueError('Name must be alphanumeric with optional underscores')
        return v

# Routes for each section
@app.get("/{section}")
async def section_page(request: Request, section: str):
    """
    Handle routing for different sections of the application.
    """
    logger.debug(f"Accessing section: {section}")
    try:
        # Return the specific section template if it exists
        return templates.TemplateResponse(
            f"pages/{section}/index.html",
            {"request": request, "section": section}
        )
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        # Fallback to base template if section template doesn't exist
        return templates.TemplateResponse(
            "layouts/base.html",
            {
                "request": request, 
                "section": section,
                "now": datetime.now
            }
        )

# Root route redirects to develop
@app.get("/")
async def root(request: Request):
    """
    Root path handler - redirects to development workspace.
    """
    logger.debug("Accessing root path")
    try:
        return templates.TemplateResponse(
            "pages/develop/index.html",
            {"request": request, "section": "develop"}
        )
    except Exception as e:
        logger.error(f"Error rendering template: {str(e)}")
        raise

@app.get("/test")
async def test():
    """
    Test endpoint to verify API functionality.
    """
    return {"message": "API is working"}

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    """
    Serve favicon from static directory
    """
    return FileResponse(
        os.path.join("static", "assets", "favicon.ico"),
        media_type="image/x-icon"
    )

@app.post("/api/notebooks")
async def create_notebook(notebook: NotebookCreate):
    try:
        # Create notebooks directory if it doesn't exist
        notebooks_dir = Path("notebooks")
        notebooks_dir.mkdir(exist_ok=True)
        
        # Create project directory with notebook name
        project_dir = notebooks_dir / notebook.name
        project_dir.mkdir(exist_ok=True)
        
        # Get template content
        template_path = Path("app/notebook_templates") / f"{notebook.template}.ipynb"
        if template_path.exists():
            with open(template_path, "r") as f:
                template_content = json.load(f)
        else:
            # Use basic template if template doesn't exist
            template_content = {
                "cells": [],
                "metadata": {
                    "kernelspec": {
                        "display_name": "Python 3",
                        "language": "python",
                        "name": "python3"
                    }
                }
            }

        # Add notebook metadata
        template_content["metadata"]["notebook_info"] = {
            "created_at": datetime.now().isoformat(),
            "template": notebook.template,
            "environment": notebook.environment,
            "region": notebook.region,
            "framework": notebook.framework,
            "description": notebook.description
        }

        # Save notebook file
        notebook_path = project_dir / "notebook.ipynb"
        with open(notebook_path, "w") as f:
            json.dump(template_content, f, indent=2)

        # Create notebook metadata file
        metadata_path = project_dir / "metadata.json"
        metadata = {
            "name": notebook.name,
            "created_at": datetime.now().isoformat(),
            "template": notebook.template,
            "environment": notebook.environment,
            "region": notebook.region,
            "framework": notebook.framework,
            "description": notebook.description,
            "status": "created"
        }
        with open(metadata_path, "w") as f:
            json.dump(metadata, f, indent=2)

        return {"status": "success", "message": f"Notebook {notebook.name} created successfully"}
    
    except Exception as e:
        logger.error(f"Error creating notebook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

async def get_notebooks_dir():
    dir = Path("notebooks")
    dir.mkdir(exist_ok=True)
    return dir

@app.get("/api/notebooks")
async def list_notebooks(notebooks_dir: Path = Depends(get_notebooks_dir)):
    try:
        notebooks = []
        if notebooks_dir.exists():
            for project_dir in notebooks_dir.iterdir():
                if project_dir.is_dir():
                    metadata_path = project_dir / "metadata.json"
                    if metadata_path.exists():
                        with open(metadata_path, "r") as f:
                            metadata = json.load(f)
                            notebooks.append(metadata)
        
        return {"notebooks": notebooks}
    
    except Exception as e:
        logger.error(f"Error listing notebooks: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get('/experiments')
async def experiments_page(request: Request):
    """
    Handle experiments page routing
    """
    return templates.TemplateResponse(
        "pages/experiment/index.html",
        {"request": request, "section": "experiments"}
    )

# Define these as constants at the top of the file
NOTEBOOKS_DIR = Path("notebooks")
TEMPLATES_DIR = Path("app/notebook_templates")

# Add new route - this is the only addition
@app.get("/experiment-details/{experiment_id}")
async def experiment_details_page(request: Request, experiment_id: str):
    logger.debug(f"Accessing experiment details for ID: {experiment_id}")
    try:
        return templates.TemplateResponse(
            "pages/experiment/details.html",
            {
                "request": request, 
                "experiment_id": experiment_id,
                "section": "experiments"  # Keep consistent with existing section handling
            }
        )
    except Exception as e:
        logger.error(f"Error rendering experiment details: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

app.include_router(
    deploy.router,
    prefix="/deploy",
    tags=["deploy"]
)
app.include_router(
    monitor.router,
    prefix="/monitor",
    tags=["monitor"]
)
app.include_router(
    governance.router,
    prefix="/governance",
    tags=["governance"]
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")

