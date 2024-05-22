# VertexAI-Semantic-Caching

Repository dedicated to enhancing data retrieval and processing efficiencies in Google Cloud's Vertex AI by implementing a semantic caching layer with MemoryStore, Vertex AI Vector Search, and Gemini, focusing on GenAI applications.


## Prerequisites 📋

Before getting started, ensure you have the following:

- Python 3.6 or later
- Git
- Google Cloud Platform account with a project set up and Vertex AI API enabled

Make sure you have permissions to create service accounts and manage API keys within your GCP project.

## Installation

Let's set up your local development environment and configure dependencies.

### Clone the Repository 📂

1. **Clone the Repository**: In your terminal, execute the following command:

   ```bash
   git clone https://github.com/arunpshankar/VertexAI-Document-Discovery.git
   cd VertexAI-Document-Discovery
   ```

### Set Up Your Environment 🛠️

2. **Create a Virtual Environment**: Isolate project dependencies by creating a Python virtual environment:

   - **For macOS/Linux**:

     ```bash
     python3 -m venv .VertexAI-Document-Discovery
     source .VertexAI-Document-Discovery/bin/activate
     ```

   - **For Windows**:

     ```bash
     python3 -m venv .VertexAI-Document-Discovery
     .VertexAI-Document-Discovery\Scripts\activate
     ```

3. **Upgrade pip and Install Dependencies**: Ensure pip is up-to-date and install project dependencies:

   ```bash
   python3 -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Update Your PYTHONPATH**:

   Ensure your Python interpreter recognizes the project directory as a module location.

   - **For macOS/Linux**:

     ```bash
     export PYTHONPATH=$PYTHONPATH:.
     ```

   - **For Windows** (use `set` instead of `export`):

     ```bash
     set PYTHONPATH=%PYTHONPATH%;.
     ```

5. **Configure Service Account Credentials** 🔑

   - Create a directory to store your Google Cloud service account key securely:

     ```bash
     mkdir credentials
     ```

   - Generate a Service Account Key from the Google Cloud Console, then move the downloaded JSON file to the `credentials` directory, renaming it to `key.json`.

Now, your environment is set up for intelligent document discovery with Vertex AI Search. Let's proceed with configuring your Google Cloud project settings, enabling APIs, and running the provided Python scripts to automate your search applications.
