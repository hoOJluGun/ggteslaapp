"""
Tesla AI Assistant - основной пакет
"""

__version__ = "1.0.0"
__author__ = "Tesla AI Team"

from .tesla_client import TeslaAPIClient, TeslaVehicle
from .ai_assistant import AIAssistant, AIResponse

__all__ = [
    "TeslaAPIClient",
    "TeslaVehicle", 
    "AIAssistant",
    "AIResponse"
]
