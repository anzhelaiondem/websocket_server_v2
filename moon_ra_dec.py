import datetime as dt

from typing import List, Dict

# Fixed start date and time.
START_DATE = dt.datetime(2021, 6, 1, 23, 59, 59)
# Fixed RA and DEC for the above mentioned START_DATE.
FIX_RA = [22, 46, 54]
FIX_DEC = [-13, 27, 21]
# Dictionary of average change(value) of RA and DEC for the mentioned time slots/key.
AV_DELTA_RA = {"0-5": 0.032, "5-12": 0.036, "12-17": 0.038, "17-0": 0.041}
AV_DELTA_DEC = {"5-9 and 17-20": 0.055, "0-5, 9-17, and 20-0": 0.182}


def convert_hours_minutes_seconds_to_seconds(time_list: List[int]):
    """Takes a list of coordinates, converts it into seconds."""
    total_seconds = time_list[0] * 3600 + time_list[1] * 60 + time_list[2]
    return total_seconds


def convert_seconds_to_hours_minutes_seconds(total_seconds):
    """The function takes total seconds and converts it into hours, minutes, and seconds.
    Can be used for DEC conversion too."""
    h, m = divmod(total_seconds, 3600)
    m, s = divmod(m, 60)
    return int(h), int(m), int(s)


def calculate_moon_ra_dec(fix_ra: List[int], fix_dec: List[int], start_date, av_delta_ra: Dict[str, float],
                          av_delta_dec: Dict[str, float]):
    """The function takes initial/fixed RA, DEC, Datetime and delta change per second of RA and DEC for
     different time slots. Runs the cycle for each seconds (difference of present and initial date)
      adds/deducts changes per second and returns the string with final RA and DEC coordinates."""
    new_ra = convert_hours_minutes_seconds_to_seconds(fix_ra)
    new_dec = convert_hours_minutes_seconds_to_seconds(fix_dec)
    start_date = start_date
    time_in_seconds = int((dt.datetime.now() - start_date).total_seconds())
    for sec in range(1, time_in_seconds):
        if 0 <= new_ra < 5 * 3600:
            new_ra = new_ra + av_delta_ra.get("0-5")
            new_dec = new_dec + av_delta_dec.get("0-5, 9-17, and 20-0")
        elif 5 * 3600 <= new_ra < 7 * 3600:
            new_ra = new_ra + av_delta_ra.get("5-12")
            new_dec = new_dec + av_delta_dec.get("5-9 and 17-20")
        elif 7 * 3600 <= new_ra < 9 * 3600:
            new_ra = new_ra + av_delta_ra.get("5-12")
            new_dec = new_dec - av_delta_dec.get("5-9 and 17-20")
        elif 9 * 3600 <= new_ra < 12 * 3600:
            new_ra = new_ra + av_delta_ra.get("5-12")
            new_dec = new_dec - av_delta_dec.get("0-5, 9-17, and 20-0")
        elif 12 * 3600 <= new_ra < 17 * 3600:
            new_ra = new_ra + av_delta_ra.get("12-17")
            new_dec = new_dec - av_delta_dec.get("0-5, 9-17, and 20-0")
        elif 17 * 3600 <= new_ra < 19 * 3600:
            new_ra = new_ra + av_delta_ra.get("17-0")
            new_dec = new_dec - av_delta_dec.get("5-9 and 17-20")
        elif 19 * 3600 <= new_ra < 24 * 3600:
            new_ra = new_ra + av_delta_ra.get("17-0")
            new_dec = new_dec + av_delta_dec.get("0-5, 9-17, and 20-0")
        if new_ra > 86399:
            new_ra = new_ra % 86399
    ra_h, ra_m, ra_s = convert_seconds_to_hours_minutes_seconds(new_ra)
    dec_degree, dec_m, dec_s = convert_seconds_to_hours_minutes_seconds(new_dec)
    return f"RA: {ra_h}:{ra_m}:{ra_s}, DEC: {dec_degree}:{dec_m}:{dec_s}"
