import requests
import re

def parse_repository(repo_url, filter_type, file_pattern, size_limit):
    # Validate URL
    if not re.match(r"https://github.com/.+/.+", repo_url):
        raise ValueError("Invalid GitHub repository URL.")
    
    # Extract repository owner and name
    try:
        owner, repo = repo_url.replace("https://github.com/", "").split("/", 1)
    except ValueError:
        raise ValueError("Invalid repository URL format.")
    
    # GitHub API URL
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
    
    # Fetch repository contents
    response = requests.get(api_url)
    if response.status_code != 200:
        raise Exception("Error fetching repository contents. Check if the repo is public.")
    
    repo_content = response.json()
    parsed_data = {"files": [], "tokens": 0, "characters": 0}
    
    for file in repo_content:
        # Skip if size exceeds limit
        if file["size"] > size_limit * 1024:
            continue
        
        # Apply file pattern filtering
        if filter_type == "include" and file_pattern and not re.match(file_pattern, file["name"]):
            continue
        if filter_type == "exclude" and file_pattern and re.match(file_pattern, file["name"]):
            continue
        
        # Add file details
        parsed_data["files"].append({
            "name": file["name"],
            "path": file["path"],
            "size_kb": file["size"] / 1024
        })
        parsed_data["characters"] += file["size"]
    
    parsed_data["tokens"] = parsed_data["characters"] // 4  # Estimate tokens
    return parsed_data
