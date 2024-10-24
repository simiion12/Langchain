FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Expose the port of streamlit
EXPOSE 8501

# Define the command to run streamlit
CMD ["streamlit", "run", "main.py"]
