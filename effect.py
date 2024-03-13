from util import *
import requests

service_url = "http://0.0.0.0:8000"  # Is there a better way to get this than hardcoding it?

#Do I have access to the event_id when executing the event/effect?
def execute(event_id):
    #How do I get the graph_id and sim_id via api call?
    graph_id = ?
    sim_id = ?
    role = #If I have the event_id, I can get the role from the event
    #Make a call to service.py to get the graph object with role=role
    graphs = requests.get(f'{service_url}/get_graphs/{role}')
    for graph in graphs:
        url = f'{service_url}/execute/{graph}/{event_id}'
        if requests.request('POST', url) not in acc_codes: # TEST THE CODE FOR SUCCESFUL EXECUTION
            requests.request('POST', f'{service_url}/rollback/{graph}/{event_id}')
            break   

    