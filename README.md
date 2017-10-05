# todobackend-aiohttp

Yet another [todo backend](http://todobackend.com) written in Python 3.5 with aiohttp. Original code [from alec.thoughts import \*](http://justanr.github.io/getting-start-with-aiohttpweb-a-todo-tutorial).

## Usage

Before starting the app, or if you want to redo the tables:
```
python3 sqlalchemy_insert.py
```


To start the app:
```
python3 -m aiohttp.web -P 8080 aiotodo:app_factory
```

## Tests

You can run validate the application with http://www.todobackend.com/specs/.
