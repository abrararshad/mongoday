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
            self._value = int(value)


class BooleanField(BaseField):
    @property
    def value(self):
        return bool(self._value)

    @value.setter
    def value(self, value):
        if value is not None:
            self._value = bool(value)


class FloatField(BaseField):
    @property
    def value(self):
        return float(self._value) if self._value else 0.0

    @value.setter
    def value(self, value):
        if value is not None:
            self._value = float(value)


class MapField(BaseField):
    @property
    def value(self):
        return dict(self._value) if self._value else {}

    @value.setter
    def value(self, value):
        self._value = dict(value) if value else {}


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
        if value:
            self._value = list(value)


class DateTimeField(BaseField):
    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value):
        if isinstance(value, datetime):
            self._value = value
        else:
            raise ValueError("DateTimeField expects a datetime object")


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
        self._value = self.embedded_model(value)


class ReferenceField(BaseField):
    @property
    def value(self):
        if self._value:
            return str(self._value)
        return None

    @value.setter
    def value(self, value):
        if value:
            self._value = ObjectId(value)
