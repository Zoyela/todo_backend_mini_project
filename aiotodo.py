from aiohttp import web
from dbhelper import create_db_connection
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from todosAndTags import Todo
from sqlalchemy import func
import aiohttp_cors


TODOS = [
    {'title': 'build an API', 'order': 1, 'completed': False},
    {'title': '?????', 'order': 2, 'completed': False},
    {'title': 'profit!', 'order': 3, 'completed': False}
]


def get_all_todos(request):
    session = request.app['session']()
    todo_list = session.query(Todo).all()

    return web.json_response([todo.to_dictionary() for todo in todo_list])


def remove_all_todos(request):
    session = request.app['session']()
    todo_list = session.query(Todo).all()
    for todo in todo_list:
        session.delete(todo)
    session.commit()
    return web.Response(status=204)


def get_one_todo(request):
    id = int(request.match_info['id'])

    session = request.app['session']()
    try:
        todo = session.query(Todo).filter_by(id=id).one()
    except MultipleResultsFound:
        return web.json_response({
            'error': 'Found multiple todos with given id, not just one as expected'
        }, status=500)
    except NoResultFound:
        return web.json_response({
            'error': 'Found no todo with the given id'
        }, status=404)

    return web.json_response(todo.to_dictionary(), status=200)


# todo
async def create_todo(request):
    session = request.app['session']()
    data = await request.json()

    if not 'title' in data:
        return web.json_response({'error': '"title" is a required field'})
    title = data['title']
    if not isinstance(title, str) or not len(title):
        return web.json_response({'error': '"title" must be a string with at least one character'})

    data['completed'] = bool(data.get('completed', False))
    new_place_number = session.query(func.max(Todo.placeNumber)).first()[0] + 1
    data['placeNumber'] = int(data.get('placeNumber', new_place_number))

    todo = Todo(title=data['title'], placeNumber=data['placeNumber'], completed=data['completed'])
    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=todo.id)))
    session.add(todo)
    session.commit()

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )


async def update_todo(request):
    id = int(request.match_info['id'])

    if id >= len(TODOS):
        return web.json_response({'error': 'Todo not found'}, status=404)

    data = await request.json()
    TODOS[id].update(data)

    return web.json_response(TODOS[id])


def remove_todo(request):
    id = int(request.match_info['id'])

    if id >= len(TODOS):
        return web.json_response({'error': 'Todo not found'})

    del TODOS[id]

    return web.Response(status=204)


def app_factory(args=()):
    app = web.Application()

    # Configure default CORS settings.
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True,
                expose_headers="*",
                allow_headers="*",
            )
    })

    app.on_startup.append(create_db_connection)

    cors.add(app.router.add_get('/todos/', get_all_todos, name='all_todos'))
    cors.add(app.router.add_delete('/todos/', remove_all_todos, name='remove_todos'))
    cors.add(app.router.add_post('/todos/', create_todo, name='create_todo'))
    cors.add(app.router.add_get('/todos/{id:\d+}', get_one_todo, name='one_todo'))
    cors.add(app.router.add_patch('/todos/{id:\d+}', update_todo, name='update_todo'))
    cors.add(app.router.add_delete('/todos/{id:\d+}', remove_todo, name='remove_todo'))


    #cors.add(app.router.add.get('/tags/', get_all_tags, name='all_tags'))
    #cors.add(app.router.add.post('/tags/', create_tag, name='create_tag'))
    #cors.add(app.router.add.get('/tags/{id:\d+}', get_all_tags, name='all_tags'))
    #cors.add(app.router.add.put('/tags/{id:\d+}', put_tag, name='put_tag'))
    #cors.add(app.router.add.delete('/tags/{id:\d+}', delete_tag, name='delete_tag'))

    return app


# Tags
# List all tags GET /tags/
# Create a tag POST /tags/
# Fetch a tag GET /tags/:tag_id
# Update a tag PUT /tags/:tag_id
# Delete a tag DELETE /tags/:tag_id
# Todos
# List all todos with a specific tag GET /todos/?tag=:tag_id
# List all tags of a todo_ GET /todos/:todo_id/tags/
# Tag a todo_ POST /todos/:todo_id/tags/
# Remove a tag DELETE /todos/:todo_id/tags/:tag_id
