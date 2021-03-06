C_XMLRPC = None

try:
    import xmlrpclib
    C_XMLRPC = xmlrpclib.ServerProxy
except:
    import xmlrpc.client
    C_XMLRPC = xmlrpc.client.ServerProxy


class ResallocClientException(Exception):
    pass

class Ticket(object):
    id = None
    connection = None

    def __init__(self, connection=None):
        self.connection = connection

    def collect(self):
        output = self.connection.collectTicket(self.id)
        ready = output['ready']
        if ready:
            self.output = output['output']
        return ready

    def wait(self):
        return str(self.connection.waitTicket(self.id))

    def close(self):
        self.connection.closeTicket(self.id)


class Connection(object):
    connection = None

    def __init__(self, conn):
        self.connection = C_XMLRPC(conn)

    def newTicket(self, tags=None):
        if tags == None:
            raise ResallocClientException("no tags specified")

        t = Ticket(connection=self.connection)
        t.id = self.connection.takeTicket(tags)
        return t

    def getTicket(self, ticket_id):
        t = Ticket(connection=self.connection)
        t.id = ticket_id
        return t
