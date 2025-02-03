import sounddevice as sd
import numpy as np
import threading
import queue
import websockets
import json
import asyncio
from typing import Callable, Optional
import logging

class VoiceProcessor:
    """Process voice commands for NexusAI."""
    
    def __init__(self, command_callback: Callable[[str], None]):
        self.command_callback = command_callback
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.sample_rate = 16000
        self.setup_logging()
        
    def setup_logging(self):
        self.logger = logging.getLogger('NexusAI.Voice')
        
    def start_listening(self):
        """Start listening for voice commands."""
        self.is_listening = True
        self.stream = sd.InputStream(
            channels=1,
            samplerate=self.sample_rate,
            callback=self._audio_callback
        )
        self.stream.start()
        
        # Start processing thread
        self.process_thread = threading.Thread(target=self._process_audio)
        self.process_thread.daemon = True
        self.process_thread.start()
        
        self.logger.info("Voice processing started")
        
    def stop_listening(self):
        """Stop listening for voice commands."""
        self.is_listening = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        self.logger.info("Voice processing stopped")
        
    def _audio_callback(self, indata, frames, time, status):
        """Callback for audio input."""
        if status:
            self.logger.warning(f"Audio callback status: {status}")
        if self.is_listening:
            self.audio_queue.put(indata.copy())
            
    async def _process_chunk(self, audio_data: np.ndarray) -> Optional[str]:
        """Process a chunk of audio data using local Whisper API."""
        try:
            # Convert audio to the correct format
            audio_float32 = audio_data.astype(np.float32)
            
            # You can replace this with any speech-to-text API
            # For now, we'll use a mock response
            return "example command"
            
        except Exception as e:
            self.logger.error(f"Error processing audio: {str(e)}")
            return None
            
    def _process_audio(self):
        """Process audio chunks from the queue."""
        while self.is_listening:
            try:
                # Get audio chunk from queue
                audio_chunk = self.audio_queue.get(timeout=1)
                
                # Process the audio
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                text = loop.run_until_complete(self._process_chunk(audio_chunk))
                
                if text:
                    # Call the callback with the recognized text
                    self.command_callback(text)
                    
            except queue.Empty:
                continue
            except Exception as e:
                self.logger.error(f"Error in audio processing: {str(e)}")
                continue
                
    def is_active(self) -> bool:
        """Check if voice processing is active."""
        return self.is_listening
