"""
AI Assistant Module - интеграция с OpenAI API
"""

import os
from typing import Optional, Dict, Any, List
from openai import OpenAI
from dataclasses import dataclass


@dataclass
class AIResponse:
    """Структура ответа от AI"""
    content: str
    tokens_used: int
    model: str


class AIAssistant:
    """AI ассистент для работы с Tesla через естественный язык"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4"):
        """
        Инициализация AI ассистента
        
        Args:
            api_key: OpenAI API ключ
            model: Модель GPT для использования
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.conversation_history: List[Dict[str, str]] = []
    
    def add_to_history(self, role: str, content: str):
        """Добавить сообщение в историю разговора"""
        self.conversation_history.append({"role": role, "content": content})
        # Ограничиваем историю последними 10 сообщениями
        if len(self.conversation_history) > 10:
            self.conversation_history = self.conversation_history[-10:]
    
    def generate_response(
        self, 
        prompt: str, 
        system_prompt: Optional[str] = None,
        vehicle_context: Optional[Dict[str, Any]] = None
    ) -> AIResponse:
        """
        Генерировать ответ от AI
        
        Args:
            prompt: Запрос пользователя
            system_prompt: Системный промпт
            vehicle_context: Контекст данных автомобиля
            
        Returns:
            AIResponse объект с ответом
        """
        messages = []
        
        # Системный промпт по умолчанию
        default_system = """Ты AI ассистент для управления автомобилем Tesla. 
Ты помогаешь пользователю выполнять команды, отвечать на вопросы о состоянии автомобиля 
и предоставлять информацию. Отвечай кратко, информативно и на русском языке."""
        
        if vehicle_context:
            default_system += f"\n\nТекущее состояние автомобиля:\n{vehicle_context}"
        
        messages.append({
            "role": "system", 
            "content": system_prompt or default_system
        })
        
        # Добавляем историю
        messages.extend(self.conversation_history)
        
        # Добавляем текущий запрос
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            tokens_used = response.usage.total_tokens if response.usage else 0
            
            # Сохраняем в историю
            self.add_to_history("user", prompt)
            self.add_to_history("assistant", content)
            
            return AIResponse(
                content=content,
                tokens_used=tokens_used,
                model=self.model
            )
            
        except Exception as e:
            return AIResponse(
                content=f"Ошибка при генерации ответа: {str(e)}",
                tokens_used=0,
                model=self.model
            )
    
    def parse_command(self, user_input: str, vehicle_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Парсить естественный язык в команду для Tesla
        
        Args:
            user_input: Ввод пользователя на естественном языке
            vehicle_state: Текущее состояние автомобиля
            
        Returns:
            Словарь с командой и параметрами
        """
        prompt = f"""
На основе запроса пользователя определи, какую команду Tesla нужно выполнить.
Верни ответ в формате JSON с полями:
- command: название команды (например: 'honk', 'lock', 'unlock', 'start_climate', 'stop_climate', 'flash_lights', 'get_status')
- parameters: объект с параметрами команды (если нужны)
- confidence: уверенность от 0 до 1

Текущее состояние автомобиля:
{vehicle_state}

Запрос пользователя: "{user_input}"

Примеры:
- "Побибикай" -> {{"command": "honk", "parameters": {{}}, "confidence": 0.95}}
- "Заблокируй двери" -> {{"command": "lock", "parameters": {{}}, "confidence": 0.98}}
- "Включи кондиционер на 23 градуса" -> {{"command": "start_climate", "parameters": {{"temperature": 23}}, "confidence": 0.9}}
- "Какой заряд батареи?" -> {{"command": "get_status", "parameters": {{"what": "battery"}}, "confidence": 0.95}}

Верни только JSON, без дополнительного текста.
"""
        
        response = self.generate_response(prompt, system_prompt="Ты парсер команд для Tesla.")
        
        try:
            import json
            # Извлекаем JSON из ответа
            content = response.content.strip()
            # Находим JSON в ответе
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != -1:
                json_str = content[start:end]
                return json.loads(json_str)
        except Exception:
            pass
        
        return {
            "command": "unknown",
            "parameters": {},
            "confidence": 0.0
        }
    
    def explain_vehicle_data(self, data: Dict[str, Any]) -> str:
        """
        Объяснить данные автомобиля простыми словами
        
        Args:
            data: Данные автомобиля
            
        Returns:
            Объяснение на естественном языке
        """
        prompt = f"""
Объясни следующие данные об автомобиле Tesla простыми словами на русском языке:

{data}

Сделай объяснение понятным для обычного пользователя, выдели важную информацию.
"""
        response = self.generate_response(prompt)
        return response.content
    
    def get_advice(self, vehicle_state: Dict[str, Any]) -> str:
        """
        Получить рекомендации на основе состояния автомобиля
        
        Args:
            vehicle_state: Состояние автомобиля
            
        Returns:
            Рекомендации
        """
        prompt = f"""
На основе состояния автомобиля дай полезные рекомендации владельцу.
Учитывай уровень заряда, местоположение, климат и другие факторы.

Состояние автомобиля:
{vehicle_state}

Дай 2-3 конкретные рекомендации.
"""
        response = self.generate_response(prompt)
        return response.content
