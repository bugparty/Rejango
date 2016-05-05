import inspect
import types


class DataBase:
    def __init__(self, config):
        self.__config = config


    def connect(self):
        raise NotImplementedError


    def get_cursor(self):
        raise NotImplementedError


    def close(self):
        raise NotImplementedError


class MySqlDB(DataBase):

    def connect(self):
        import mysql.connector
        self.__cnx = mysql.connector.connect(user=self._DataBase__config['user'],
                     password=self._DataBase__config['password'],
                     host=self._DataBase__config['host'],
                     database=self._DataBase__config['database'])


    def get_cursor(self):
        return self.__cnx.cursor()


    def close(self):
        self.__cnx.close()


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


class ModelManager:
    def create(self):
        raise NotImplementedError

class Model:
    objects = ModelManager()

    def __init__(self):
        self.id = AutoField()

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

class DataBaseManager:
    def __init__(self,db_instance):
        self.__instance = db_instance
        self.__instance.connect()
        self.__cursor = self.__instance.get_cursor()

    def create_table(self, model):
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

        self.__cursor.execute(sql)

        print('creating table %s:' % model.__name__)
        DataBaseManager.desc_model(methodList, model)
        print('sql is')
        print(sql)


    @staticmethod
    def gen_desc_row(cls,method):
        field = getattr(cls,method)
        m_type = field._type
        row = '|{0:^12.12}|{1:^14.14}|{2:^6.6}|{3:^5.5}|{4:^9.9}|{5:^7.7}|'.format(
            method,m_type,'Yes','','NULL','')
        return row


    @staticmethod
    def is_class_derive_from(the_class, origin):
        if(not inspect.isclass(the_class)):
            return False
        if(not inspect.isclass(origin)):
            return False
        return origin in the_class.__bases__

    @staticmethod
    def desc_model(methodList,model):
        table_head = '''+------------+--------------+------+-----+---------+-------+
|   Field    |      Type    | Null | Key | Default | Extra |
+------------+--------------+------+-----+---------+-------+'''
        table_end = '''+------------+--------------+------+-----+---------+-------+'''

        print(table_head)
        for m in methodList:
            print(DataBaseManager.gen_desc_row(model,m))
        print(table_end)

    def auto_dectet(self,context):
         self.load_class(context.values())
         modules = [module  for module in context.values() if type(module) == types.ModuleType ]
         for module in modules:
             self.load_module(module)
    def load_class(self,cls):
         models = [m for m in cls if DataBaseManager.is_class_derive_from(m, Model) ]
         for model in models:
             self.create_table(model)
    def load_module(self,module):
        classes = [getattr(module,cls) for cls in dir(module) if inspect.isclass(getattr(module,cls))]
        models = [m for m in  classes if DataBaseManager.is_class_derive_from(m, Model) ]
        for model in models:
            self.create_table(model)


