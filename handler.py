from seatRes import webRequests
import warnings

warnings.filterwarnings('ignore')
seat_id = webRequests.reserve('xxx', 'xxx', 2685, 1380, 1410)
if seat_id is not None:
    webRequests.cancel('xxx', 'xxx', seat_id)
