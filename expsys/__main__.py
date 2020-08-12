from time import sleep

from .inference_engine import InferenceEngine

# pylint: disable=line-too-long,suppressed-message,useless-suppression

agents = {
    'domain_resolves':     {'type':'dns', 'domain':'parts.horse'},
    'website_up':          {'type':'http', 'url':'https://parts.horse'},
    'search_up':           {'type':'http', 'url':'https://parts.horse/search?q=attiny', 'contents':'ATtiny2313'},
    'ssh_echo':            {'type':'ssh', 'dest':'freebsd@parts.horse', 'cmd':'echo -n'},
    'website_up_local':    {'type':'ssh', 'dest':'freebsd@parts.horse', 'cmd':'curl https://parts.horse'},
    'search_up_local':     {'type':'ssh', 'dest':'freebsd@parts.horse', 'cmd':'curl https://parts.horse/search?q=attiny'},
    'elasticsearch_network': {'type':'ssh', 'dest':'freebsd@parts.horse', 'cmd':'curl localhost:9200/_stats'},
    'elasticsearch_process': {'type':'ssh', 'dest':'freebsd@parts.horse', 'cmd':'pgrep -u elasticsearch java'},
}

rules = {
    'dns_failure':            '!domain_resolves',
    'server_inaccessible':    '!website_up & !ssh_echo',
    'server_up_website_down': '!website_up &  ssh_echo',
    'website_up_search_down': ' website_up & !search_up',
    'elasticsearch_down':     '!elasticsearch_process | !elasticsearch_network',
    'search_down_python_app': 'website_up & !search_up_local & !elasticsearch_down',
    'website_only_local':     '!website_up & website_up_local',
}


watch = {
    'dns_failure': 'Domain does not resolve.',
    'server_inaccessible': 'Server inaccessible.',
    'server_up_website_down': 'Website is down, but server is accessible.',
    'elasticsearch_down': 'Elasticsearch is malfunctioning. (Likely affects search.)',
    'search_down_python_app': 'Search is down, likely due to the Python app.',
    'website_only_local': 'The website down, but accessible from the server it\'s hosted on.',
}

inf = InferenceEngine(agents, rules)


def wait(delay):
    for i in range(0, delay):
        print(f'\rWaiting {delay - i} seconds...', end='')
        sleep(1)
    print('')


while True:
    print(chr(27) + "c", end="")
    for name in watch:
        status = inf[name]
        if not status:
            print(f'[OKAY] {name}')
        else:
            print(f'[FAIL] {name}')

    wait(5)
