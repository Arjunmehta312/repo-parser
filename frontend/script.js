document.getElementById("go-button").addEventListener("click", async () => {
    const repoLink = document.getElementById("repo-link").value;
    const filterType = document.getElementById("include-exclude").value;
    const filePattern = document.getElementById("file-pattern").value;
    const sizeLimit = document.getElementById("size-limit").value;

    if (!repoLink) {
        alert("Please enter a GitHub repository link.");
        return;
    }

    try {
        const response = await fetch(`/parse-repo?repo_url=${repoLink}&filter_type=${filterType}&file_pattern=${filePattern}&size_limit=${sizeLimit}`);
        if (!response.ok) throw new Error("Failed to fetch repository data.");
        
        const data = await response.json();

        // Populate Summary
        document.getElementById("repo-name").textContent = repoLink.split("/").slice(-2).join("/");
        document.getElementById("files-analyzed").textContent = data.files.length;
        document.getElementById("total-tokens").textContent = data.tokens;
        document.getElementById("total-characters").textContent = data.characters;

        // Populate Project Structure
        const structureBox = document.getElementById("project-structure");
        structureBox.textContent = data.files.map(f => `${f.name} (${f.size_kb.toFixed(2)} KB)`).join("\n");

        // Populate Repo Content
        const contentBox = document.getElementById("repo-content");
        contentBox.textContent = JSON.stringify(data, null, 2);
    } catch (error) {
        console.error(error);
        alert("An error occurred while parsing the repository.");
    }
});
