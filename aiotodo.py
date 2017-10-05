from aiohttp import web
from dbhelper import create_db_connection
from sqlalchemy.orm.exc import MultipleResultsFound, NoResultFound
from todos_and_tags import Todo, Tag
from sqlalchemy import func
import aiohttp_cors


def get_all_todos(request):
    session = request.app['session']()

    if 'tag' in request.query:
        try:
            tag = session.query(Tag).filter_by(id=request.query['tag']).one()
        except MultipleResultsFound:
            return web.json_response({
                'error': 'Found multiple tags with given id, not just one as expected'
            }, status=500)
        except NoResultFound:
            return web.json_response({
                'error': 'Found no tag with the given id'
            }, status=404)
        todo_list = tag.todos
    else:
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
    session = request.app['session']()
    data = await request.json()

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

    if 'title' in data:
        todo.title = data['title']

    if 'placeNumber' in data:
        todo.title = data['placeNumber']

    if 'completed' in data:
        todo.title = data['completed']

    session.commit()

    return web.json_response(todo.to_dictionary(), status=200)


def remove_todo(request):
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

    session.delete(todo)
    session.commit()

    return web.json_response(status=204)


def get_all_tags(request):
    session = request.app['session']()
    tag_list = session.query(Tag).all()

    return web.json_response([tag.to_dictionary() for tag in tag_list])


async def create_tag(request):
    session = request.app['session']()
    data = await request.json()

    if not 'name' in data:
        return web.json_response({'error': '"name" is a required field'})
    name = data['name']
    if not isinstance(name, str) or not len(name):
        return web.json_response({'error': '"name" must be a string with at least one character'})

    tag = Tag(name=name)

    data['url'] = str(request.url.join(request.app.router['one_todo'].url_for(id=tag.id)))

    session.add(tag)
    session.commit()

    return web.Response(
        headers={'Location': data['url']},
        status=303
    )


def get_one_tag(request):
    id = int(request.match_info['id'])

    session = request.app['session']()
    try:
        tag = session.query(Tag).filter_by(id=id).one()
    except MultipleResultsFound:
        return web.json_response({
            'error': 'Found multiple tags with given id, not just one as expected'
        }, status=500)
    except NoResultFound:
        return web.json_response({
            'error': 'Found no tag with the given id'
        }, status=404)

    return web.json_response(tag.to_dictionary(), status=200)


async def update_tag(request):
    id = int(request.match_info['id'])
    session = request.app['session']()
    data = await request.json()

    try:
        tag = session.query(Tag).filter_by(id=id).one()
    except MultipleResultsFound:
        return web.json_response({
            'error': 'Found multiple tags with given id, not just one as expected'
        }, status=500)
    except NoResultFound:
        return web.json_response({
            'error': 'Found no tag with the given id'
        }, status=404)

    if 'name' in data:
        tag.name = data['name']

    session.commit()

    return web.json_response(tag.to_dictionary(), status=200)


def remove_tag(request):
    id = int(request.match_info['id'])
    session = request.app['session']()

    try:
        tag = session.query(Tag).filter_by(id=id).one()
    except MultipleResultsFound:
        return web.json_response({
            'error': 'Found multiple tag with given id, not just one as expected'
        }, status=500)
    except NoResultFound:
        return web.json_response({
            'error': 'Found no tag with the given id'
        }, status=404)

    session.delete(tag)
    session.commit()

    return web.json_response(status=204)

# /todos/{id:\d+}/tags/
def get_todo_tags(request):
    id=int(request.match_info['id'])
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

    return web.json_response([tag.to_dictionary() for tag in todo.tags], status=200)


async def add_todo_tag(request):
    id=int(request.match_info['id'])
    session = request.app['session']()
    data = await request.json()

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

    try:
        tag = session.query(Tag).filter_by(id=data['id']).one()
    except MultipleResultsFound:
        return web.json_response({
            'error': 'Found multiple tags with given id, not just one as expected'
        }, status=500)
    except NoResultFound:
        return web.json_response({
            'error': 'Found no tag with the given id'
        }, status=404)

    todo.tags.append(tag)

    session.commit()

    return web.json_response(todo.to_dictionary(), status=200)


async def delete_todo_tag(request):
    todo_id=int(request.match_info['todo_id'])
    tag_id=int(request.match_info['tag_id'])
    session = request.app['session']()

    try:
        todo = session.query(Todo).filter_by(id=todo_id).one()
    except MultipleResultsFound:
        return web.json_response({
            'error': 'Found multiple todos with given id, not just one as expected'
        }, status=500)
    except NoResultFound:
        return web.json_response({
            'error': 'Found no todo with the given id'
        }, status=404)

    try:
        tag = session.query(Tag).filter_by(id=tag_id).one()
    except MultipleResultsFound:
        return web.json_response({
            'error': 'Found multiple tags with given id, not just one as expected'
        }, status=500)
    except NoResultFound:
        return web.json_response({
            'error': 'Found no tag with the given id'
        }, status=404)

    todo.tags.remove(tag)

    session.commit()

    return web.json_response(todo.to_dictionary(), status=200)


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

    cors.add(app.router.add_get('/tags/', get_all_tags, name='all_tags'))
    cors.add(app.router.add_post('/tags/', create_tag, name='create_tag'))
    cors.add(app.router.add_get('/tags/{id:\d+}', get_one_tag, name='one_tag'))
    cors.add(app.router.add_patch('/tags/{id:\d+}', update_tag, name='update_tag'))
    cors.add(app.router.add_delete('/tags/{id:\d+}', remove_tag, name='remove_tag'))

    cors.add(app.router.add_get('/todos/{id:\d+}/tags/', get_todo_tags, name='get_todo_tags'))
    cors.add(app.router.add_post('/todos/{id:\d+}/tags/', add_todo_tag, name='add_todo_tag'))
    cors.add(app.router.add_delete('/todos/{todo_id:\d+}/tags/{tag_id:\d+}', delete_todo_tag, name='delete_todo_tag'))


    return app


# Tags
# List all tags GET /tags/ ok
# Create a tag POST /tags/ ok
# Fetch a tag GET /tags/:tag_id ok
# Update a tag PUT /tags/:tag_id ok
# Delete a tag DELETE /tags/:tag_id ok

# Todo
# List all todos with a specific tag GET /todos/?tag=:tag_id ok
# List all tags of a todo_ GET /todos/:todo_id/tags/ ok
# Tag a todo_ POST /todos/:todo_id/tags/ ok

# Remove a tag DELETE /todos/:todo_id/tags/:tag_id
