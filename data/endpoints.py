ALL_GLOBAL_DATA = {
    'authenticate'      : '/authentication/authenticate',
    'test'              : '/accounts/quotes/a5p190000008P7h',
    'authenticate_v2'   : {
        'url'       : '/authentication/authenticate',
        'params'    : {
            'userId'    : '{USER_NAME}',
            'password'  : '{PASSWORD}'
        },
        'header'    : {
            'Accept'    : 'application/json'
        },
        'data'      : ''
    }
}

ALL_ENV_DATA = {
    
    'LOCAL' : {}

}

def build_variables(environment):
    if environment == 'DEFAULT':
        environment = 'LOCAL'

    try:
        return dict(ALL_GLOBAL_DATA.items() + ALL_ENV_DATA[environment.upper()].items())
    except KeyError:
        print "Couldn't find %s endpoints, using default of LOCAL!" % environment.upper()
        return dict(ALL_GLOBAL_DATA.items() + ALL_ENV_DATA['LOCAL'].items())
