from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse
import utils

app = FastAPI()

@app.get("/")
def root():
    return {"message": "GitHub Repository Parser API is running!"}

@app.get("/parse-repo")
async def parse_repo(
    repo_url: str = Query(..., description="GitHub repository URL"),
    filter_type: str = Query("include", description="Filter type: 'include' or 'exclude'"),
    file_pattern: str = Query(None, description="File pattern to include/exclude (e.g., '*.md')"),
    size_limit: int = Query(50, description="Maximum file size in KB"),
):
    try:
        repo_data = utils.parse_repository(repo_url, filter_type, file_pattern, size_limit)
        return JSONResponse(content=repo_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
