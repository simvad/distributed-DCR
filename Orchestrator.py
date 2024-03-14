import asyncio
import aio_pika
from util import *

#Stuff that might benefit from being in a config file
config = {
    'host': 'localhost',
    'prefetch_count': 1,
    'exchange': ''
}

class Orchestrator:
    def __init__(self, host=config['host']):
        self.host = host
        self.connection = None
        self.channel = None
        self.graphs = set()
        self.rolled_back = set() #Set of rolled back events by their vector clock

    #Does this need to be async? Does it even need to be a method, or can it just be part of setup
    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.host)
        self.channel = await self.connection.channel() #Should I use more than 1 channel?

    # Adds the graph to the set of known graphs, and creates a queue for the recipient role
    async def subscribe(self, graph_id, sim_id, vector_clock, role):
        await self.channel.declare_queue(role)
        await self.channel.set_qos(prefetch_count=1)
        await self.channel.bind_queue(queue_name, exchange_name=config[exchange] , routing_key=role) #Default exchange means routing_key = queue_name, which I think makes the key irrelevant 
         #Is it necessary to store everything here? What about address of the sender?
        self.graphs.add((graph_id, sim_id, vector_clock, role))

    # Removes the graph from the set of known graphs, and deletes the queue for the recipient role
    async def unsubscribe(self, role):
        await self.channel.delete_queue(role)
        self.graphs.remove(role)

    # Sends the event_id to the recipient queue -- Where should the 
    async def execute(self receiver, event_id, vector_clock):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=serialize_event(event_id, vector_clock), 
            routing_key=receiver))     

    # Filters the sent message based the set of rolled back events (if a sent message is causally related to a rolled back event, it should be nack'd) and added to the rolled back events
    def callback(ch, method, properties, body):
        #deserialize the message
        message = json.loads(body)
        event_id = message['event_id']
        vector_clock = VectorClock(message['vector_clock'])
        #Check if the message is causally related to a rolled back event
        for rolled_back in self.rolled_back:
            if vector_clock.happened_after(rolled_back, receiver):
                ch.nack(delivery_tag=method.delivery_tag)
                self.rolled_back.add(vector_clock)
            else:
                ch.ack(delivery_tag=method.delivery_tag)

    async def consume(self, queue_name, callback):
        await self.channel.declare_queue(queue_name)
        await self.channel.consume(callback, queue_name)

    async def close_connection(self):
        if self.connection:
            await self.connection.close()
