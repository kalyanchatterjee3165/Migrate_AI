from faker import Faker

# Single shared Faker instance — import this everywhere
fake = Faker()
Faker.seed(42)  # reproducible data across runs


def fake_id(i: int) -> int:
    return i + 1


def fake_name() -> str:
    return fake.name()


def fake_email() -> str:
    return fake.email()


def fake_phone() -> str:
    return fake.phone_number()


def fake_address() -> str:
    return fake.address().replace("\n", ", ")


def fake_company() -> str:
    return fake.company()


def fake_date() -> str:
    return fake.date_between(start_date="-2y", end_date="today").isoformat()


def fake_datetime() -> str:
    return fake.date_time_between(start_date="-2y", end_date="now").isoformat()


def fake_amount() -> float:
    return round(fake.pyfloat(min_value=1, max_value=10_000, right_digits=2), 2)


def fake_status(options: list[str]) -> str:
    return fake.random_element(options)


def fake_uuid() -> str:
    return str(fake.uuid4())


def fake_url() -> str:
    return fake.url()


def fake_country() -> str:
    return fake.country()


def fake_city() -> str:
    return fake.city()