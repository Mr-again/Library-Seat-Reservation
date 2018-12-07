from seatRes import webRequests
import warnings

warnings.filterwarnings('ignore')
seat_id = webRequests.reserve('2015301500269', '084818', 2685, 1380, 1410)
if seat_id is not None:
    webRequests.cancel('2015301500269', '084818', seat_id)
