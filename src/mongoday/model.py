from .utils.normalizer import MongoNormalizer
from .utils.func import cal_timestamp
from .field import *
from bson.objectid import ObjectId


class ValueErrorException(Exception):
    pass


DATA_TYPE_MAPPINGS = {
    'MongoIDField': MongoIDField,
    'FloatField': FloatField,
    'IntegerField': IntegerField,
    'StringField': StringField,
    'BooleanField': BooleanField,
    'MapField': MapField,
    'DateTimeField': DateTimeField,
    'EmbeddedDocumentField': EmbeddedDocumentField,
    'ReferenceField': ReferenceField,
    'ListField': ListField,

}


class BaseModel(object):
    indexes = [
        [('changed', -1)],
    ]

    def __init__(self, collection, config=None):
        self.id = MongoIDField()
        self.deleted = BooleanField(False)
        self.created = TimestampField()
        self.changed = TimestampField()

        self._collection = collection
        self.config = config

        if self.indexes:
            try:
                self._prepare_indexes(self._collection)
            except Exception as e:
                # raise Exception(f"Error creating indexes: {e}")
                # TODO: log error or do something more useful
                pass

        if self.id:
            self.initialize()

    def add_indexes(self, indexes):
        if isinstance(indexes, list):
            self.indexes.extend(indexes)

    def _prepare_indexes(self, collection):
        existing_indexes = collection.list_indexes()
        existing_index_names = [index['name'] for index in existing_indexes]

        for index_definition in self.indexes:
            index_keys = [(field, _) for field, _ in index_definition[:-1]] if isinstance(index_definition[-1],
                                                                                          dict) else [
                (field, _) for field, _ in index_definition]

            index_options = index_definition[-1] if isinstance(index_definition[-1],
                                                               dict) else {}
            index_name = "_".join([f"{field}_{_}" for field, _ in index_keys])

            if index_name not in existing_index_names:
                collection.create_index(index_keys, **index_options)

    def convert_value_by_field_type(self, field_name, value):
        field_class = type(self.__dict__[field_name])
        field_object = field_class(value)
        return field_object.value

    def __setattr__(self, key, value):
        try:
            attr = object.__getattribute__(self, key)
            if attr and isinstance(attr, BaseField):
                try:
                    update_func = '{}_alter_value'.format(key)
                    # if object.__getattribute__(self, update_func):
                    if hasattr(self, update_func):
                        value = getattr(self, update_func)(value)
                except Exception as e:
                    raise ValueErrorException(e)

                if isinstance(attr, MongoIDField):
                    object.__setattr__(self, key, MongoIDField(value))
                else:
                    field_type_class = type(attr).__name__
                    field_class = DATA_TYPE_MAPPINGS.get(field_type_class)
                    if field_class:
                        value = field_class(value)
                    else:
                        value = BaseField(value)

                    object.__setattr__(self, key, value)
        except Exception as e:
            object.__setattr__(self, key, value)

            # exception is of type ValueErrorException then raise it
            if isinstance(e, ValueErrorException):
                raise e

    def __getattribute__(self, key):
        try:
            attr = object.__getattribute__(self, key)
            if attr and isinstance(attr, BaseField):
                return attr.value

        except:
            pass

        return object.__getattribute__(self, key)

    def get(self, model_id):
        model = self._collection.find_one({'_id': ObjectId(model_id)})
        return self.initialize(model)

    def get_id(self):
        return ObjectId(self.id)

    def save(self, data=None):
        self.set_bulk_fields(data)

        fields = {}
        attrs = self.__dict__
        for k, v in attrs.items():
            if isinstance(v, MongoIDField):
                fields[k] = ObjectId(v.value) if v.value else None
            elif isinstance(v, BaseField):
                fields[k] = v.value

        if fields:
            try:
                self._perform_insert_or_update(fields)
                return self.initialize()
            except Exception as e:
                raise Exception('{} could not be saved. Error: {}'.format(self.__class__.__name__, e))

    def _perform_insert_or_update(self, fields):
        fields['changed'] = cal_timestamp()

        # delete id in any case
        if 'id' in fields:
            del fields['id']

        try:
            if not self.id:
                fields['created'] = fields['changed']
                result = self._collection.insert_one(fields)
                self.id = str(result.inserted_id)
            else:
                result = self._collection.replace_one({'_id': ObjectId(self.id)}, fields)
        except Exception as e:
            raise Exception(e)

    def delete(self, soft_delete=False):
        if self.id:
            if not soft_delete:
                self._collection.delete_one({"_id": ObjectId(self.id)})
            else:
                self.deleted = True
                self.save()

    def initialize(self, model=None):
        if isinstance(model, BaseModel):
            return model

        if not model:
            model = self._collection.find_one({'_id': ObjectId(self.id)})

        if not model:
            raise Exception('Cannot initialize ' + self.__module__)

        normalized = MongoNormalizer.deserialize(model)
        for k, v in self.get_fields().items():
            # Check to prevent any missing/new column from being initialized
            if k in normalized or (k == 'id' and '_' + k in normalized):
                self.__dict__[k].value = normalized['_' + k if k == 'id' else k]

        return self

    def get_fields(self):
        fields = {}
        attrs = self.__dict__
        for k, v in attrs.items():
            if isinstance(v, BaseField):
                fields[k] = v.value

        return fields

    def set_bulk_fields(self, data):
        if data:
            for k in data:
                self.__setattr__(k, data[k])

    def __str__(self):
        return str(self.get_fields())

    @staticmethod
    def mongo_id(mongo_id):
        return ObjectId(mongo_id)

    def get_type(self):
        return type(self).__name__.lower()
