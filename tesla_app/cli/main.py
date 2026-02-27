#!/usr/bin/env python3
"""
Tesla AI Assistant - CLI интерфейс для управления Tesla с AI
"""

import cmd
import sys
import os
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown

# Добавляем родительскую директорию в путь
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tesla_app.tesla_client import TeslaAPIClient, TeslaVehicle
from tesla_app.ai_assistant import AIAssistant

console = Console()


class TeslaAICLI(cmd.Cmd):
    """Интерактивный CLI для управления Tesla с AI"""
    
    intro = """
╔═══════════════════════════════════════════════════════════════╗
║           🚗 Tesla AI Assistant v1.0.0                      ║
║           Управление Tesla через естественный язык          ║
╚═══════════════════════════════════════════════════════════════╝

Доступные команды:
  status          - Показать статус автомобиля
  vehicles        - Список автомобилей
  select <id>     - Выбрать автомобиль
  honk            - Побибикать
  lock            - Заблокировать двери
  unlock          - Разблокировать двери
  climate <temp>  - Включить климат (температура в °C)
  stop-climate    - Выключить климат
  flash           - Мигнуть фарами
  ask <вопрос>    - Спросить у AI о состоянии автомобиля
  chat <текст>    - Поговорить с AI ассистентом
  advice          - Получить рекомендации
  help            - Показать эту справку
  exit            - Выйти

Для быстрого доступа к командам можно использовать естественный язык:
  Примеры: "заблокируй машину", "включи кондиционер", "какой заряд?"
"""
    
    prompt = "\n[tesla]> "
    
    def __init__(self, tesla_client: TeslaAPIClient, ai_assistant: Optional[AIAssistant] = None):
        super().__init__()
        self.tesla = tesla_client
        self.ai = ai_assistant
        self.current_vehicle: Optional[TeslaVehicle] = None
        self.vehicles: List[TeslaVehicle] = []
    
    def preloop(self):
        """Действия перед началом цикла команд"""
        try:
            self.vehicles = self.tesla.get_vehicles()
            if self.vehicles:
                self.current_vehicle = self.vehicles[0]
                console.print(f"[green]✓ Загружено {len(self.vehicles)} автомобилей[/green]")
                console.print(f"[cyan]Выбран: {self.current_vehicle.display_name} ({self.current_vehicle.vin})[/cyan]")
            else:
                console.print("[yellow]⚠ Автомобили не найдены[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ Ошибка загрузки автомобилей: {e}[/red]")
    
    def do_status(self, arg):
        """Показать статус текущего автомобиля"""
        if not self.current_vehicle:
            console.print("[red]✗ Сначала выберите автомобиль[/red]")
            return
        
        try:
            summary = self.tesla.get_vehicle_summary(self.current_vehicle.id_s)
            console.print(Panel.fit(summary, title="📊 Статус автомобиля", border_style="cyan"))
        except Exception as e:
            console.print(f"[red]✗ Ошибка получения статуса: {e}[/red]")
    
    def do_vehicles(self, arg):
        """Показать список автомобилей"""
        try:
            self.vehicles = self.tesla.get_vehicles()
            
            table = Table(title="🚗 Ваши автомобили Tesla")
            table.add_column("ID", style="cyan")
            table.add_column("Имя", style="magenta")
            table.add_column("VIN", style="green")
            table.add_column("Состояние", style="yellow")
            table.add_column("ID_s", style="dim")
            
            for v in self.vehicles:
                table.add_row(
                    str(v.id),
                    v.display_name,
                    v.vin,
                    v.state,
                    v.id_s
                )
            
            console.print(table)
            
            if self.current_vehicle:
                console.print(f"[cyan]Текущий: {self.current_vehicle.display_name}[/cyan]")
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_select(self, arg):
        """Выбрать автомобиль по ID или индексу"""
        if not arg:
            console.print("[red]✗ Укажите ID или индекс автомобиля[/red]")
            return
        
        try:
            idx = int(arg) - 1
            if 0 <= idx < len(self.vehicles):
                self.current_vehicle = self.vehicles[idx]
                console.print(f"[green]✓ Выбран: {self.current_vehicle.display_name}[/green]")
            else:
                console.print("[red]✗ Неверный индекс[/red]")
        except ValueError:
            # Ищем по id_s или display_name
            for v in self.vehicles:
                if v.id_s == arg or v.display_name == arg:
                    self.current_vehicle = v
                    console.print(f"[green]✓ Выбран: {v.display_name}[/green]")
                    return
            console.print("[red]✗ Автомобиль не найден[/red]")
    
    def do_honk(self, arg):
        """Побибикать клаксоном"""
        if not self.current_vehicle:
            console.print("[red]✗ Сначала выберите автомобиль[/red]")
            return
        
        try:
            success = self.tesla.honk_horn(self.current_vehicle.id_s)
            if success:
                console.print("[green]✓ Бибикнул! 🎵[/green]")
            else:
                console.print("[yellow]⚠ Не удалось побибикать[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_lock(self, arg):
        """Заблокировать двери"""
        if not self.current_vehicle:
            console.print("[red]✗ Сначала выберите автомобиль[/red]")
            return
        
        try:
            success = self.tesla.lock_doors(self.current_vehicle.id_s, lock=True)
            if success:
                console.print("[green]✓ Двери заблокированы 🔒[/green]")
            else:
                console.print("[yellow]⚠ Не удалось заблокировать[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_unlock(self, arg):
        """Разблокировать двери"""
        if not self.current_vehicle:
            console.print("[red]✗ Сначала выберите автомобиль[/red]")
            return
        
        try:
            success = self.tesla.lock_doors(self.current_vehicle.id_s, lock=False)
            if success:
                console.print("[green]✓ Двери разблокированы 🔓[/green]")
            else:
                console.print("[yellow]⚠ Не удалось разблокировать[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_climate(self, arg):
        """Включить климат-контроль [температура]"""
        if not self.current_vehicle:
            console.print("[red]✗ Сначала выберите автомобиль[/red]")
            return
        
        try:
            temp = float(arg) if arg else 22.0
            success = self.tesla.start_climate(self.current_vehicle.id_s, temperature=temp)
            if success:
                console.print(f"[green]✓ Климат-контроль включен на {temp}°C ❄️[/green]")
            else:
                console.print("[yellow]⚠ Не удалось включить климат[/yellow]")
        except ValueError:
            console.print("[red]✗ Укажите число (температуру в °C)[/red]")
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_stop_climate(self, arg):
        """Выключить климат-контроль"""
        if not self.current_vehicle:
            console.print("[red]✗ Сначала выберите автомобиль[/red]")
            return
        
        try:
            success = self.tesla.stop_climate(self.current_vehicle.id_s)
            if success:
                console.print("[green]✓ Климат-контроль выключен[/green]")
            else:
                console.print("[yellow]⚠ Не удалось выключить климат[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_flash(self, arg):
        """Мигнуть фарами"""
        if not self.current_vehicle:
            console.print("[red]✗ Сначала выберите автомобиль[/red]")
            return
        
        try:
            success = self.tesla.flash_lights(self.current_vehicle.id_s)
            if success:
                console.print("[green]✓ Фары мигнули 💡[/green]")
            else:
                console.print("[yellow]⚠ Не удалось мигнуть фарами[/yellow]")
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_ask(self, arg):
        """Спросить у AI о состоянии автомобиля"""
        if not arg:
            console.print("[red]✗ Введите вопрос[/red]")
            return
        
        if not self.ai:
            console.print("[red]✗ AI ассистент не настроен (нужен OPENAI_API_KEY)[/red]")
            return
        
        if not self.current_vehicle:
            console.print("[red]✗ Сначала выберите автомобиль[/red]")
            return
        
        try:
            with console.status("[bold cyan]Думаю...", spinner="dots"):
                state = self.tesla.get_vehicle_state(self.current_vehicle.id_s)
                response = self.ai.generate_response(arg, vehicle_context=state)
            
            console.print(Panel.fit(
                Markdown(response.content),
                title="🤖 AI Ответ",
                border_style="green"
            ))
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_chat(self, arg):
        """Поговорить с AI ассистентом"""
        if not arg:
            console.print("[red]✗ Введите сообщение[/red]")
            return
        
        if not self.ai:
            console.print("[red]✗ AI ассистент не настроен (нужен OPENAI_API_KEY)[/red]")
            return
        
        try:
            with console.status("[bold cyan]Думаю...", spinner="dots"):
                response = self.ai.generate_response(arg)
            
            console.print(Panel.fit(
                Markdown(response.content),
                title="🤖 AI",
                border_style="green"
            ))
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_advice(self, arg):
        """Получить рекомендации от AI"""
        if not self.ai:
            console.print("[red]✗ AI ассистент не настроен (нужен OPENAI_API_KEY)[/red]")
            return
        
        if not self.current_vehicle:
            console.print("[red]✗ Сначала выберите автомобиль[/red]")
            return
        
        try:
            with console.status("[bold cyan]Анализирую состояние...", spinner="dots"):
                state = self.tesla.get_vehicle_state(self.current_vehicle.id_s)
                advice = self.ai.get_advice(state)
            
            console.print(Panel.fit(
                Markdown(advice),
                title="💡 Рекомендации",
                border_style="yellow"
            ))
        except Exception as e:
            console.print(f"[red]✗ Ошибка: {e}[/red]")
    
    def do_exit(self, arg):
        """Выйти из программы"""
        console.print("[cyan]До свидания! 👋[/cyan]")
        return True
    
    def default(self, line):
        """Обработка неизвестных команд - попытка интерпретировать через AI"""
        if self.ai and line.strip():
            console.print("[yellow]Неизвестная команда. Пробую интерпретировать через AI...[/yellow]")
            try:
                if not self.current_vehicle:
                    console.print("[red]✗ Сначала выберите автомобиль[/red]")
                    return
                
                state = self.tesla.get_vehicle_state(self.current_vehicle.id_s)
                parsed = self.ai.parse_command(line, state)
                
                command = parsed.get("command")
                confidence = parsed.get("confidence", 0)
                
                if confidence > 0.7:
                    self._execute_parsed_command(command, parsed.get("parameters", {}))
                else:
                    console.print(f"[yellow]⚠ Низкая уверенность ({confidence:.2f}). Используйте явные команды.[/yellow]")
            except Exception as e:
                console.print(f"[red]✗ Ошибка: {e}[/red]")
        else:
            console.print(f"[red]✗ Неизвестная команда: {line}[/red]")
    
    def _execute_parsed_command(self, command: str, params: Dict[str, Any]):
        """Выполнить распарсенную команду"""
        commands = {
            'honk': lambda: self.tesla.honk_horn(self.current_vehicle.id_s),
            'lock': lambda: self.tesla.lock_doors(self.current_vehicle.id_s, lock=True),
            'unlock': lambda: self.tesla.lock_doors(self.current_vehicle.id_s, lock=False),
            'start_climate': lambda: self.tesla.start_climate(
                self.current_vehicle.id_s, 
                temperature=params.get('temperature', 22.0)
            ),
            'stop_climate': lambda: self.tesla.stop_climate(self.current_vehicle.id_s),
            'flash_lights': lambda: self.tesla.flash_lights(self.current_vehicle.id_s),
            'get_status': lambda: self.tesla.get_vehicle_summary(self.current_vehicle.id_s)
        }
        
        if command in commands:
            try:
                result = commands[command]()
                if isinstance(result, str):
                    console.print(result)
                elif result:
                    console.print(f"[green]✓ Команда '{command}' выполнена[/green]")
                else:
                    console.print(f"[yellow]⚠ Команда '{command}' не выполнена[/yellow]")
            except Exception as e:
                console.print(f"[red]✗ Ошибка выполнения: {e}[/red]")
        else:
            console.print(f"[yellow]⚠ Неизвестная команда: {command}[/yellow]")


def main():
    """Точка входа в приложение"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Tesla AI Assistant CLI")
    parser.add_argument("--token", help="Tesla API access token")
    parser.add_argument("--openai-key", help="OpenAI API key")
    parser.add_argument("--model", default="gpt-4", help="OpenAI model (default: gpt-4)")
    args = parser.parse_args()
    
    # Инициализация Tesla клиента
    if not args.token:
        console.print("[red]✗ Необходимо указать Tesla API токен[/red]")
        console.print("[cyan]Используйте: --token <ваш_токен>[/cyan]")
        console.print("[cyan]Или установите переменную окружения TESLA_ACCESS_TOKEN[/cyan]")
        sys.exit(1)
    
    tesla_client = TeslaAPIClient(access_token=args.token)
    
    # Инициализация AI ассистента (опционально)
    ai_assistant = None
    if args.openai_key or os.getenv("OPENAI_API_KEY"):
        try:
            ai_assistant = AIAssistant(
                api_key=args.openai_key or os.getenv("OPENAI_API_KEY"),
                model=args.model
            )
            console.print("[green]✓ AI ассистент подключен[/green]")
        except Exception as e:
            console.print(f"[yellow]⚠ AI ассистент не настроен: {e}[/yellow]")
    else:
        console.print("[yellow]⚠ AI ассистент отключен (нужен OPENAI_API_KEY)[/yellow]")
    
    # Запуск CLI
    try:
        cli = TeslaAICLI(tesla_client, ai_assistant)
        cli.cmdloop()
    except KeyboardInterrupt:
        console.print("\n[cyan]До свидания! 👋[/cyan]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[red]✗ Критическая ошибка: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()
