from modules import auth
import time
from tqdm import tqdm
import unittest
import random

VALID_PASSWORD = r"GzsU`d>%8r_WK`u~JpMZR}tmL{,#:vmC'__\BTw#x2aVq+\Q{)"

class test_cant_register_user_twice(unittest.TestCase):
    def setUp(self):
        auth.register('user1',VALID_PASSWORD)
    def tearDown(self):
        auth.delete('user1')
    def test_cant_register_user_twice(self):
        with self.assertRaises(KeyError):
            auth.register('user1',VALID_PASSWORD)


class test_Register_and_Signin(unittest.TestCase):
    def test_Register_and_Signin(self):
        auth.register('user1',VALID_PASSWORD)
        assert auth.login('user1',VALID_PASSWORD)
        assert auth.login('user1','abc') == False
        auth.delete('user1')
        assert auth.login('user1',VALID_PASSWORD) == False

class test_Login_is_Timing_Attack_Safe(unittest.TestCase):
    def setUp(self):
        auth.register('user1',VALID_PASSWORD)
    def tearDown(self):
        auth.delete('user1')

    def measure_login_speed(self,iterations,password):
        start = time.time()
        for _ in range(iterations):
            auth.login('user1',password)
        duration = time.time() - start
        return duration
    
    def test_Login_is_Timing_Attack_Safe(self):
        TEST_DURATION = 5
        ACCEPTABLE_PERCENTAGE = 10
        
        hashrate = self.measure_login_speed(20,VALID_PASSWORD)
        iterations = int(TEST_DURATION / (hashrate / 2))
        valid_duration = self.measure_login_speed(iterations,VALID_PASSWORD)
        invalid_duration = self.measure_login_speed(iterations,"abc")
        delta_percent = valid_duration / invalid_duration

        self.assertAlmostEqual(
            first=delta_percent,second=1,
            delta=(0.01 * ACCEPTABLE_PERCENTAGE),
        )


class test_Register_and_Delete(unittest.TestCase):
    def tearDown(self):
        auth.delete('user1')
    
    def test_Register_and_Signin(self):
        auth.register('user1',VALID_PASSWORD)
        assert auth.login('user1',VALID_PASSWORD)
        assert auth.login('user1','abc') == False
