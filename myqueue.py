import os
from twilio.rest import Client

class Line:
    def __init__(self):
        self.account_sid = ""
        self.auth_token = ""
        self.client = Client(self.account_sid, self.auth_token)
        self.name= ""
        self.phone =0
        self._queue = [{
            'name': 'Tom Wilson',
            'phone': '+56997730170'
        },
        {
            'name': 'Nelson Mandela',
            'phone': '+56997730170'

        }]
        self._mode = 'FIFO'
    def enqueue(self, item): # add user         
        message_add = self.client.messages.create(
            body="Welcome"+ item["name"] + "you have been added to the queue, you have: "+ str(self.size()) +" person(s) before you turn, we will inform you when it's your turn, thank you for choosing us",
            to = item["phone"],
            from_ = "+19715992774"
            )

        self._queue.append(item)
        return message_add
    def dequeue(self): # next route
        if len(self._queue)>0:
            message_now = self.client.messages.create(
                body="Mr/Mrs."+self._queue[0]['name']+", you are next, please approach to the counter",
                to = self._queue[0]['phone'],
                from_ = "+19715992774"
                )
            if len(self._queue)>1:
                message_next = self.client.messages.create(
                    body="Mr/Mrs."+self._queue[1]['name']+", there is only one turn before yours, please approach to the counter",
                    to = self._queue[1]['phone'],
                    from_ = "+19715992774"
                    )
            self._queue.pop(0)
       
        return self._queue

    def get_queue(self): # all route
        return self._queue
    def size(self):
        return len(self._queue)


# message_next = client.messages.create(
#             body="Usted es el siguiente",
#             to="+56997730170",
#             )

# message_add = client.messages.create(
#             body="Bienvenido, usted ha sido añadido a la fila, le informaremos cuando sea su turno",
#             to="+56997730170",
#             )

# print(message)