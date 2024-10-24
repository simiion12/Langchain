# Interactive Chatbot with Web Search

Welcome to the **Interactive Chatbot with Web Search**! This project utilizes Streamlit to create a web-based chatbot that leverages real-time web searches to provide informative responses based on user queries. The chatbot is powered by the LangChain framework and integrates several content extraction methods to gather relevant information from various sources.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Dockerization](#dockerization)
- [License](#license)

## Features

- **Interactive Chat Interface**: Engage in a conversation with the chatbot using a friendly web interface.
- **Web Search Capability**: The chatbot can perform web searches to retrieve up-to-date information.
- **Multiple Content Extraction Methods**: Extracts relevant content from web pages using various libraries like `trafilatura`, `newspaper3k`, and `BeautifulSoup`.
- **Memory Management**: Keeps track of the conversation context for better responses.

## Technologies Used

- **Streamlit**: For building the web interface.
- **LangChain**: For managing conversational memory and interactions.
- **Groq**: For processing user queries with a powerful LLM.
- **BeautifulSoup**: For parsing HTML content.
- **Requests**: For making HTTP requests to fetch web pages.
- **Trafilatura**: For content extraction from URLs.
- **Newspaper3k**: For article scraping and parsing.

## Installation

To get started with this project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/simiion12/Langchain.git
    ```
2. **Set up your environment: Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
3. **Install dependencies: Use the provided requirements.txt file:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set environment variables: Create a .env file in the root directory and include the following:**
   ```bash
   GROQ_API_KEY=your_groq_api_key
   SERPER_API_KEY=your_serper_api_key
   ```

## Usage

To run the chatbot, execute the following command:
```bash
streamlit run main.py
```
Then, open your web browser and go to http://localhost:8501 to interact with the chatbot.

## How It Works

- `User Interaction:` Users can input queries through the Streamlit interface.
- `Web Search:` The chatbot performs a web search using the Google Serper API to gather relevant information.
- `Content Extraction:` It attempts to extract content from the resulting URLs using multiple libraries to ensure quality information retrieval.
- `Response Generation:` The chatbot generates a natural language response based on the search results and the context of the conversation, utilizing the Groq LLM.
- `Conversation Memory:` All interactions are stored in memory to maintain context across the conversation.

  ## Dockerization

  This project can be easily run using Docker. To start the application, simply use the following command:
  
   ```bash
   docker-compose up --build.
    ```


  ## License
  This project is licensed under the MIT License. See the LICENSE file for details.
