import os

from pymongo import MongoClient

from models import *

client = MongoClient('mongodb://localhost')

todo_collection = client.get_database('todo').get_collection('todos')

if os.getenv('TEST_FLAG'):
    todo_collection = client.get_database('todo_test').get_collection('todos')
    todo_collection.delete_many({})


def insert_todo_to_db(todo: TodoInModel) -> str:
    todo_type = todo_type_str_from_object(todo)
    result = todo_collection.insert_one(dict(type=todo_type, **todo.dict()))
    id_ = str(result.inserted_id)
    return id_


def build_todo_object(todo: dict) -> TodoModel:
    todo['id_'] = str(todo.pop('_id'))

    for cls in [TodoBoolean, TodoCount, TodoTimer]:
        if todo['type'] == cls.__name__:
            return cls(**todo)


def todo_type_str_from_object(todo_object: Union[TodoModel, TodoInModel]):
    todo_type = todo_object.__class__.__name__
    # If the class comes from an "In" model object, we want to take that out of the class name
    return todo_type.replace('In', '')
