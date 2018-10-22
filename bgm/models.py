import peewee

import bgm.settings
from peewee import *
import json


class JSONField(TextField):
    # field_type = 'JSON'

    def python_value(self, value):
        if value is not None:
            try:
                return json.loads(value)
            except (TypeError, ValueError):
                return value

    def db_value(self, value):
        if value is not None:
            return json.dumps(value)


class BgmIpViewer(Model):
    class Meta:
        database = peewee.MySQLDatabase(bgm.settings.MYSQL_DBNAME,
                                        host=bgm.settings.MYSQL_HOST,
                                        charset='utf8mb4',
                                        user=bgm.settings.MYSQL_USER,
                                        password=bgm.settings.MYSQL_PASSWORD, )


class Subject(BgmIpViewer):
    id = IntegerField(primary_key=True, index=True)
    name = CharField()
    image = CharField()
    subject_type = CharField()
    name_cn = CharField()

    tags = JSONField()
    info = JSONField()
    score_details = JSONField()

    score = CharField()
    wishes = CharField()
    done = CharField()
    doings = CharField()
    on_hold = CharField()
    dropped = CharField()
    map = IntegerField(index=True, null=True)


class Relation(BgmIpViewer):
    id = CharField(primary_key=True, index=True)
    relation = CharField()
    source = IntegerField()
    target = IntegerField()
    map = IntegerField(index=True, null=True)
    removed = BooleanField(null=True)
    pass

    @classmethod
    def get_relation_of_subject(cls, subject_id):
        return cls.select().where(((cls.source == subject_id) | (cls.target == subject_id)) & (cls.removed.is_null()))


class Map(BgmIpViewer):
    id = AutoField(primary_key=True)
    pass

# Subject.create_table()
# Relation.create_table()
# Map.create_table()
