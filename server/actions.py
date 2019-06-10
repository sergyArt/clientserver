from settings import INSTALLED_APPS
from functools import reduce

def get_server_actions():
    return reduce(
        lambda value, item: value + getattr(item, 'actionnames', []),
        reduce(
            lambda value, item: value + [getattr(item, 'actions', [])],
            reduce(
                lambda value, item: value + [__import__(f'{item}.actions')],
                INSTALLED_APPS,
                []
            ),
            []
        ),
        []
    )

def resolve(action_name, actions=None):
    action_list =  actions or get_server_actions()
    action_mapping = {
        action.get('action'): action.get('controller')
        for action in action_list
    }
    return action_mapping.get(action_name)
