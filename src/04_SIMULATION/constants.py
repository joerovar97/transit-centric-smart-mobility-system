from datetime import datetime, timedelta, date
import numpy as np
import math
# SIMULATION

START_TIME = datetime.strptime('05:00:00', "%H:%M:%S")
END_TIME = datetime.strptime('10:00:00', "%H:%M:%S")
START_TIME_SEC = (START_TIME - datetime(1900, 1, 1)).total_seconds()
END_TIME_SEC = (END_TIME - datetime(1900, 1, 1)).total_seconds()
TOTAL_MIN = (END_TIME - START_TIME).total_seconds() / 60
FOCUS_START_TIME = datetime.strptime('07:28:00', "%H:%M:%S")
FOCUS_END_TIME = datetime.strptime('08:15:00', "%H:%M:%S")
FOCUS_START_TIME_SEC = (FOCUS_START_TIME - datetime(1900, 1, 1)).total_seconds()
FOCUS_END_TIME_SEC = (FOCUS_END_TIME - datetime(1900, 1, 1)).total_seconds()
# ROUTE NETWORK: NUMBER OF ROUTES, NUMBER OF STOPS, ROUTE STOPS
# ROUTE 20 EAST
TIME_INTERVAL_LENGTH_MINS = 30
TIME_START_INTERVAL = int(START_TIME_SEC / (60 * TIME_INTERVAL_LENGTH_MINS))
TIME_NR_INTERVALS = int(math.ceil(TOTAL_MIN / TIME_INTERVAL_LENGTH_MINS))
DATES = ['2019-09-03', '2019-09-04', '2019-09-05', '2019-09-06']
TRIP_WITH_FULL_STOP_PATTERN = 911414030
# OUTBOUND TIME DEPENDENT TRIP TIME DISTRIBUTION
TRIP_TIME_INTERVAL_LENGTH_MINS = 30
TRIP_TIME_START_INTERVAL = int(START_TIME_SEC / (60 * TRIP_TIME_INTERVAL_LENGTH_MINS))
TRIP_TIME_NR_INTERVALS = int(math.ceil(TOTAL_MIN / TRIP_TIME_INTERVAL_LENGTH_MINS))

# TRAVEL, DWELL TIME AND DEPARTURE DELAY DISTRIBUTION

ACC_DEC_TIME = 4.5
BOARDING_TIME = 2.1
ALIGHTING_TIME = 1.1
DWELL_TIME_ERROR = 1.5

DDD = 'UNIFORM'
DEP_DELAY_FROM = -60
DEP_DELAY_TO = 90


# DEMAND: O-D POISSON RATES
INPUT_DEMAND_START_SEC = 7 * 60 * 60
INPUT_DEMAND_END_SEC = 10 * 60 * 60
INPUT_DEMAND_TOTAL_MIN = (INPUT_DEMAND_END_SEC - INPUT_DEMAND_START_SEC) / 60
INPUT_DEM_INTERVAL_LENGTH_MINS = 5
INPUT_DEM_START_INTERVAL = int(INPUT_DEMAND_START_SEC / (60 * INPUT_DEM_INTERVAL_LENGTH_MINS))
INPUT_DEM_NR_INTERVALS = int(math.ceil(INPUT_DEMAND_TOTAL_MIN / INPUT_DEM_INTERVAL_LENGTH_MINS))
INPUT_DEM_END_INTERVAL = INPUT_DEM_START_INTERVAL + INPUT_DEM_NR_INTERVALS
DEM_INTERVAL_LENGTH_MINS = 60
DEM_START_INTERVAL = int(INPUT_DEMAND_START_SEC / (60 * DEM_INTERVAL_LENGTH_MINS))
DEM_END_INTERVAL = int(INPUT_DEMAND_END_SEC / (60 * DEM_INTERVAL_LENGTH_MINS))
DEM_NR_INTERVALS = int(math.ceil(INPUT_DEMAND_TOTAL_MIN / DEM_INTERVAL_LENGTH_MINS))
DEM_PROPORTION_INTERVALS = int(DEM_INTERVAL_LENGTH_MINS / INPUT_DEM_INTERVAL_LENGTH_MINS)
CAPACITY = 55
POST_PROCESSED_DEM_START_INTERVAL = int(START_TIME_SEC / (60 * DEM_INTERVAL_LENGTH_MINS))
POST_PROCESSED_DEM_END_INTERVAL = int(END_TIME_SEC / (60 * DEM_INTERVAL_LENGTH_MINS))

# OTHER SERVICE PARAMETERS: DWELL TIME, SIMULATION LENGTH
[IDX_ARR_T, IDX_DEP_T, IDX_LOAD, IDX_PICK, IDX_DROP, IDX_DENIED, IDX_HOLD_TIME, IDX_SKIPPED] = [i for i in range(1, 9)]
TPOINT0 = '386'
TPOINT1 = '8613'
NO_OVERTAKE_BUFFER = 5

# REINFORCEMENT LEARNING
BASE_HOLDING_TIME = 10
CONTROLLED_STOPS = ['386', '406', '416', '4727', '3954']
CONTROLLED_STOPS_ALTERNATIVE = ['386', '409', '428', '3954']
LIMIT_HOLDING = 40
N_ACTIONS_RL = int(LIMIT_HOLDING/BASE_HOLDING_TIME) + 2
N_STATE_PARAMS_RL = 6
[IDX_RT_PROGRESS, IDX_LOAD_RL, IDX_FW_H, IDX_BW_H, IDX_PAX_AT_STOP, IDX_PREV_FW_H] = [i for i in range(N_STATE_PARAMS_RL)]
SKIP_ACTION = 0
