from fastapi import FastAPI, HTTPException
import asyncio
import pika
from fastapi import FastAPI, HTTPException
import import requests
import json
import asyncio
from util import *
import uvicorn

app = FastAPI()

# Initialize RabbitMQ connection and channel
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='messages')

# Function to send a message to RabbitMQ
def send_message(message):
    channel.basic_publish(exchange='', routing_key='messages', body=message)

@app.post("/send_message")
async def send_message_route(message: str):
    # Send message to RabbitMQ
    send_message(message)
    return {"message": "Message sent successfully!"}

graphs = set() #Set of graph objects
queues = {} #Dictionary of queues. Queue is asyncio FIFO queues of (graph, event_id, vectorclock) tuples


#Subscribes simulation with sim_id to all transactions w. recipient role
@app.post("/subscribe/{graph}")
async def subscribe(graph):
    simulations.add(graph)
    #Add a queue for the recipient in the queues dictionary
    if graph.role not in queues:
        queues[role] = asyncio.Queue() 

@app.post("/unsubscribe/{graph}")
async def unsubscribe(graph):
    simulations.remove(graph)
    #Remove the queue for the recipient-- Should I delete the queue or let it be
    if role in queues:
        del queues[role]

@app.get("/get_graphs/{role}")
async def get_graphs(role):
    return {graph for graph in graphs if graph.role == role}


@app.post("/enqueue/{graph}/{event_id}")
async def enqueue(graph, event_id):
    await queue.put((graph, event_id))

#rollback event_id initiated by role and all events with vc[role]
@app.post("/rollback/{graph}/{event_id}")
async def rollback(graph, event_id):
    #iterate through all events in all queues and remove all events that happened after event_id
    for queue in queues:
        for event in queue:
            if event[1] > event_id:
                queue.remove(event)

@app.post("/execute/{graph}/{event_id}")
async def execute(graph,event_id,note=''):
    url = f'https://repository.dcrgraphs.net/api/graphs/{graph.graph_id}/sims/{graph.sim_id}/events/{event_id}?filter={note}'
    response = api_call(url, 'POST')
    #return status code of the response
    return response.status_code 


# Function to gracefully close RabbitMQ connection when application exits
@app.on_event("shutdown")
async def shutdown_event():
    connection.close()

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
