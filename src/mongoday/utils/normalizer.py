from bson.json_util import dumps
from json import loads as json_loads


class MongoNormalizer:

    @classmethod
    def _handle_oid(cls, record):
        if '$oid' in record:
            return record['$oid']
        return record

    @classmethod
    def deserialize(cls, data, use_new_format=False):
        if not data:
            return [] if isinstance(data, list) else None

        records = json_loads(dumps(data))

        is_single_record = not isinstance(records, list)
        if is_single_record:
            records = [records]

        for record in records:
            for key, value in list(record.items()):
                if isinstance(value, dict):
                    record[key] = cls._handle_oid(value)

            if use_new_format and '_id' in record:
                record['id'] = record.pop('_id')

        return records[0] if is_single_record else records
