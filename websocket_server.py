import websockets
import asyncio
import config
import logging
import moon_ra_dec as m

from pyngrok import ngrok

USERS = set()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(config.LOG_MSG_FORMAT)
handler = logging.FileHandler(config.LOG_FILE_NAME, mode=config.LOG_FILE_MODE)
handler.setLevel(logging.DEBUG)
handler.setFormatter(formatter)
logger.addHandler(handler)


async def sleep(websocket):
    """This function implements 10 seconds sleeping effect (the SLEEP_TIME is fixed in the config.py)
     and every second checks the connectivity of the client (websocket)."""
    t = 1
    while t <= config.SLEEP_TIME:
        await asyncio.sleep(1)
        await websocket.send("")
        t += 1


async def producer_handler(websocket, path) -> None:
    """The function starts actively listening to any websocket client that connects to the websocket server.
     It adds the client into the USERS' set and calls the calculate_and_send_moon_ra_dec() function.
     As soon as the client is disconnected, the function removes it from the set and logs the information and
     the error into the users.log file."""
    USERS.add(websocket)
    logger.info(f"Client {websocket.remote_address[:2]} is CONNECTED. Active clients N: {len(USERS)}")
    try:
        while True:
            await websocket.send(
                m.calculate_moon_ra_dec(m.FIX_RA, m.FIX_DEC, m.START_DATE, m.AV_DELTA_RA, m.AV_DELTA_DEC))
            await sleep(websocket)
    except websockets.ConnectionClosedError as err:
        logger.error(f"Client {websocket.remote_address[:2]} has closed the connection with CloseError: {err}")
    except websockets.ConnectionClosedOK as err:
        logger.error(f"Client {websocket.remote_address[:2]} has closed the connection with CloseOK: {err}")
    except Exception as err:
        logger.exception(f"UNEXPECTED ERROR: {err}")
    finally:
        USERS.remove(websocket)
        logger.info(f"Active clients N: {len(USERS)}")


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
