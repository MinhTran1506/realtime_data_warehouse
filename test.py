from faker import Faker

fake = Faker('de_DE')

fake_address = fake.street_address()
fake_name = fake.first_name()
fake_region = fake.state()
fake_phonenumber = fake.phone_number()
fake_eamil = fake.email()
print(fake_address)
print(fake_name)
print(fake_region)
print(fake_phonenumber)
print(fake_eamil)

