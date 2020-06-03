import asyncio
from asyncua import Client, Node, ua

class SubscriptionHandler:
    """
    The SubscriptionHandler is used to handle the data that is received for the subscription.
    """
    def datachange_notification(self, node: Node, val, data):
        """
        Callback for asyncua Subscription.
        This method will be called when the Client received a data change message from the Server.
        """
        print('datachange_notification %r %s', node, val)

async def main():
    client = Client(url='opc.tcp://127.0.0.1:4840/test')
    async with client:
        idx = await client.get_namespace_index("http://andreas-heine.net/UA")
        handler = SubscriptionHandler()
        subscription = await client.create_subscription(100, handler)
        myobj = client.get_node("ns=2;i=1")
        nodes = await myobj.get_variables()
        await subscription.subscribe_data_change(nodes)

        while 1:
            await asyncio.sleep(0)

if __name__ == "__main__":
    asyncio.run(main())