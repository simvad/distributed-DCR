import asyncio
import aio_pika
import requests
import json
from util import *
from Orchestrator import Orchestrator

#There must be a way to get these from the local graph as an effect
graph_id = ?
sim_id = ?
role = ?

#I may just do this manually or in a setup script along with the other setup
async def setup():
    orchestrator = Orchestrator()
    await orchestrator.connect()
    await orchestrator.subscribe(graph_id, sim_id, VectorClock(), role)
    
#Do I have access to the event_id when executing the event/effect?
def execute(event_id)
    listen()
    Orchestrator.execute('role', 'event_id', VectorClock())

def listen():
    await msg = orchestrator.consume(role, orchestrator.callback)
    #deserialize the message
    message = json.loads(msg)
    event_id = message['event_id']
    vector_clock = VectorClock(message['vector_clock'])
    url = f'https://repository.dcrgraphs.net/api/graphs/{graph_id}/sims/{sim_id}/events/{event_id}'
    if api_call(url, 'PUT').status_code == 200:
        #execute the effect
        #update the vector clock
        vector_clock.increment(role)
        #How do I send the updated vector clock to the orchestrator?
    else:
        #Rollback -- BUT HOW?
        
        

