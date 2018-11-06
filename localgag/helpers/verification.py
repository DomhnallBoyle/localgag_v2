import random
import string


def create_verification_code():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
