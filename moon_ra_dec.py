import datetime as dt

# Fixed date and time for the start.
START_DATE = dt.datetime(2021, 6, 1, 23, 59, 59)
# Fixed RA and DEC for the above mentioned START_DATE.
FIX_RA = [22, 46, 54]
FIX_DEC = [-13, 27, 21]
# FIX_RA and FIX_DEC is converted into seconds.
FIX_RA_IN_SEC = FIX_RA[0] * 3600 + FIX_RA[1] * 60 + FIX_RA[2]
FIX_DEC_IN_SEC = FIX_DEC[0] * 3600 + FIX_DEC[1] * 60 + FIX_DEC[2]
# The average change of the Moon RA (in seconds) when RA is between 0-5.
AV_DELTA_RA_0_5 = 0.032
# The average change of the Moon RA (in seconds) when RA is between 5-12.
AV_DELTA_RA_5_12 = 0.036
# The average change of the Moon RA (in seconds) when RA is between 12-17.
AV_DELTA_RA_12_17 = 0.038
# The average change of the Moon RA (in seconds) when RA is between 17-0.
AV_DELTA_RA_17_24 = 0.041
# The average change of the Moon DEC (in seconds) when RA is between 5-8 and 17-20.
AV_DELTA_DEC_5_8_and_17_20 = 0.055
# The average change of the Moon DEC (in seconds) when RA is between 0-5, 8-17, and 20-24.
AV_DELTA_DEC_0_5_8_17_20_24 = 0.182


def calculate_moon_ra_dec():
    new_ra = FIX_RA_IN_SEC
    new_dec = FIX_DEC_IN_SEC
    start_date = START_DATE
    time_in_seconds = int((dt.datetime.now() - start_date).total_seconds())
    for sec in range(time_in_seconds):
        if 0 <= new_ra < 5 * 3600:
            new_ra = new_ra + AV_DELTA_RA_0_5
            new_dec = new_dec + AV_DELTA_DEC_0_5_8_17_20_24
        elif 5 * 3600 <= new_ra < 6 * 3600:
            new_ra = new_ra + AV_DELTA_RA_5_12
            new_dec = new_dec + AV_DELTA_DEC_5_8_and_17_20
        elif 6 * 3600 <= new_ra < 8 * 3600:
            new_ra = new_ra + AV_DELTA_RA_5_12
            new_dec = new_dec - AV_DELTA_DEC_5_8_and_17_20
        elif 8 * 3600 <= new_ra < 12 * 3600:
            new_ra = new_ra + AV_DELTA_RA_5_12
            new_dec = new_dec - AV_DELTA_DEC_0_5_8_17_20_24
        elif 12 * 3600 <= new_ra < 17 * 3600:
            new_ra = new_ra + AV_DELTA_RA_12_17
            new_dec = new_dec - AV_DELTA_DEC_0_5_8_17_20_24
        elif 17 * 3600 <= new_ra < 18 * 3600:
            new_ra = new_ra + AV_DELTA_RA_17_24
            new_dec = new_dec - AV_DELTA_DEC_0_5_8_17_20_24
        elif 18 * 3600 <= new_ra < 24 * 3600:
            new_ra = new_ra + AV_DELTA_RA_17_24
            new_dec = new_dec + AV_DELTA_DEC_0_5_8_17_20_24
        if new_ra > 86399:
            new_ra = new_ra % 86399
    ra = f'{(int(new_ra // 3600))}:{int((new_ra % 3600) // 60)}:{int((new_ra % 3600) % 60)}'
    dec = f'{int(new_dec // 3600)}° {int((new_dec % 3600) // 60)}′ {int((new_dec % 3600) % 60)}′′'
    return f" RA: {ra}, DEC: {dec}"
