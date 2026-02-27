"""
Тесты для Tesla AI Assistant
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tesla_app.tesla_client import TeslaAPIClient, TeslaVehicle
from tesla_app.ai_assistant import AIAssistant, AIResponse


class TestTeslaVehicle(unittest.TestCase):
    """Тесты модели TeslaVehicle"""
    
    def test_create_vehicle(self):
        """Тест создания объекта автомобиля"""
        data = {
            "id": 123,
            "vin": "5YJ3E1EAKF123456",
            "display_name": "My Tesla",
            "color": "Red",
            "tokens": ["abc123"],
            "state": "online",
            "in_service": False,
            "id_s": "123456",
            "vehicle_id": 123
        }
        
        vehicle = TeslaVehicle(**data)
        
        self.assertEqual(vehicle.id, 123)
        self.assertEqual(vehicle.vin, "5YJ3E1EAKF123456")
        self.assertEqual(vehicle.display_name, "My Tesla")
        self.assertEqual(vehicle.color, "Red")
        self.assertEqual(vehicle.state, "online")
        self.assertFalse(vehicle.in_service)


class TestTeslaAPIClient(unittest.TestCase):
    """Тесты Tesla API клиента"""
    
    def setUp(self):
        """Настройка тестового клиента"""
        self.mock_session = Mock()
        self.client = TeslaAPIClient("test_token")
        self.client.session = self.mock_session
    
    def test_get_vehicles(self):
        """Тест получения списка автомобилей"""
        mock_response = {
            "response": [
                {
                    "id": 1,
                    "vin": "5YJ3E1EA1KF123456",
                    "display_name": "Model 3",
                    "color": "White",
                    "tokens": ["token1"],
                    "state": "online",
                    "in_service": False,
                    "id_s": "vehicle1",
                    "vehicle_id": 1
                }
            ]
        }
        
        self.mock_session.get.return_value.json.return_value = mock_response
        self.mock_session.get.return_value.raise_for_status = Mock()
        
        vehicles = self.client.get_vehicles()
        
        self.assertEqual(len(vehicles), 1)
        self.assertEqual(vehicles[0].vin, "5YJ3E1EA1KF123456")
        self.mock_session.get.assert_called_once()
    
    def test_get_vehicle_summary(self):
        """Тест получения сводки об автомобиле"""
        vehicle_data = {
            "display_name": "Model 3",
            "vin": "5YJ3E1EA1KF123456",
            "color": "White",
            "state": "online",
            "battery_range": 400,
            "odometer": 50000,
            "software_update": {"version": "2024.1.1"},
            "locked": True,
            "sentry_mode": False,
            "summon_standby": False
        }
        
        charge_state = {
            "battery_level": 85,
            "charging_state": "complete",
            "charge_rate": 0,
            "time_to_full_charge": 0
        }
        
        drive_state = {
            "latitude": 55.7558,
            "longitude": 37.6173,
            "speed": 0,
            "power": 0
        }
        
        # Мокаем методы
        self.client.get_vehicle_data = Mock(return_value=vehicle_data)
        self.client.get_charge_state = Mock(return_value=charge_state)
        self.client.get_drive_state = Mock(return_value=drive_state)
        
        summary = self.client.get_vehicle_summary("test_vehicle_id")
        
        self.assertIn("Model 3", summary)
        self.assertIn("85%", summary)
        self.assertIn("5YJ3E1EA1KF123456", summary)
    
    def test_honk_horn(self):
        """Тест бибикания"""
        self.mock_session.post.return_value.status_code = 200
        
        result = self.client.honk_horn("test_id")
        
        self.assertTrue(result)
        self.mock_session.post.assert_called_once()
    
    def test_lock_doors(self):
        """Тест блокировки дверей"""
        self.mock_session.post.return_value.json.return_value = {"response": True}
        
        result = self.client.lock_doors("test_id", lock=True)
        
        self.assertTrue(result)
    
    def test_start_climate(self):
        """Тест включения климата"""
        self.mock_session.post.return_value.status_code = 200
        self.mock_session.post.return_value.json.return_value = {"response": True}
        
        result = self.client.start_climate("test_id", temperature=23.5)
        
        self.assertTrue(result)


class TestAIAssistant(unittest.TestCase):
    """Тесты AI ассистента"""
    
    @patch('tesla_app.ai_assistant.OpenAI')
    def test_generate_response(self, mock_openai_class):
        """Тест генерации ответа"""
        # Настраиваем мок
        mock_client = Mock()
        mock_openai_class.return_value = mock_client
        
        mock_response = Mock()
        mock_response.choices = [Mock(message=Mock(content="Привет! Я AI ассистент Tesla."))]
        mock_response.usage = Mock(total_tokens=50)
        
        mock_client.chat.completions.create.return_value = mock_response
        
        assistant = AIAssistant(api_key="test_key")
        response = assistant.generate_response("Привет")
        
        self.assertEqual(response.content, "Привет! Я AI ассистент Tesla.")
        self.assertEqual(response.tokens_used, 50)
    
    def test_add_to_history(self):
        """Тест добавления в историю"""
        assistant = AIAssistant(api_key="test_key")
        
        assistant.add_to_history("user", "Привет")
        assistant.add_to_history("assistant", "Привет! Как дела?")
        
        self.assertEqual(len(assistant.conversation_history), 2)
        self.assertEqual(assistant.conversation_history[0]["role"], "user")
        self.assertEqual(assistant.conversation_history[1]["role"], "assistant")
    
    def test_history_limit(self):
        """Тест ограничения истории"""
        assistant = AIAssistant(api_key="test_key")
        
        # Добавляем 15 сообщений
        for i in range(15):
            assistant.add_to_history("user", f"Message {i}")
            assistant.add_to_history("assistant", f"Response {i}")
        
        # История должна быть ограничена 10 последними сообщениями (5 пар)
        self.assertEqual(len(assistant.conversation_history), 10)
        
        # Проверяем, что остались последние сообщения
        self.assertEqual(assistant.conversation_history[0]["content"], "Message 10")


class TestIntegration(unittest.TestCase):
    """Интеграционные тесты"""
    
    def test_module_imports(self):
        """Тест импорта модулей"""
        from tesla_app import TeslaAPIClient, TeslaVehicle, AIAssistant
        from tesla_app.cli import TeslaAICLI
        
        self.assertTrue(callable(TeslaAPIClient))
        self.assertTrue(callable(AIAssistant))
        self.assertTrue(callable(TeslaAICLI))


if __name__ == "__main__":
    unittest.main(verbosity=2)
