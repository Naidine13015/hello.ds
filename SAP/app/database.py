import os
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# # load_dotenv()

# class Database:
#     def __init__(self):
#         # connection_string = (
#         #     f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
#         # )
#         self.engine = create_engine(connection_string)
#         self.meta = MetaData(bind=self.engine)
#         self.meta.reflect()
#         self.Session = sessionmaker(bind=self.engine)

class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.meta = MetaData()
        self.meta.reflect(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        # Crée les tables seulement si elles n'existent pas encore
        Table('clients', self.meta,
              Column('id', Integer, primary_key=True),
              Column('nom', String(100)),
              Column('prenom', String(100)),
              Column('email', String(150))
        )

        Table('ventes', self.meta,
              Column('id', Integer, primary_key=True),
              Column('produit', String(100)),
              Column('quantite', Integer),
              Column('prix', Numeric)
        )

        Table('stocks', self.meta,
              Column('id', Integer, primary_key=True),
              Column('produit', String(100)),
              Column('quantite', Integer)
        )

        self.meta.create_all(self.engine)

    def insert_initial_data(self):
        session = self.Session()

        # Vérifier que les tables sont vides avant insertion
        if session.query(self.clients).count() == 0:
            session.execute(self.clients.insert(), [
                {'nom': 'Dupont', 'prenom': 'Jean', 'email': 'jean.dupont@example.com'},
                {'nom': 'Durand', 'prenom': 'Marie', 'email': 'marie.durand@example.com'},
                {'nom': 'Martin', 'prenom': 'Luc', 'email': 'luc.martin@example.com'},
                {'nom': 'Bernard', 'prenom': 'Julie', 'email': 'julie.bernard@example.com'},
                {'nom': 'Petit', 'prenom': 'Paul', 'email': 'paul.petit@example.com'}
            ])

        if session.query(self.ventes).count() == 0:
            session.execute(self.ventes.insert(), [
                {'produit': 'Produit A', 'quantite': 10, 'prix': 99.99},
                {'produit': 'Produit B', 'quantite': 5, 'prix': 59.99},
                {'produit': 'Produit C', 'quantite': 20, 'prix': 29.99},
                {'produit': 'Produit D', 'quantite': 7, 'prix': 79.99},
                {'produit': 'Produit E', 'quantite': 3, 'prix': 199.99}
            ])

        if session.query(self.stocks).count() == 0:
            session.execute(self.stocks.insert(), [
                {'produit': 'Produit A', 'quantite': 50},
                {'produit': 'Produit B', 'quantite': 30},
                {'produit': 'Produit C', 'quantite': 100},
                {'produit': 'Produit D', 'quantite': 25},
                {'produit': 'Produit E', 'quantite': 15}
            ])

        session.commit()
        session.close()

    def read(self, table_name):
        table = Table(table_name, self.meta, autoload_with=self.engine)
        session = self.Session()
        query = session.query(table).all()
        session.close()
        return [dict(row._mapping) for row in query]

    def create(self, table_name, record):
        table = Table(table_name, self.meta, autoload_with=self.engine)
        session = self.Session()
        insert_stmt = table.insert().values(**record)
        session.execute(insert_stmt)
        session.commit()
        session.close()

    def update(self, table_name, record_id, updated_data):
        table = Table(table_name, self.meta, autoload_with=self.engine)
        session = self.Session()
        update_stmt = table.update().where(table.c.id == record_id).values(**updated_data)
        session.execute(update_stmt)
        session.commit()
        session.close()

    def delete(self, table_name, record_id):
        table = Table(table_name, self.meta, autoload_with=self.engine)
        session = self.Session()
        delete_stmt = table.delete().where(table.c.id == record_id)
        session.execute(delete_stmt)
        session.commit()
        session.close()
