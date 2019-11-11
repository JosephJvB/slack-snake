import os
import peewee

if os.environ['ENV'] != 'dev':
    db = peewee.MySQLDatabase(os.environ['CLEARDB_DATABASE_URL'])
else:
    db = peewee.MySQLDatabase(
    os.environ['DB_NAME'],
    user=os.environ['DB_USER'],
    passwd=os.environ['DB_PASS'])

class Base(peewee.Model):
    class Meta:
        database = db

class Records(Base):
    user = peewee.CharField()
    track = peewee.CharField()

def main():
    db.connect()
    db.create_tables([Records])
    print('up!')

if __name__ == '__main__':
    main()
