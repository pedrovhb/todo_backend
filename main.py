from typing import List

import uvicorn as uvicorn
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from database import *
from models import *

app = FastAPI()
origins = [
    "http://localhost:8000",
    "http://localhost:5000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/todo', response_model=TodoModel)
def get_todo(id_: str):
    try:
        todo = todo_collection.find_one({'_id': ObjectId(id_)})
    except InvalidId:
        raise HTTPException(400, f'Invalid ID {id_}')
    if not todo:
        raise HTTPException(404, f'No todo found with ID {id_}')
    return build_todo_object(todo)


@app.get('/all_todos', response_model=List[TodoModel])
def get_all_todos():
    results = todo_collection.find().limit(500)
    return [build_todo_object(result) for result in results]


@app.post('/todo/boolean', response_model=TodoBoolean)
def create_todo_boolean(todo: TodoBooleanIn):
    return TodoBoolean(id_=insert_todo_to_db(todo), **todo.dict())


@app.post('/todo/count', response_model=TodoCount)
def create_todo_count(todo: TodoCountIn):
    return TodoCount(id_=insert_todo_to_db(todo), **todo.dict())


@app.post('/todo/timer', response_model=TodoTimer)
def create_todo_timer(todo: TodoTimerIn):
    return TodoTimer(id_=insert_todo_to_db(todo), **todo.dict())


@app.patch('/todo', response_model=TodoModel)
def update_todo(todo: TodoModel):
    todo_dict = dict(type=todo_type_str_from_object(todo), **todo.dict(exclude={'id_'}))
    try:
        result = todo_collection.replace_one({'_id': ObjectId(todo.id_)}, todo_dict)
    except InvalidId:
        raise HTTPException(400, f'Invalid ID {todo.id_}')
    if result.matched_count != 1:
        raise HTTPException(404, f'No todo found with id {todo.id_}')
    return todo


@app.delete('/todo')
def delete_todo(id_: str):
    try:
        delete_result = todo_collection.delete_one({'_id': ObjectId(id_)})
    except InvalidId:
        raise HTTPException(400, f'Invalid ID {id_}')
    if delete_result.deleted_count != 1:
        raise HTTPException(404, f'No todo found with ID {id_}')
    return {'message': 'ok'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
