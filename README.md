# Orchestrator
Alle processer har deres egen instans af Orchestrator klassen, og deler config information, der lader dem forbinde til samme RabbitMQ server på 'host' med 'exchange'. 

Ved forbindelse oprettes der en kø med grafens rolle-navn. Denne sørger for at ordne og sidenhen sende beskeder til den relevante graf.

I endpoint projektioner har events altid en modtager (eller modtagere, hvilket der i øjeblikket ikke tages hensyn til). En besked der skal executes kan derfor altid bare executes lokalt og sendes til den relevante queue.

Hvis vi antager at listen effekten tillæges samtlige events, lyttes der efter indkommende beskeder inden hver lokal event-udførsel. Hvad er en hensigtsmæssig prefetch, dette taget i betragtning??

# Forbedring?
Det kunne være lækkert at have graferne til at køre lokalt fremfor altid at skulle tilgå dem gennem api'en og effekter. Det introducerer unødvendig synkronicitet og det er for eksempel ikke muligt for en proces at lytte til indkommende beskeder (kunne man sætte listen som en effekt på samtlige events?).

# TODO
- [ ] Implementer rollback funktionalitet
- [ ] Hvordan håndteres opdatering af vector clocks?
- [ ] Funktionalitet for mere end en modtager
- [ ] Mere sofistikeret kausalitets begreb for at undgå unødvendige rollbacks 
- [ ] Test RabbitMQ setup lokalt
- [ ] Importer som effekt
- [ ] Lille run
- [ ] Stor run
- [ ] Performance benchmarking
- [ ] Rewrite i GO?