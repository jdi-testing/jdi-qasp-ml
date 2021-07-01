import uuid
from random import random

import faker

fake = faker.Faker()


def generate_uuid():
    return str(uuid.uuid4())[:8]
