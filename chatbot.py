from langchain.memory import ConversationBufferMemory
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.text_splitter import RecursiveCharacterTextSplitter
from bs4 import BeautifulSoup
import requests
from groq import Groq
from config import GROQ_API_KEY, SERPER_API_KEY
import trafilatura
import newspaper


class ChatBot:
    def __init__(self):
        self.memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        self.llm = Groq(api_key=GROQ_API_KEY)
        self.chat_history = []
        self.search = GoogleSerperAPIWrapper(serper_api_key=SERPER_API_KEY)

        # Initialize text splitter for processing long texts
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )

    def extract_content_from_url(self, url: str) -> str:
        """
        This function tries three different methods to get content from a webpage:
        1. First tries trafilatura (good for news articles)
        2. If that fails, tries newspaper3k
        3. If both fail, uses basic BeautifulSoup parsing
        """
        try:
            # First attempt: using trafilatura
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                content = trafilatura.extract(downloaded,
                                              include_comments=False,
                                              include_tables=True)
                if content:
                    return content

            # Second attempt: using newspaper
            article = newspaper.Article(url)
            article.download()
            article.parse()
            if article.text:
                return article.text

            # Last attempt: basic HTML parsing
            response = requests.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            # Removes unwanted elements like scripts, styles, etc.
            for tag in soup(['script', 'style', 'nav', 'footer', 'iframe']):
                tag.decompose()
            return ' '.join(soup.stripped_strings)

        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return ""

    def search_web(self, query: str) -> str:
        """
        Perform comprehensive web search using Serper
        """
        try:
            # Get results from Serper
            search_results = self.search.results(query)
            all_content = []

            # Gets the organic (non-ad) results
            organic_results = search_results.get('organic', [])
            # Process search results
            for result in organic_results[:5]:
                url = result.get('link')
                if url:
                    content = self.extract_content_from_url(url)
                    if content:
                        all_content.append({
                            'source': url,
                            'content': content,
                            'title': result.get('title', '')
                        })

            # Combine and format the content
            formatted_content = ""
            for item in all_content:
                # Split content into manageable chunks
                chunks = self.text_splitter.split_text(item['content'])
                # Take the most relevant chunk (usually the beginning)
                relevant_content = chunks[0] if chunks else ""

                formatted_content += f"\nSource: {item['title']}\nURL: {item['source']}\n"
                formatted_content += f"Content: {relevant_content}\n{'=' * 50}\n"

            return formatted_content if formatted_content else "No relevant information found."

        except Exception as e:
            # Add more detailed error logging
            print(f"Search results structure: {search_results}")
            return f"Error performing web search: {str(e)}"

    def generate_response(self, user_input: str, search_results: str) -> str:
        """
        Generate a response using the GroqLLM model with context from web search
        """
        context = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.chat_history[-5:]])

        prompt = f"""Based on the following search results and conversation context, provide a comprehensive and up-to-date response. 
        Focus on the most recent and relevant information.

        Previous conversation context:
        {context}
        
        Recent search results:
        {search_results}
        
        Current question: {user_input}
        
        Please provide a natural, informative response that:
        1. Prioritizes the most recent information from the search results
        2. Incorporates relevant context from our conversation
        3. Cites sources when stating specific facts or claims
        4. Distinguishes between factual information and any analysis or interpretation
        
        Response:"""

        try:
            chat_completion = self.llm.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model="llama3-8b-8192",
                stream=True
            )

            response_chunks = []
            for chunk in chat_completion:
                if chunk.choices[0].delta.content:
                    response_chunks.append(chunk.choices[0].delta.content)

            return "".join(response_chunks)
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def process_input(self, user_input: str) -> str:
        """
        Process user input and return a response
        """
        self.chat_history.append({"role": "user", "content": user_input})

        search_results = self.search_web(user_input)
        response = self.generate_response(user_input, search_results)

        self.chat_history.append({"role": "assistant", "content": response})
        self.memory.save_context(
            {"input": user_input},
            {"output": response}
        )

        return response
