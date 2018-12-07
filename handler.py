from seatRes import webRequests
import warnings

warnings.filterwarnings('ignore')
seat_id = webRequests.reserve('2015301500270', '178511', 2685, 1380, 1410)
webRequests.cancel('2015301500270', '178511', seat_id)
