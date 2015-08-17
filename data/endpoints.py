ALL_GLOBAL_DATA = {
    'authenticate': '/authentication/authenticate',
    'WOODII_930_1': '/accounts/8888/creditbalances',
    'WOODII_906_1': '/accounts/quotes/a5p190000008P7h',
    'WOODII_947_1': '/users/{}/sfdccontact',
    'WOODII_947_2': '/trips/proposals',
    'WOODII_908_1': '/destinations/{}/contacts',
    'Maintence_Flag': '/systemstatus',
    'Residence_R87': '/residences/R87',
    'v2_example': {
        'url': '',
        'url_vars': '',
        'method': '',
        'header': '',
        'params': '',
        'data': '',
        'tests': {
            'schemas': {
                'Valid_Schema': '',
                'ERROR_Schema': '',
                'ERROR_Schema_2': ''
            },
            'Other_Tests': ''
        },
        'functions': []
    },
    'WOODII_947_2_v2': {
        'url': '/trips/proposals',
        'method': 'POST',
        'header': {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        'data': '''{
                    "dryflyId": "90545",
                    "proposalCreatedBy": "",
                    "description": "trip proposal description",
                    "proposalSource": "Proactive",
                    "checkInDate": "2015-01-24",
                    "checkOutDate": "2015-01-31",
                    "flexible": "Yes",
                    "tripPurpose": "Holiday",
                    "status": "Open"
                }'''
    }
}

ALL_ENV_DATA = {
    'LOCAL': {}
}


def build_variables(environment):
    if environment == 'DEFAULT':
        environment = 'LOCAL'

    try:
        return dict(ALL_GLOBAL_DATA.items() + ALL_ENV_DATA[environment.upper()].items())
    except KeyError:
        print "Couldn't find %s endpoints, using default of LOCAL!" % environment.upper()
        return dict(ALL_GLOBAL_DATA.items() + ALL_ENV_DATA['LOCAL'].items())
