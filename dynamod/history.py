from dynamod.core import *

class History:
    def __init__(self, model):
        self.model = model
        self.track = set()
        self.incoming = [{}]
        self.matrix = []
        self.results = {}
        for name in self.model.results:
            self.results[name] = []

    def get_incoming(self, segment, t, rfactor):
        key = deslice(segment)
        if key in self.track:
            if t > 0:
                if key in self.incoming[t]:
                    return self.incoming[t][key]
        else:
            self.track.add(key)
        return rfactor * self.matrix[0][segment]

    def keep_track (self):
        tracks = {}
        for key in self.track:
            tracks[key] = self.model.incoming[reslice(key)]
        self.incoming.append(tracks)

    def store(self):
        self.matrix.append(self.model.matrix.copy())
        for name, expr in self.model.results.items():
            self.results[name].append (self.model.evalExpr(expr))

