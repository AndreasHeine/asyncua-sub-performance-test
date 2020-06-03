import asyncio, random
from asyncua import ua, Server

async def main():
    server = Server()
    await server.init()
    server.set_endpoint("opc.tcp://127.0.0.1:4840/test")
    idx = await server.register_namespace("http://andreas-heine.net/UA")
    obj = server.get_objects_node()
    
    """
    setup test namespace
    """
    myobj = await obj.add_object(idx, "myOBJ")
    var_list = []
    for i in range(1000):
        var = await myobj.add_variable(ua.NodeId.from_string(f'ns={idx};s=DB_DATA.Test.var{i}'), f'Test.var{i}', 0)
        await var.set_writable(True)
        var_list.append(var)


    async with server:
        while 1:
            for each in var_list:
                await each.set_value(random.randint(1,100))
                await asyncio.sleep(0.001)
            await asyncio.sleep(0)
            
if __name__ == "__main__":
    asyncio.run(main())
