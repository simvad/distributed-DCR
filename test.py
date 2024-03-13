import asyncio
import aio_pika

class Orchestrator:
    def __init__(self, host='0.0.0.0'):
        self.host = host
        self.connection = None
        self.channel = None
        self.queues = {}

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.host)
        self.channel = await self.connection.channel()

    async def subscribe(self, graph_id, sim_id, vector_clock, role, url):
        queue_name = role
        await self.channel.declare_queue(queue_name)
        await self.channel.set_qos(prefetch_count=1)
        await self.channel.bind_queue(queue_name, exchange_name='direct_exchange', routing_key=role)
        self.queues[role] = queue_name

    async def unsubscribe(self, role):
        if role in self.queues:
            queue_name = self.queues[role]
            await self.channel.delete_queue(queue_name)
            del self.queues[role]
        else:
            print(f"No queue found for role '{role}'")

    async def enqueue(self, sender_role, receiver_role_vector_clock, event_id):
        if receiver_role_vector_clock in self.queues:
            queue_name = self.queues[receiver_role_vector_clock]
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=event_id),
                routing_key=receiver_role_vector_clock
            )
            print(f"Event '{event_id}' enqueued in queue '{queue_name}'")
        else:
            print(f"No queue found for role '{receiver_role_vector_clock}'")

    async def execute(self, sender, receiver, event_id):
        if receiver in self.queues:
            queue_name = self.queues[receiver]
            await self.channel.default_exchange.publish(
                aio_pika.Message(body=event_id),
                routing_key=receiver
            )
            print(f"Event '{event_id}' sent to queue '{queue_name}' for execution")
        else:
            print(f"No queue found for role '{receiver}'")

    async def rollback(self, event_id, vector_clock):
        # Implement rollback logic here based on the vector clock
        print(f"Rollback triggered for event '{event_id}' with vector clock '{vector_clock}'")

    async def close_connection(self):
        if self.connection:
            await self.connection.close()
