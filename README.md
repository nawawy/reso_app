# Reso Researcher Chat Agent

## Overview
This project implements a full-stack AI-powered search agent called **Reso Researcher Chat Agent**. It combines a Python-based backend with a React frontend to perform web searches, scrape articles, and extract structured data based on user-defined schemas. The backend leverages APIs like Serper for search and OpenAI for data extraction, while the frontend provides a user-friendly chat interface for interaction.

## Project Structure

- **backend/**: Contains the Python backend code.
  - `app/`: Main application folder.
    - `agent.py`: Core logic for scraping articles and extracting data using NLP and OpenAI.
    - `config.py`: Configuration file for API keys (loaded from `.env`).
    - `main.py`: FastAPI application to handle API requests.
    - `schemas.py`: Pydantic models for request validation.
    - `utils.py`: Utility functions for text processing and chunking.
  - `requirements.txt`: Lists Python dependencies.
  - `.env`: Stores environment variables like API keys (not included in version control).

- **frontend/**: Contains the React frontend code.
  - `src/`: Source folder for React components and styles.
    - `App.jsx`: Main React component for the chat interface.
    - `App.css`, `index.css`: Styling for the frontend.
  - `index.html`: Entry point for the React app.
  - `package.json`, `vite.config.js`: Configuration for the Vite build tool.
  - `.eslintrc.js`: ESLint configuration for linting.
  - `.gitignore`: Specifies files to ignore in version control.

## Features
- **Search Functionality**: Uses the Serper API to fetch search results based on user prompts.
- **Article Scraping**: Scrapes articles using the `newspaper3k` library.
- **Data Extraction**: Combines rule-based (spaCy) and AI-based (OpenAI) methods to extract fields like title, authors, and dates.
- **Frontend Interface**: A React-based chat UI built with Material-UI for user interaction.
- **Backend API**: FastAPI server to handle search requests and return extracted data.

## Prerequisites
- **Python 3.8+**: For the backend.
- **Node.js 18+**: For the frontend.
- API keys for:
  - [Serper API](https://serper.dev/) (for search).
  - [OpenAI API](https://openai.com/) (for data extraction).

## Setup Instructions

### Backend
1. Navigate to the `backend/` directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Install the spaCy model:
   ```bash
   python -m spacy download en_core_web_sm
   ```
5. Set up environment variables in a `.env` file:
   ```plaintext
   SERPER_API_KEY=your_serper_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```
6. Run the FastAPI server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Frontend
1. Navigate to the `frontend/` directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   npm install @mui/material @emotion/react @emotion/styled
   npm install tailwindcss @tailwindcss/vite
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
   The frontend will be available at `http://localhost:5173` (or the port specified by Vite).

## Usage
1. Open the frontend in your browser.
2. Enter a search prompt (e.g., "Elon Musk biography") and an optional schema in JSON format (e.g., `["title", "authors", "date_of_birth"]`).
3. Click "Send" to initiate the search.
4. The backend will fetch search results, scrape articles, extract data, and display the results in the chat interface.

## Example
- **Prompt**: "Elon Musk biography"
- **Schema**: `["title", "authors", "date_of_birth"]`
- **Output**: The chat will display extracted data from the top search result, such as the article title, authors, and any identified dates of birth.

## Dependencies
### Backend
- `fastapi`: For the API server.
- `httpx`: For asynchronous HTTP requests.
- `spacy`: For NLP-based data extraction.
- `openai`: For AI-based data extraction.
- `newspaper3k`: For article scraping.
- `nltk`, `langchain`: For text processing.

### Frontend
- `react`: For the UI.
- `@mui/material`: For Material-UI components.
- `vite`: For the build tool.

## Notes
- Ensure your API keys are kept secure and not exposed in version control.
- The backend API runs on `http://localhost:8000` by default. Update the frontend fetch URL in `App.jsx` if you change the backend port or host.
- The schema field in the frontend is optional but must be valid JSON if provided.

## Troubleshooting
- **Backend Errors**:
  - If the Serper or OpenAI API fails, check your API keys in the `.env` file.
  - Ensure the spaCy model (`en_core_web_sm`) is installed.
- **Frontend Errors**:
  - If the frontend cannot connect to the backend, verify that the backend server is running and the fetch URL in `App.jsx` is correct.
  - Check the browser console for CORS-related errors and adjust the CORS settings in `main.py` if needed.