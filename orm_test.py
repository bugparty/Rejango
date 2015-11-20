import orm
import unittest
config = {
        'user':'root',
        'password':'admin',
        'host':'localhost',
        'database':'test'
}
import orm_test_models
class ModelTest(unittest.TestCase):
    def test_Model(self):
        m = orm.Model()
        self.assertTrue(isinstance(m.id,orm.AutoField))

class ModelLoad(unittest.TestCase):
    def test_load(self):
        pass

class DataBaseManagerTest(unittest.TestCase):
    def test_auto_detect(self):
        import orm_test_models
        db = orm.MySqlDB(config)
        manager = orm.DataBaseManager(db)
        manager.auto_dectet(globals())


class MysqlDatabaseTest(unittest.TestCase):
    def test_connect(self):
        db = orm.MySqlDB(config)
        db.connect()


    def test_get_cursor(self):
        db = orm.MySqlDB(config)
        db.connect()
        cursor = db.get_cursor()
        cursor.execute("DROP TABLE IF EXISTS test_get_cursor;")
        cursor.execute("CREATE TABLE test_get_cursor("
                       "user VARCHAR(30)"
                       ");")
        cursor.execute("INSERT INTO test_get_cursor (user) VALUES"
                       "('bowman han');")
        cursor.execute("select * from test_get_cursor;")
        self.assertIsNotNone(cursor.fetchone())
        db.close()



