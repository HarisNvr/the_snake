# Игра "Змейка"

## Описание

Это простая графическая игра "Змейка", реализованная на языке Python. Вы управляете змейкой при помощи стрелок на клавиатуре, "поедая яблоки" вы увеличиваете длину змейки, "поедая себя" вы сбрасываете длину змейки до 1.

## Установка
- Убедитесь, что у вас установлен Python 3.6 или новее
- Склонируйте репозиторий:
```
git clone https://github.com/HarisNvr/the_snake.git
```
- Перейдите в директорию проекта:
```
cd the_snake
```
- Создайте и активируйте виртуальное окружение:
```
python -m venv venv
source venv/bin/activate
```
- Установите зависимости:
```
pip install -r requirements.txt
```

## Использование

- Запустите игру:
```
python the_snake.py
```

## Скорость игры:

- **В этой игре скорость змейки измеряется в кадрах в секунду (FPS - Frames Per Second). Базовая скорость игры задана значением 15 FPS, что означает, что игра обновляется 15 раз в секунду.**

Когда вы "поедаете яблоки" и увеличиваете длину змейки, её скорость также увеличивается в соответствии с таблицей ниже:

```
| Длина змейки  | Прибавка к базовой скорости  | Итоговая скорость (FPS) |
|---------------|------------------------------|-------------------------|
| 0-5           | 0                            | 15 FPS                  |
| 6-10          | 1                            | 16 FPS                  |
| 11-20         | 2                            | 17 FPS                  |
| 21-30         | 3                            | 18 FPS                  |
| 31-40         | 4                            | 19 FPS                  |
| 41-55         | 5                            | 20 FPS                  |
| 56-75         | 6                            | 21 FPS                  |
| 76-100        | 7                            | 22 FPS                  |
| 101-130       | 9                            | 24 FPS                  |
| 131-170       | 11                           | 26 FPS                  |
| 171-220       | 13                           | 28 FPS                  |
| 221-250       | 14                           | 29 FPS                  |
| 251-300       | 15                           | 30 FPS                  |
```
