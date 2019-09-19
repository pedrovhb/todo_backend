# Todo

This is the back-end for a to-do app. It's written in Python and uses FastAPI and MongoDB.

The app has 3 kinds of to-do item models: 
* boolean, the traditional check/uncheck item
* count, a to-do item that has a target number and updates add to its count
* timer, a to-do item that has a target time and updates based on time spent on it