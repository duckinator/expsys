from datetime import datetime
from freezegun import freeze_time  # type: ignore
from expsys.inference_engine import InferenceEngine


def test_main(): # pylint: disable=too-many-statements
    agents = {
        'sunday': {'type': 'strftime', 'format': '%a', 'match': 'Sun'},
        'monday': {'type': 'strftime', 'format': '%a', 'match': 'Mon'},
        'tuesday': {'type': 'strftime', 'format': '%a', 'match': 'Tue'},
        'wednesday': {'type': 'strftime', 'format': '%a', 'match': 'Wed'},
        'thursday': {'type': 'strftime', 'format': '%a', 'match': 'Thu'},
        'friday': {'type': 'strftime', 'format': '%a', 'match': 'Fri'},
        'saturday': {'type': 'strftime', 'format': '%a', 'match': 'Sat'},
        'first_7_days': {
            'type': 'datetime_range',
            'attr': 'day',
            'range': [1, 8],
        },
        'second_7_days': {
            'type': 'datetime_range',
            'attr': 'day',
            'range': [8, 15],
        },
        'third_7_days': {
            'type': 'datetime_range',
            'attr': 'day',
            'range': [15, 22],
        },
        'fourth_7_days': {
            'type': 'datetime_range',
            'attr': 'day',
            'range': [22, 29],
        },
        'fifth_7_days': {
            'type': 'datetime_range',
            'attr': 'day',
            'range': [28, 32],
        },
    }

    rules = {
        "1st Saturday of every month": 'saturday & first_7_days',
        "2nd Saturday of every month": 'saturday & second_7_days',
        "3rd Saturday of every month": 'saturday & third_7_days',
        "4th Saturday of every month": 'saturday & fourth_7_days',
        "5th Saturday of every month": 'saturday & fifth_7_days',

        "1st Wednesday of every month": 'wednesday & first_7_days',
        "2nd Wednesday of every month": 'wednesday & second_7_days',
        "3rd Wednesday of every month": 'wednesday & third_7_days',
        "4th Wednesday of every month": 'wednesday & fourth_7_days',
        "5th Wednesday of every month": 'wednesday & fifth_7_days',
    }

    inf = InferenceEngine(agents, rules)

    with freeze_time('2020-08-02'): # First Sunday -- matches nothing
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-02'
        assert not inf['saturday']
        assert not inf['wednesday']
        assert not inf['1st Saturday of every month']
        assert not inf['2nd Saturday of every month']
        assert not inf['3rd Saturday of every month']
        assert not inf['4th Saturday of every month']
        assert not inf['5th Saturday of every month']
        assert not inf['1st Wednesday of every month']
        assert not inf['2nd Wednesday of every month']
        assert not inf['3rd Wednesday of every month']
        assert not inf['4th Wednesday of every month']
        assert not inf['5th Wednesday of every month']

    with freeze_time('2020-08-01'): # First Saturday
        inf.expire()
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-01'
        assert     inf['1st Saturday of every month']
        assert not inf['2nd Saturday of every month']
        assert not inf['3rd Saturday of every month']
        assert not inf['4th Saturday of every month']
        assert not inf['5th Saturday of every month']
        assert not inf['wednesday']

    with freeze_time('2020-08-08'): # Second Saturday
        inf.expire()
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-08'
        assert not inf['1st Saturday of every month']
        assert     inf['2nd Saturday of every month']
        assert not inf['3rd Saturday of every month']
        assert not inf['4th Saturday of every month']
        assert not inf['5th Saturday of every month']
        assert not inf['wednesday']

    with freeze_time('2020-08-15'): # Third Saturday
        inf.expire()
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-15'
        assert not inf['1st Saturday of every month']
        assert not inf['2nd Saturday of every month']
        assert     inf['3rd Saturday of every month']
        assert not inf['4th Saturday of every month']
        assert not inf['5th Saturday of every month']
        assert not inf['wednesday']

    with freeze_time('2020-08-22'): # Fourth Saturday
        inf.expire()
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-22'
        assert not inf['1st Saturday of every month']
        assert not inf['2nd Saturday of every month']
        assert not inf['3rd Saturday of every month']
        assert     inf['4th Saturday of every month']
        assert not inf['5th Saturday of every month']
        assert not inf['wednesday']

    with freeze_time('2020-08-29'): # Fifth Saturday
        inf.expire()
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-29'
        assert not inf['1st Saturday of every month']
        assert not inf['2nd Saturday of every month']
        assert not inf['3rd Saturday of every month']
        assert not inf['4th Saturday of every month']
        assert     inf['5th Saturday of every month']
        assert not inf['wednesday']


    with freeze_time('2020-08-05'): # First Wednesday
        inf.expire()
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-05'
        assert     inf['1st Wednesday of every month']
        assert not inf['2nd Wednesday of every month']
        assert not inf['3rd Wednesday of every month']
        assert not inf['4th Wednesday of every month']
        assert not inf['5th Wednesday of every month']
        assert not inf['saturday']

    with freeze_time('2020-08-12'): # Second Wednesday
        inf.expire()
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-12'
        assert not inf['1st Wednesday of every month']
        assert     inf['2nd Wednesday of every month']
        assert not inf['3rd Wednesday of every month']
        assert not inf['4th Wednesday of every month']
        assert not inf['5th Wednesday of every month']
        assert not inf['saturday']

    with freeze_time('2020-08-19'): # Third Wednesday
        inf.expire()
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-19'
        assert not inf['1st Wednesday of every month']
        assert not inf['2nd Wednesday of every month']
        assert     inf['3rd Wednesday of every month']
        assert not inf['4th Wednesday of every month']
        assert not inf['5th Wednesday of every month']
        assert not inf['saturday']

    with freeze_time('2020-08-26'): # Fourth Wednesday
        inf.expire()
        assert datetime.now().strftime('%Y-%m-%d') == '2020-08-26'
        assert not inf['1st Wednesday of every month']
        assert not inf['2nd Wednesday of every month']
        assert not inf['3rd Wednesday of every month']
        assert     inf['4th Wednesday of every month']
        assert not inf['5th Wednesday of every month']
        assert not inf['saturday']
