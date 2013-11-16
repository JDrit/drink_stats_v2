from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models import (
    DBSession,
    Base,
    )


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('index', '/')
    config.add_route('drink_page', '/drink/{item_id}')
    config.add_route('user_redirect', '/user')
    config.add_route('user_page', '/user/{username}')
    config.add_route('machine_page', '/machine/{machine_id}')

    config.add_route('api_item_usage', '/api/drink/{item_id}')
    config.add_route('api_user_usage', '/api/user/{username}')
    config.add_route('api_machine_usage', '/api/machine/{machine_id}')
    config.add_route('api_total_usage', '/api/total')
    config.add_route('api_pop_hours', '/api/hours')

    config.scan()
    return config.make_wsgi_app()
