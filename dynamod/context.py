
class DynaContext:
    def __init__(self, model, values=None):
        self.model = model
        self.partition = model.partition
        self.values = ChainedStore(model.baseStore) if values == None else values

    def chained_by (self, store=None):
        return DynaContext(self.model, ChainedStore(self.values, store))

class ValueStore:
    def knows (self, key):
        pass

    def get (self, key):
        pass

    def put (self, key, value):
        pass

    def delete (self, key):
        pass

    def extendedBy (self, store):
        return ChainedStore(self, store)

    def clear_cache (self):
        pass

class ChainedStore(ValueStore):
    def __init__(self, base:ValueStore, local:ValueStore=None):
        self.secondary = base
        self.primary = local if local is not None else MapStore()

    def knows (self, key):
        return self.primary.knows(key) or self.secondary.knows(key)

    def get (self, key):
        if self.primary.knows(key):
            return self.primary.get(key)
        return self.secondary.get(key)

    def put (self, key, value):
        if value is None:
            self.delete (key)
        if self.primary.knows(key) or not self.secondary.knows(key):
            self.primary.put(key, value)
        else:
            self.secondary.put(key, value)

    def delete (self, key):
        if self.primary.knows(key) or not self.secondary.knows(key):
            self.primary.delete(key)
        else:
            self.secondary.delete(key)

    def clear_cache (self):
        self.primary.clear_cache()
        self.secondary.clear_cache()

class MapStore(ValueStore):
    def __init__(self, map=None):
        self.here = [] if map is None else map

    def knows (self, key):
        return key in self.here

    def get (self, key):
        if key in self.here:
            return self.here[key]
        return None

    def put (self, key, value):
        if value is None:
            self.delete (key)
        self.here[key] = value

    def delete (self, key):
        if key in self.here:
            del (self.here[key])

class ImmutableMapStore(MapStore):
    def put (self, key, value):
        raise ValueError("cannot modify " + key)

    def delete (self, key):
        raise ValueError("cannot modify " + key)

