ALL_GLOBAL_DATA = {
    'Test': 'this is a test'
}

ALL_ENV_DATA = {
    'LOCAL': {
        'BASE_URL': 'http://localhost:8080/elements/api-v2',
        'IM_URL': 'http://localhost:8081/integrationmanager/api-v2',
        'USER_NAME': 'system',
        'PASSWORD': 'system',
        'ORG_SECRET': '218383cd8ec9242ffa0325187399cd79',
        'USER_SECRET': 'a33e1a7f2cf3df18a042982556cc907d',
        'TOKEN': {
            'SFCD': '',
            'DRY_FLY': '',
            'ELEMENTS': ''
            },
        'HEADER': {
            'IM_SESSION_ID': '',
            'Authentication': ''
            }
        },
    'LOCAL_IM': {
        'BASE_URL': 'http://localhost:8080/elements/api-v2',
        'IM_URL': 'http://localhost:8081/integrationmanager/api-v2',
        'USER_NAME': 'inspirato',
        'PASSWORD': 'inspirato',
        'ORG_SECRET': '218383cd8ec9242ffa0325187399cd79',
        'USER_SECRET': 'a33e1a7f2cf3df18a042982556cc907d',
        'TOKEN': {
            'SFCD': '',
            'DRY_FLY': '',
            'ELEMENTS': ''
            },
        'HEADER': {
            'IM_SESSION_ID': '',
            'Authentication': ''
            }
        },
        'SNAPSHOT_IM': {
        'BASE_URL': 'http://localhost:8080/elements/api-v2',
        'IM_URL': 'https://inspirato-im-snapshot.cloud-elements.com/integrationmanager/api-v2',
        'USER_NAME': 'im-qa@cloud-elements.com',
        'PASSWORD': 'password',
        'ORG_SECRET': '218383cd8ec9242ffa0325187399cd79',
        'USER_SECRET': 'a33e1a7f2cf3df18a042982556cc907d',
        'TOKEN': {
            'SFCD': '',
            'DRY_FLY': '',
            'ELEMENTS': ''
            },
        'HEADER': {
            'IM_SESSION_ID': '',
            'Authentication': ''
            }
        },
    'SNAPSHOT_IM_ADMIN': {
        'BASE_URL': 'http://localhost:8080/elements/api-v2',
        'IM_URL': 'https://inspirato-im-snapshot.cloud-elements.com/integrationmanager/api-v2',
        'USER_NAME': 'inspirato',
        'PASSWORD': 'inspirato',
        'ORG_SECRET': '218383cd8ec9242ffa0325187399cd79',
        'USER_SECRET': 'a33e1a7f2cf3df18a042982556cc907d',
        'TOKEN': {
            'SFCD': '',
            'DRY_FLY': '',
            'ELEMENTS': ''
            },
        'HEADER': {
            'IM_SESSION_ID': '',
            'Authentication': ''
            }
        },
    'QA_IM': {
        'BASE_URL': '',
        'IM_URL': 'https://inspirato-im-qa.cloud-elements.com/integrationmanager/api-v2',
        'USER_NAME': 'inspirato',
        'PASSWORD': 'inspirato',
        'ORG_SECRET': 'a33e1a7f2cf3df18a042982556cc907d',
        'USER_SECRET': '218383cd8ec9242ffa0325187399cd79',
        'TOKEN': {
            'SFCD': '',
            'DRY_FLY': '',
            'ELEMENTS': ''
            },
        'HEADER': {
            'IM_SESSION_ID': '',
            'Authentication': ''
            }
        }

}


def build_variables(environment):
    if environment == 'DEFAULT':
        environment = 'LOCAL'

    try:
        return dict(ALL_GLOBAL_DATA.items() + ALL_ENV_DATA[environment.upper()].items())
    except KeyError:
        print "Couldn't find %s environment, using default of LOCAL!" % environment.upper()
        return dict(ALL_GLOBAL_DATA.items() + ALL_ENV_DATA['LOCAL'].items())
