import pytz
import datetime
import time

def check_timer(target_time):
    now = datetime.datetime.now(pytz.timezone("Asia/Seoul"))
    current_time = "{}:{}:{}".format(str(now.hour).zfill(2), str(now.minute).zfill(2), str(now.second).zfill(2))
    if target_time == current_time:
        print("Currnet Time : {}, Alarm Time {} ".format(current_time, target_time))
        return True
    else:
        print("Currnet Time : {}, Alarm Time {} ".format(current_time, target_time))
        return False

if __name__ == "__main__":
    while True:
        ret_bool = check_timer("14:11:00")
        print("Run Bool? : {}".format(ret_bool))
        if ret_bool:
            print("Run Something")
        else:
            pass
        time.sleep(1)
        