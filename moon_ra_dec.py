import datetime as dt

# Fixed start date and time.
START_DATE = dt.datetime(2021, 6, 1, 23, 59, 59)
# Fixed RA and DEC for the above mentioned START_DATE.
FIX_RA = [22, 46, 54]
FIX_DEC = [-13, 27, 21]
# Dictionary of average change(value) of RA and DEC for the mentioned time slots/key.
AV_DELTA_RA = {"0-5": 0.032, "5-12": 0.036, "12-17": 0.038, "17-0": 0.041}
AV_DELTA_DEC = {"5-8 and 17-20": 0.055, "0-5, 8-17, and 20-0": 0.182}


def convert_ra_and_dec_into_seconds(ra: list[int], dec: list[int]):
    """Takes list of RA and list of DEC coordinates, converts it into seconds and returns
     tuple of RA and DEC in seconds."""
    ra_in_sec = ra[0] * 3600 + ra[1] * 60 + ra[2]
    dec_in_sec = dec[0] * 3600 + dec[1] * 60 + dec[2]
    return ra_in_sec, dec_in_sec


def convert_ra_and_dec_into_coordinates(ra: int, dec: int):
    """Takes RA and DEC in seconds, converts it into coordinates and returns
     tuple of RA and DEC."""
    ra = f'{(int(ra // 3600))}:{int((ra % 3600) // 60)}:{int((ra % 3600) % 60)}'
    dec = f'{int(dec // 3600)}° {int((dec % 3600) // 60)}′ {int((dec % 3600) % 60)}′′'
    return ra, dec


def calculate_moon_ra_dec(initial_ra: list[int] = FIX_RA, initial_dec: list[int] = FIX_DEC, initial_date=START_DATE,
                          delta_ra: dict[str, float] = AV_DELTA_RA, delta_dec: dict[str, float] = AV_DELTA_DEC):
    """The function takes initial/fixed RA, DEC, Datetime and delta change per second of RA and DEC for
     different time slots. Runs the cycle for each seconds (difference of present and initial date)
      adds/deducts changes per second and returns the string with final RA and DEC coordinates."""
    new_ra, new_dec = convert_ra_and_dec_into_seconds(initial_ra, initial_dec)
    start_date = initial_date
    time_in_seconds = int((dt.datetime.now() - start_date).total_seconds())
    for sec in range(1, time_in_seconds):
        if 0 <= new_ra < 5 * 3600:
            new_ra = new_ra + delta_ra.get("0-5")
            new_dec = new_dec + delta_dec.get("0-5, 8-17, and 20-0")
        elif 5 * 3600 <= new_ra < 6 * 3600:
            new_ra = new_ra + delta_ra.get("5-12")
            new_dec = new_dec + delta_dec.get("5-8 and 17-20")
        elif 6 * 3600 <= new_ra < 8 * 3600:
            new_ra = new_ra + delta_ra.get("5-12")
            new_dec = new_dec - delta_dec.get("5-8 and 17-20")
        elif 8 * 3600 <= new_ra < 12 * 3600:
            new_ra = new_ra + delta_ra.get("5-12")
            new_dec = new_dec - delta_dec.get("0-5, 8-17, and 20-0")
        elif 12 * 3600 <= new_ra < 17 * 3600:
            new_ra = new_ra + delta_ra.get("12-17")
            new_dec = new_dec - delta_dec.get("5-8 and 17-20")
        elif 17 * 3600 <= new_ra < 18 * 3600:
            new_ra = new_ra + delta_ra.get("17-0")
            new_dec = new_dec - delta_dec.get("0-5, 8-17, and 20-0")
        elif 18 * 3600 <= new_ra < 24 * 3600:
            new_ra = new_ra + delta_ra.get("17-0")
            new_dec = new_dec + delta_dec.get("0-5, 8-17, and 20-0")
        if new_ra > 86399:
            new_ra = new_ra % 86399
    ra, dec = convert_ra_and_dec_into_coordinates(new_ra, new_dec)
    return f"RA: {ra}, DEC: {dec}"