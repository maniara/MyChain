import json

class json_encoder(json.JSONEncoder):
    def encode(self, obj):
        obj['type'] = str(obj['type'])
        obj['ip_address'] = str(obj['ip_address'])

        return super(json_encoder, self).encode(obj)