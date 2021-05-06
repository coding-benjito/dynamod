
class DynaContext:
    def __init__(self, model, partition, values=None):
        self.model = model
        self.partition = partition
        self.partition_stack = []
        self.values = ChainedStore(model.baseStore) if values == None else values

    def chained_by (self, store=None):
        return DynaContext(self.model, self.partition, ChainedStore(self.values, store))

    def push_partition (self, part):
        if part is None:
            part = self.partition
        self.partition_stack.append(self.partition)
        self.partition = part

    def pop_partition (self):
        self.partition = self.partition_stack.pop()

    def restricted(self, axis, value):
        return self.partition.restricted(axis, value)

    def with_prob(self, prob):
        return self.partition.with_prob(prob)

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

    def extended (self):
        return ChainedStore(self, None)

    def clear_cache (self):
        pass

class ChainedStore(ValueStore):
    def __init__(self, base:ValueStore, local:ValueStore=None):
        self.base = base
        self.local = local if local is not None else MapStore()

    def knows (self, key):
        return self.local.knows(key) or self.base.knows(key)

    def get (self, key):
        if self.local.knows(key):
            return self.local.get(key)
        return self.base.get(key)

    def put (self, key, value):
        if value is None:
            self.delete (key)
        if self.local.knows(key) or not self.base.knows(key):
            self.local.put(key, value)
        else:
            self.base.put(key, value)

    def delete (self, key):
        if self.local.knows(key) or not self.base.knows(key):
            self.local.delete(key)
        else:
            self.base.delete(key)

    def clear_cache (self):
        self.local.clear_cache()
        self.base.clear_cache()

class MapStore(ValueStore):
    def __init__(self, map=None):
        self.here = {} if map is None else map

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

