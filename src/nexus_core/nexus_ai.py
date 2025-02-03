import json
import requests
import subprocess
import os
import logging
from typing import Optional, Dict, Any
from .response_handler import ResponseHandler

class NexusAI:
    """Core AI system for NexusOS."""
    
    def __init__(self, ollama_url: str = "http://localhost:11434"):
        self.ollama_url = ollama_url
        self.model = "llama2"  # Default model
        self.response_handler = ResponseHandler()
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for NexusAI."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            filename='nexus_ai.log'
        )
        self.logger = logging.getLogger('NexusAI')
        
    def get_prompt(self, user_input: str) -> str:
        """Generate a structured prompt for Ollama."""
        return f"""You are NexusOS, an AI-powered operating system. Analyze the user's input and return a structured JSON response.
Your response MUST be a valid JSON object with these fields:
1. "type": The type of action to perform
2. "speak": What to say to the user
3. Additional fields based on the action type

Available action types:
1. chat: General conversation
   {{"type": "chat", "speak": "response message"}}

2. command: Execute system command
   {{"type": "command", "command": "command to run", "speak": "message"}}

3. code: Generate code
   {{"type": "code", "language": "python", "code": "code here", "speak": "message"}}

4. system_info: Get system information
   {{"type": "system_info", "info": "requested info", "speak": "message"}}

5. create: Create a file
   {{"type": "create", "filename": "file.txt", "content": "content", "speak": "message"}}

6. read: Read a file
   {{"type": "read", "filename": "file.txt", "speak": "message"}}

Always return exactly ONE valid JSON object.
User input: {user_input}"""

    def query_ai(self, prompt: str) -> Optional[str]:
        """Query the Ollama AI model."""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }
            response = requests.post(f"{self.ollama_url}/api/generate", json=payload)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                self.logger.error(f"AI query failed with status code: {response.status_code}")
                return None
        except Exception as e:
            self.logger.error(f"Error querying AI: {str(e)}")
            return None
            
    def process_request(self, request: str) -> Dict[str, Any]:
        """Process a user request and return appropriate response."""
        try:
            # Generate structured prompt
            prompt = self.get_prompt(request)
            
            # Get AI response
            response_text = self.query_ai(prompt)
            if not response_text:
                return {
                    "success": False,
                    "error": "Failed to get AI response",
                    "output": "Sorry, I couldn't process your request."
                }
                
            # Handle the response
            result = self.response_handler.handle_response(response_text)
            if result:
                return {
                    "success": True,
                    "output": result.get('speak', 'Operation completed'),
                    "result": result
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to handle AI response",
                    "output": "Sorry, I couldn't process the AI response."
                }
                
        except Exception as e:
            self.logger.error(f"Error processing request: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "output": f"Error: {str(e)}"
            }

if __name__ == "__main__":
    # Test the NexusAI core
    nexus = NexusAI()
    test_request = "list all running processes"
    result = nexus.process_request(test_request)
    print(json.dumps(result, indent=2))
