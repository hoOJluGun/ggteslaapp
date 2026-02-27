"""
Tesla API Client - модуль для работы с Tesla API
"""

import requests
from typing import Optional, Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TeslaVehicle:
    """Модель данных автомобиля Tesla"""
    id: int
    vin: str
    display_name: str
    color: Optional[str]
    tokens: List[str]
    state: str
    in_service: bool
    id_s: str
    vehicle_id: int


class TeslaAPIClient:
    """Клиент для работы с Tesla API"""
    
    def __init__(self, access_token: str, base_url: str = "https://owner-api.teslamotors.com"):
        """
        Инициализация Tesla API клиента
        
        Args:
            access_token: OAuth токен доступа
            base_url: Базовый URL API
        """
        self.access_token = access_token
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        })
    
    def get_vehicles(self) -> List[TeslaVehicle]:
        """
        Получить список всех автомобилей пользователя
        
        Returns:
            Список объектов TeslaVehicle
        """
        response = self.session.get(f"{self.base_url}/api/1/vehicles")
        response.raise_for_status()
        
        data = response.json()
        vehicles = []
        for v in data.get("response", []):
            vehicle = TeslaVehicle(
                id=v.get("id"),
                vin=v.get("vin"),
                display_name=v.get("display_name"),
                color=v.get("color"),
                tokens=v.get("tokens", []),
                state=v.get("state"),
                in_service=v.get("in_service", False),
                id_s=v.get("id_s"),
                vehicle_id=v.get("vehicle_id")
            )
            vehicles.append(vehicle)
        
        return vehicles
    
    def get_vehicle_data(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Получить полные данные об автомобиле
        
        Args:
            vehicle_id: ID автомобиля (id_s)
            
        Returns:
            Словарь с данными автомобиля
        """
        response = self.session.get(
            f"{self.base_url}/api/1/vehicles/{vehicle_id}/data"
        )
        response.raise_for_status()
        return response.json().get("response", {})
    
    def get_vehicle_state(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Получить текущее состояние автомобиля
        
        Args:
            vehicle_id: ID автомобиля
            
        Returns:
            Словарь с состоянием автомобиля
        """
        response = self.session.get(
            f"{self.base_url}/api/1/vehicles/{vehicle_id}/vehicle_data"
        )
        response.raise_for_status()
        return response.json().get("response", {})
    
    def get_charge_state(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Получить состояние зарядки
        
        Args:
            vehicle_id: ID автомобиля
            
        Returns:
            Словарь с состоянием зарядки
        """
        response = self.session.get(
            f"{self.base_url}/api/1/vehicles/{vehicle_id}/charge_state"
        )
        response.raise_for_status()
        return response.json().get("response", {})
    
    def get_climate_state(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Получить состояние климат-контроля
        
        Args:
            vehicle_id: ID автомобиля
            
        Returns:
            Словарь с состоянием климат-контроля
        """
        response = self.session.get(
            f"{self.base_url}/api/1/vehicles/{vehicle_id}/climate_state"
        )
        response.raise_for_status()
        return response.json().get("response", {})
    
    def get_drive_state(self, vehicle_id: str) -> Dict[str, Any]:
        """
        Получить информацию о местоположении и движении
        
        Args:
            vehicle_id: ID автомобиля
            
        Returns:
            Словарь с данными о движении
        """
        response = self.session.get(
            f"{self.base_url}/api/1/vehicles/{vehicle_id}/drive_state"
        )
        response.raise_for_status()
        return response.json().get("response", {})
    
    def get_vehicle_summary(self, vehicle_id: str) -> str:
        """
        Получить текстовую сводку об автомобиле
        
        Args:
            vehicle_id: ID автомобиля
            
        Returns:
            Форматированная строка с информацией
        """
        try:
            vehicle_data = self.get_vehicle_data(vehicle_id)
            charge_state = self.get_charge_state(vehicle_id)
            drive_state = self.get_drive_state(vehicle_id)
            
            summary = f"""
🚗 Tesla Vehicle Summary:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 Basic Info:
  • Name: {vehicle_data.get('display_name', 'N/A')}
  • VIN: {vehicle_data.get('vin', 'N/A')}
  • Color: {vehicle_data.get('color', 'N/A')}
  • State: {vehicle_data.get('state', 'N/A')}

🔋 Battery & Charge:
  • Battery Level: {charge_state.get('battery_level', 'N/A')}%
  • Charging State: {charge_state.get('charging_state', 'N/A')}
  • Charge Rate: {charge_state.get('charge_rate', 'N/A')} km/h
  • Time to Full Charge: {charge_state.get('time_to_full_charge', 'N/A')} hours
  • Range: {vehicle_data.get('battery_range', 'N/A')} km

📍 Location:
  • Latitude: {drive_state.get('latitude', 'N/A')}
  • Longitude: {drive_state.get('longitude', 'N/A')}
  • Speed: {drive_state.get('speed', 'N/A')} km/h
  • Power: {drive_state.get('power', 'N/A')} kW

🔧 Vehicle Info:
  • Odometer: {vehicle_data.get('odometer', 'N/A')} km
  • Software Version: {vehicle_data.get('software_update', {}).get('version', 'N/A')}
  • Locked: {vehicle_data.get('locked', 'N/A')}
  • Sentry Mode: {vehicle_data.get('sentry_mode', 'N/A')}
  • Summon Standby: {vehicle_data.get('summon_standby', 'N/A')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
            return summary
        except Exception as e:
            return f"Error getting vehicle summary: {str(e)}"
    
    def honk_horn(self, vehicle_id: str) -> bool:
        """
        Побибикать клаксоном
        
        Args:
            vehicle_id: ID автомобиля
            
        Returns:
            True если успешно
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/1/vehicles/{vehicle_id}/command/honk_horn"
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def lock_doors(self, vehicle_id: str, lock: bool = True) -> bool:
        """
        Заблокировать/разблокировать двери
        
        Args:
            vehicle_id: ID автомобиля
            lock: True - заблокировать, False - разблокировать
            
        Returns:
            True если успешно
        """
        try:
            command = "lock" if lock else "unlock"
            response = self.session.post(
                f"{self.base_url}/api/1/vehicles/{vehicle_id}/command/{command}_doors"
            )
            return response.json().get("response", False)
        except Exception:
            return False
    
    def start_climate(self, vehicle_id: str, temperature: float = 22.0) -> bool:
        """
        Включить климат-контроль
        
        Args:
            vehicle_id: ID автомобиля
            temperature: Желаемая температура в градусах Цельсия
            
        Returns:
            True если успешно
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/1/vehicles/{vehicle_id}/command/set_temps",
                json={"driver_temp": temperature, "passenger_temp": temperature}
            )
            if response.status_code == 200:
                response = self.session.post(
                    f"{self.base_url}/api/1/vehicles/{vehicle_id}/command/auto_condition_air"
                )
                return response.json().get("response", False)
            return False
        except Exception:
            return False
    
    def stop_climate(self, vehicle_id: str) -> bool:
        """
        Выключить климат-контроль
        
        Args:
            vehicle_id: ID автомобиля
            
        Returns:
            True если успешно
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/1/vehicles/{vehicle_id}/command/auto_condition_air_off"
            )
            return response.json().get("response", False)
        except Exception:
            return False
    
    def flash_lights(self, vehicle_id: str) -> bool:
        """
        Мигнуть фарами
        
        Args:
            vehicle_id: ID автомобиля
            
        Returns:
            True если успешно
        """
        try:
            response = self.session.post(
                f"{self.base_url}/api/1/vehicles/{vehicle_id}/command/flash_lights"
            )
            return response.json().get("response", False)
        except Exception:
            return False
