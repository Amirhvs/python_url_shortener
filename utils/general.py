from hashids import Hashids
import random
import time

hashids = Hashids(min_length=10, salt="dang fang")

def get_hash_id():
    rand_int = random.randint(1, 999999)
    return hashids.encode(rand_int, int(time.time())) 
