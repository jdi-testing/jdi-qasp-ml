import random
import uuid

import faker

fake = faker.Faker()


def generate_uuid():
    return str(uuid.uuid4())[:8]


def border_properties():
    return {'border-style': random.choice(('solid', 'none', 'dotted', 'inset',
                                           'dashed solid', 'hidden', 'double',
                                           'groove', 'ridge')),
            'border-width': f"{random.randint(1, 5)}px",
            'border-color': fake.color()}


def bootstrap_button_styles():
    return ('btn-primary', 'btn-secondary', 'btn-success',
            'btn-danger', 'btn-warning', 'btn-warning',
            'btn-light', 'btn-dark', 'btn-link',
            'btn-outline-primary', 'btn-outline-secondary', 'btn-outline-success',
            'btn-outline-danger', 'btn-outline-warning', 'btn-outline-warning',
            'btn-outline-light', 'btn-outline-dark', 'btn-outline-link')
