import inspect
import mysql.connector

cnx = mysql.connector.connect(user='root',password='admin',
                              host='127.0.0.1',
                              database='test')

cursor = cnx.cursor()
class Field:
    _type = "undefined"


class StringField(Field):
    def __init__(self):
        self._type = 'String'

class DateField(Field):
    def __init__(self):
        self._type = 'Date'

class IntField(Field):
    def __init__(self):
        self._type = 'Int'
class AutoField(Field):
    def __init__(self):
        self._type = 'Auto'

def process_create_StringField(obj):
    return "VARCHAR(30)"
def process_create_IntField(obj):
    return "INT"
def process_create_AutoField(obj):
    return "INT AUTO_INCREMENT PRIMARY KEY"
def process_create_Date(obj):
    return "DATE"
class Model:
    def __init__(self):
        pass
    id = AutoField()
    def __cal_fields(self):
        self.__methodList = [method for method in dir(self)
              if isinstance(getattr(self,method),Field)]
        self.__fields = [(str_method, getattr(self,str_method))for str_method in self.__methodList]

    def save(self):
        if(not hasattr(self,'__methodList')):
            self.__cal_fields()

        class_name = self.__class__.__name__
        pass
        #print(dir(self))


class User(Model):
    username = StringField()
    age = IntField()
    birthday = DateField()

class Foo(Model):
    bar = StringField()
def create_table(model):
    '''A sample of the table description is like that

    mysql> desc tb02e946a0
        -> ;
    +-------+----------+------+-----+---------+-------+
    | Field | Type     | Null | Key | Default | Extra |
    +-------+----------+------+-----+---------+-------+
    | pos   | int(11)  | YES  |     | NULL    |       |
    | tree  | char(20) | YES  |     | NULL    |       |
    +-------+----------+------+-----+---------+-------+
    so we will simlulate this style
    '''

    create_table = 'CREATE TABLE IF NOT EXISTS %s\n(\n'
    methodList = [method for method in dir(model)
                  if isinstance(getattr(model,method),Field)]
    fields = [(str_method, getattr(model,str_method))for str_method in methodList]

    sql_head = create_table % model.__name__
    sql_end  = ');'
    sql = sql_head
    for field in fields:
        obj = field[1]
        sql += field[0]
        sql += " "
        if(isinstance(obj, StringField)):
            sql += process_create_StringField(obj)
        elif(isinstance(obj,IntField)):
            sql += process_create_IntField(obj)
        elif(isinstance(obj,AutoField)):
            sql += process_create_AutoField(obj)
        elif(isinstance(obj,DateField)):
            sql += process_create_Date(obj)
        sql +=",\n"
    sql = sql[0:-2] + '\n'
    sql += sql_end

    cursor.execute(sql)

    print('creating table %s:' % model.__name__)
    desc_model(methodList, model)
    print('sql is')
    print(sql)

def gen_desc_row(cls,method):
    field = getattr(cls,method)
    m_type = field._type
    row = '|{0:^12.12}|{1:^14.14}|{2:^6.6}|{3:^5.5}|{4:^9.9}|{5:^7.7}|'.format(
        method,m_type,'Yes','','NULL','')
    return row
def is_class_derive_from(the_class, origin):
    if(not inspect.isclass(the_class)):
        return False
    if(not inspect.isclass(origin)):
        return False
    return origin in the_class.__bases__

def auto_dectet():
     models = [m for m in globals().values() if is_class_derive_from(m, Model) ]
     for model in models:
         create_table(model)

        
def desc_model(methodList,model):
    table_head = '''+------------+--------------+------+-----+---------+-------+
|   Field    |      Type    | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+'''
    table_end = '''+------------+--------------+------+-----+---------+-------+'''

    print(table_head)
    for m in methodList:
        print(gen_desc_row(model,m))
    print(table_end)

if __name__ == '__main__':
    #create_table(User)
    auto_dectet()

    cursor.execute("SHOW TABLES;")
    print(cursor.fetchall())
    cnx.close()
    m = Model()
    m.save()
