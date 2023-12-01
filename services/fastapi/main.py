# main.py
from typing import Optional

from fastapi import FastAPI

# Создание объекта приложения.
app = FastAPI()

# Декоратор, определяющий, что GET-запросы к основному URL приложения
# должны обрабатываться этой функцией.
@app.get('/', tags=['special methods', 'greetings'])
def read_root():
    return {'Hello': 'FastAPI'}


@app.get(
    '/{name}',
    tags=['common methods'],
    summary='Общее приветствие',
    response_description='Полная строка приветствия'
)
def user(name: str, surname: Optional[str] = None, age:  Optional[int] = None) -> dict[str, str]:
    return {'Hello': name}