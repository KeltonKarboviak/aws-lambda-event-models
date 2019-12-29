from base64 import b64decode


class Base64Str(str):
    """base64 encoded data validation."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, (bytes, str)):
            raise TypeError(f'bytes or string required, received {type(v)}')
        decoded = b64decode(v).decode('utf8')
        return cls(decoded)

    def __repr__(self):
        return f'Base64({super().__repr__()})'
