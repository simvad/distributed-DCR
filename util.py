import requests
from pprint import pprint
import json

acc_codes = {200,201,202,203,204}

def api_call(url, method,json = None):
    headers = {
        'Content-Type': 'application/json'
    }
    username = 'mth311@alumni.ku.dk'
    password = open('pw.txt', 'r').read().strip()
    if method not in ['GET', 'POST', 'PUT', 'DELETE']:
        raise ValueError('Invalid method')
    response = requests.request(method, url, headers=headers, auth=(username, password),json=json)
    #pprint(f'Status code:{response.status_code}')
    #pprint(f'Response text:{response.text}')
    #pprint(f'Response headers:{response.headers}')
    return response

class VectorClock:
    def __init__(self, role, vector=None):
        if vector is None:
            self.clock = {role: 0}
        else:
            self.clock = vector.copy()
            if role not in self.clock:
                self.clock[role] = 0

    def increment(self, role):
        if role in self.clock:
            self.clock[role] += 1
        else:
            self.clock[role] = 1

    def merge(self, other):
        for role in other.clock:
            if role in self.clock:
                self.clock[role] = max(self.clock[role], other.clock[role])
            else:
                self.clock[role] = other.clock[role]
        for role in self.clock:
            if role not in other.clock:
                other.clock[role] = self.clock[role]

    # Returns true if other happened after self at role
    def happened_after(self, other, role):
        if role in self.clock and role in other.clock:
            return other.clock[role] > self.clock[role]
        elif role in other.clock:
            return True
        else:
            return False
    
    def get(self):
        return self.clock

    def __str__(self):
        return str(self.clock)

#Is this the only needed information?
def serialize_event(event_id, vector_clock):
    return json.dumps({'event_id': event_id, 'vector_clock': vector_clock.get()})
