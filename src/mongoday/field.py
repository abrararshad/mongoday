from datetime import datetime
from bson.objectid import ObjectId


class BaseField:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class MongoIDField(BaseField):
    @property
    def value(self):
        return str(self._value) if self._value else None

    @value.setter
    def value(self, value):
        if value:
            self._value = ObjectId(value)
        else:
            raise Exception("MongoIDField expects a value")


class StringField(BaseField):
    @property
    def value(self):
        return str(self._value) if self._value else ""

    @value.setter
    def value(self, value):
        self._value = str(value) if value else ""


class IntegerField(BaseField):
    @property
    def value(self):
        return int(self._value) if self._value else 0

    @value.setter
    def value(self, value):
        if value is not None:
            if isinstance(value, int):
                self._value = value
            else:
                raise ValueError("IntegerField expects an integer")
        else:
            self._value = 0


class BooleanField(BaseField):
    @property
    def value(self):
        return bool(self._value)

    @value.setter
    def value(self, value):
        if value is not None:
            if isinstance(value, bool):
                self._value = value
            else:
                raise ValueError("BooleanField expects a boolean")
        else:
            self._value = None


class FloatField(BaseField):
    @property
    def value(self):
        return float(self._value) if self._value else 0.0

    @value.setter
    def value(self, value):
        if value is not None:
            if isinstance(value, float):
                self._value = value
            else:
                raise ValueError("FloatField expects a float")
        else:
            self._value = 0.0


class MapField(BaseField):
    @property
    def value(self):
        return dict(self._value) if self._value else {}

    @value.setter
    def value(self, value):
        if value is not None:
            if value and isinstance(value, dict):
                self._value = value
            else:
                raise ValueError("MapField expects a dict")
        else:
            self._value = {}


class ListField(BaseField):
    @property
    def value(self):
        v = super().value
        if v:
            return list(v)
        else:
            return []

    @value.setter
    def value(self, value):
        if value is not None:
            if value and isinstance(value, list):
                self._value = value
            else:
                raise ValueError("ListField expects a list")
        else:
            self._value = []


class DateTimeField(BaseField):
    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value):
        if value is not None:
            if isinstance(value, datetime):
                self._value = value
            else:
                raise ValueError("DateTimeField expects a datetime object")
        else:
            self._value = None


class TimestampField(BaseField):
    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value):
        if value is not None:
            if isinstance(value, int):
                self._value = value
            else:
                raise ValueError("DateTimeField expects a datetime object")
        else:
            self._value = None


class EmbeddedDocumentField(BaseField):
    def __init__(self, embedded_model, value=None):
        self.embedded_model = embedded_model
        super().__init__(value)

    @property
    def value(self):
        v = super().value
        if v:
            return self.embedded_model(v).to_dict()
        else:
            return None

    @value.setter
    def value(self, value):
        if value is not None:
            if isinstance(value, dict):
                self._value = self.embedded_model(value)
            else:
                raise ValueError("EmbeddedDocumentField expects a dict")
        else:
            self._value = None


class ReferenceField(BaseField):
    @property
    def value(self):
        if self._value:
            return str(self._value)
        return None

    @value.setter
    def value(self, value):
        if value is not None:
            if isinstance(value, str):
                self._value = ObjectId(value)
            else:
                raise ValueError("ReferenceField expects an ObjectId")
        else:
            self._value = None
