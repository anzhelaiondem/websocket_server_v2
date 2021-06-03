import websockets
import asyncio
import config

from pyngrok import ngrok


async def sleep(websocket):
    """This function implements 10 seconds sleeping effect (the SLEEP_TIME is fixed in the config.py)
     and every second checks the connectivity of the client (websocket)."""
    t = 1
    while t <= config.SLEEP_TIME:
        await asyncio.sleep(1)
        await websocket.send("")
        t += 1


async def calculate_and_send_moon_ra_dec(websocket):
    """The function calculates the difference of time between the time point, calculates the RA 
    and the DEC of the Moon (based on the difference), sends it to the client, sleeps for mentioned
    amount of time and again repeats the cycle unless the client closes the connection."""
    new_ra = config.FIX_RA_IN_SEC
    new_dec = config.FIX_DEC_IN_SEC
    start_date = config.START_DATE
    while True:
        time_in_seconds = int((config.dt.datetime.now() - start_date).total_seconds())
        start_date = config.dt.datetime.now()
        for sec in range(time_in_seconds):
            new_ra = new_ra + config.AV_CHANGE_OF_M_RA_S
            if new_ra > 86399:
                new_ra = new_ra % 86399
            if 18 * 3600 < new_ra < 24 * 3600 or 0 < new_ra < 6 * 3600:
                new_dec = new_dec + config.AV_CHANGE_OF_M_DEC_S
            elif 6 * 3600 <= new_ra <= 18 * 3600:
                new_dec = new_dec - config.AV_CHANGE_OF_M_DEC_S
        ra = f'{(int(new_ra // 3600))}:{int((new_ra % 3600) // 60)}:{int((new_ra % 3600) % 60)}'
        dec = f'{int(new_dec // 3600)}° {int((new_dec % 3600) // 60)}′ {int((new_dec % 3600) % 60)}′′'
        await websocket.send(f"RA {ra}  DEC {dec}")
        await sleep(websocket)


async def producer_handler(websocket, path) -> None:
    """The function starts actively listening to any websocket client that connects to the websocket server.
     It adds the client into the USERS' set and calles the calculate_and_send_moon_ra_dec() function.
     As soon as the client is disconnected, the function removes it from the set and logs the information and
     the error into the users.log file."""
    config.USERS.add(websocket)
    config.logger.info(f"Client {websocket.remote_address[:2]} is CONNECTED. Active clients N: {len(config.USERS)}")
    try:
        while True:
            await calculate_and_send_moon_ra_dec(websocket)
    except websockets.ConnectionClosedError as err:
        config.USERS.remove(websocket)
        config.logger.info(f"Client {websocket.remote_address[:2]} is DISCONNECTED. "
                           f"Active clients N: {len(config.USERS)}")
        config.logger.error(f"Client {websocket.remote_address[:2]} has closed the connection with CloseError: {err}")
    except websockets.ConnectionClosedOK as err:
        config.USERS.remove(websocket)
        config.logger.info(f"Client {websocket.remote_address[:2]} is DISCONNECTED. "
                           f"Active clients N: {len(config.USERS)}")
        config.logger.error(f"Client {websocket.remote_address[:2]} has closed the connection with CloseOK: {err}")


def create_and_run_websocket(ip: str, port: int):
    """ The function takes as parameters ip and port and returns activated (listening) websocket server."""
    return websockets.serve(producer_handler, ip, port)


def main():
    """The function establishes the Ngrok tunnel with the mentioned port, creates and runs the websocket server
     without stop."""
    ng_url = ngrok.connect(config.PORT).public_url
    print(f"Ngrok tunnel address: ws{ng_url[4:]}")
    start_server = create_and_run_websocket(config.IP, config.PORT)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == "__main__":
    main()
