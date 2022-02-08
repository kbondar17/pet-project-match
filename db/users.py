from sqlalchemy import text
import random
from faker.providers import DynamicProvider
from db.session import db_session, engine
from db.models import User
from faker import Faker
fake = Faker('ru_RU')


prog_langs = DynamicProvider(
    provider_name="prog_langs",
    elements=["python", "javascript", "go",
              "java", "c#", 'css', 'html', 'c++'])

fake.add_provider(prog_langs)

# with engine.connect() as conn:
#     res = conn.execute(text("create table testtable();"))
#     print(res)

for _ in range(1, 51):

    # user = User(
    #     name=fake.name(),
    #     description=fake.text(random.randint(200, 500)),
    #     prog_lang=list(set(fake.prog_langs()
    #                    for e in range(random.randint(1, 3))))

    # )
    db_session.add(user)
    db_session.commit()
