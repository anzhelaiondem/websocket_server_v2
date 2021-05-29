import websockets
import asyncio
import config

from pyngrok import ngrok


async def client_handler(ws, path):
    try:
        while True:
            if await ws.recv():
                await ws.send("You are connected. Close the program to disconnect.")
    except (websockets.ConnectionClosedError, websockets.ConnectionClosedOK) as err:
        return err


async def producer_handler(ws, path):
    config.USERS.add(ws)
    config.logger.info(f"Client {ws.remote_address[:2]} is connected. Active clients N: {len(config.USERS)}")
    try:
        while True:
            msg = await calculating_ra_dec_of_moon()
            await ws.send(msg)
            await asyncio.sleep(config.SLEEP_TIME)
    except websockets.ConnectionClosedError as err:
        config.USERS.remove(ws)
        config.logger.info(f"Client {ws.remote_address[:2]} is disconnected. Active clients N: {len(config.USERS)}")
        config.logger.error(f"Client {ws.remote_address[:2]} has closed the connection: {err}")
    except websockets.ConnectionClosedOK as err:
        config.USERS.remove(ws)
        config.logger.info(f"Client {ws.remote_address[:2]} is disconnected. Active clients N: {len(config.USERS)}")
        config.logger.error(f"Client {ws.remote_address[:2]} has closed the connection: {err}")


async def handler(ws, path):
    request_task = asyncio.ensure_future(client_handler(ws, path))
    sender_task = asyncio.ensure_future(producer_handler(ws, path))
    done, pending = await asyncio.wait([request_task, sender_task], return_when=asyncio.ALL_COMPLETED, )
    for task in pending:
        task.cancel()


async def calculating_ra_dec_of_moon():
    m = 20 * 100 - 1 + 3904  # just for testing
    return f"Answer is: {m}"


def main():
    ng_url = ngrok.connect(config.PORT).public_url
    print(f"Ngrok tunnel address: ws{ng_url[4:]}")
    start_server = websockets.serve(handler, config.HOST, config.PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
