from faker import Faker
from random import choice, randint
from decimal import Decimal


fake = Faker()

def generate_fake_products(count=10) -> None:
    from users.models import User
    from products.models import Product, Category, City

    users = list(User.objects.all())
    categories = list(Category.objects.all())
    cities = list(City.objects.all())

    for _ in range(count):
        product = Product.objects.create(
            user=choice(users),
            name=fake.text().title()[:255],
            category=choice(categories),
            city=choice(cities),
            price=Decimal(fake.pyfloat(left_digits=4, right_digits=2, positive=True, min_value=10, max_value=1000)),
            description=fake.text(max_nb_chars=200),
            is_new_product=fake.boolean(),
            is_delivery_available=fake.boolean(),
            is_credit_available=fake.boolean(),
            is_barter_available=fake.boolean(),
            is_via_negotiator=fake.boolean(),
            is_vip=fake.boolean(),
            is_premium=fake.boolean(),
            is_promoted=fake.boolean(),
            is_super_chance=fake.boolean(),
            status=choice([Product.PENDING, Product.APPROVED, Product.REJECTED]),
            slug=fake.slug(),
            is_active=fake.boolean(),
            extra_filters={fake.word(): fake.word() for _ in range(randint(1, 3))},
            view_count=randint(0, 1000),
            expires_at=fake.future_datetime(end_date="+30d")
        )
        print(f"Created product: {product.name}")

    print(f"Successfully created {count} products.")