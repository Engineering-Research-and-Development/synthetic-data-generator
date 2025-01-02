"""This module call all the testing functions"""
import test_tmodels


if __name__ == '__main__':
    for i in dir(test_tmodels):
        item = getattr(test_tmodels,i)
        if callable(item):
            result = item()
            if result:
                print("Testing: ",item.__name__," Result: \033[92mPASSED\033[0m")
            else:
                print("Testing: ", item.__name__, " Result: \033[91mFAILED\033[0m")