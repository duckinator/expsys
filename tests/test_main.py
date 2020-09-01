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
        'day_1_to_7': {'type': 'date_range', 'attr': 'day', 'range': [1, 8]},
        'day_8_to_14': {'type': 'date_range', 'attr': 'day', 'range': [8, 15]},
        'day_15_to_21': {'type': 'date_range', 'attr': 'day', 'range': [15, 22]},
        'day_22_to_28': {'type': 'date_range', 'attr': 'day', 'range': [22, 29]},
        'day_29_to_31': {'type': 'date_range', 'attr': 'day', 'range': [29, 32]},
    }

    rules = {
        "1st Saturday of every month": 'saturday & day_1_to_7',
        "2nd Saturday of every month": 'saturday & day_8_to_14',
        "3rd Saturday of every month": 'saturday & day_15_to_21',
        "4th Saturday of every month": 'saturday & day_22_to_28',
        "5th Saturday of every month": 'saturday & day_29_to_31',

        "1st Wednesday of every month": 'wednesday & day_1_to_7',
        "2nd Wednesday of every month": 'wednesday & day_8_to_14',
        "3rd Wednesday of every month": 'wednesday & day_15_to_21',
        "4th Wednesday of every month": 'wednesday & day_22_to_28',
        "5th Wednesday of every month": 'wednesday & day_29_to_31',
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
