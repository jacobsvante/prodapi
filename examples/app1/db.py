_storage = []


async def persist(model):
    _storage.append(model)


async def fetch(limit: int = 10):
    return _storage[0:limit]
