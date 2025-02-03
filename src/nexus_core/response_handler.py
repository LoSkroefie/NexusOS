import json
import os
import subprocess
from typing import Dict, Any, Optional
import logging

class ResponseHandler:
    """Handle structured responses from Ollama."""
    
    def __init__(self):
        self.logger = logging.getLogger('NexusAI.ResponseHandler')
        
    def handle_response(self, response_text: str) -> Optional[Dict[str, Any]]:
        """Parse and handle the response from Ollama."""
        try:
            # Try to parse the response as JSON
            response = json.loads(response_text)
            
            # Validate response structure
            if 'type' not in response or 'speak' not in response:
                raise ValueError("Invalid response structure")
                
            # Handle different response types
            handler_method = getattr(self, f"_handle_{response['type']}", None)
            if handler_method:
                return handler_method(response)
            else:
                return {
                    'type': 'error',
                    'error': f"Unknown response type: {response['type']}",
                    'speak': f"Sorry, I don't know how to handle {response['type']} actions."
                }
                
        except json.JSONDecodeError:
            return {
                'type': 'error',
                'error': "Invalid JSON response",
                'speak': "Sorry, I received an invalid response format."
            }
        except Exception as e:
            self.logger.error(f"Error handling response: {str(e)}")
            return {
                'type': 'error',
                'error': str(e),
                'speak': f"Sorry, an error occurred: {str(e)}"
            }
            
    def _handle_chat(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle chat responses."""
        return {
            'type': 'chat',
            'result': response['speak'],
            'speak': response['speak']
        }
        
    def _handle_command(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle system command execution."""
        try:
            result = subprocess.run(
                response['command'],
                shell=True,
                capture_output=True,
                text=True
            )
            return {
                'type': 'command',
                'result': result.stdout if result.returncode == 0 else result.stderr,
                'success': result.returncode == 0,
                'speak': response['speak']
            }
        except Exception as e:
            return {
                'type': 'error',
                'error': str(e),
                'speak': f"Error executing command: {str(e)}"
            }
            
    def _handle_create(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle file creation."""
        try:
            os.makedirs(os.path.dirname(response['filename']), exist_ok=True)
            with open(response['filename'], 'w') as f:
                f.write(response['content'])
            return {
                'type': 'create',
                'result': f"File {response['filename']} created successfully",
                'speak': response['speak']
            }
        except Exception as e:
            return {
                'type': 'error',
                'error': str(e),
                'speak': f"Error creating file: {str(e)}"
            }
            
    def _handle_code(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle code generation."""
        try:
            filename = f"generated_{response['language']}_code.{response['language']}"
            with open(filename, 'w') as f:
                f.write(response['code'])
            return {
                'type': 'code',
                'result': {
                    'filename': filename,
                    'code': response['code']
                },
                'speak': response['speak']
            }
        except Exception as e:
            return {
                'type': 'error',
                'error': str(e),
                'speak': f"Error generating code: {str(e)}"
            }
            
    def _handle_system_info(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle system information requests."""
        import psutil
        try:
            info = {
                'cpu': psutil.cpu_percent(interval=1),
                'memory': psutil.virtual_memory()._asdict(),
                'disk': {path: psutil.disk_usage(path)._asdict() 
                        for path in psutil.disk_partitions()}
            }
            return {
                'type': 'system_info',
                'result': info,
                'speak': response['speak']
            }
        except Exception as e:
            return {
                'type': 'error',
                'error': str(e),
                'speak': f"Error getting system info: {str(e)}"
            }
            
    def _handle_read(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Handle file reading."""
        try:
            with open(response['filename'], 'r') as f:
                content = f.read()
            return {
                'type': 'read',
                'result': content,
                'speak': response['speak']
            }
        except Exception as e:
            return {
                'type': 'error',
                'error': str(e),
                'speak': f"Error reading file: {str(e)}"
            }
