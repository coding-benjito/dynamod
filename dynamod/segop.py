from dynamod.core import *

class Segop:
    def __init__(self, model, seg=None, change=None, share=1):
        self.model = model
        self.n = len(model.attSystem.attributes)
        self.change = [None for att in model.attSystem.attributes] if change is None else change.copy()
        self.seg = tuple(self.change) if seg is None else seg
        self.share = 1 if share is None else share

    def set_value (self, iaxis, ivalue):
        on = self.seg[iaxis]
        if on is None or (isinstance(on, list) and ivalue in on):
            raise EvaluationError("illegal attribute assignament")
        if ivalue != on:
            self.change[iaxis] = ivalue

    def needs_split (self, iaxis, ivalue):
        on = self.seg[iaxis]
        return on is None or (isinstance(on, list) and ivalue in on)

    def has_segment (self, iaxis, ivalue):
        on = self.seg[iaxis]
        if on == ivalue:
            return True
        if on is None or isinstance(on, list):
            raise self.miss (iaxis)
        return False

    def miss (self, iaxis):
        return MissingAxis(self.model.attSystem.attributes[iaxis].name)

    def has_segments (self, iaxis, ivalues):
        on = self.seg[iaxis]
        if on is None:
            raise self.miss(iaxis)
        if not isinstance(on, list):
            return on in ivalues
        sect = set(ivalues) & set(on)
        if len(sect) == 0:
            return False
        if len(sect) == len(ivalues):
            return True
        raise self.miss(iaxis)

    def has_value (self, iaxis, ivalue):
        return self.seg[iaxis] == ivalue

    def modified_by_seg(self, seg):
        return Segop(self.model, seg, self.change, self.share)

    def split_on_prob(self, prob):
        splits = []
        splits.append(Segop(self.model, self.seg, self.change, prob * self.share))
        splits.append(Segop(self.model, self.seg, self.change, (1-prob) * self.share))
        return splits

    def split_on_att(self, iaxis, ivalue):
        splits = []
        on = self.seg[iaxis]
        if on is None:
            splits.append(self.modified_by_seg(modified_seg(self.seg, iaxis, ivalue)))
            others = list(range(len(self.model.attSystem.attributes[iaxis].values)))
            others.remove(ivalue)
            if len(others) == 1:
                others = others[0]
            splits.append(self.modified_by_seg(modified_seg(self.seg, iaxis, others)))
        elif isinstance(on, list) and ivalue in on:
            splits.append(self.modified_by_seg(modified_seg(self.seg, iaxis, ivalue)))
            others = on.copy()
            others.remove(ivalue)
            if len(others) == 1:
                others = others[0]
            splits.append(self.modified_by_seg(modified_seg(self.seg, iaxis, others)))
        else:
            raise EvaluationError("illegal attribute split")
        return splits

    def split_on_attlist(self, iaxis, ivalues):
        splits = []
        on = self.seg[iaxis]
        if on is None:
            splits.append(self.modified_by_seg(modified_seg(self.seg, iaxis, ivalues)))
            all = range(len(self.model.attSystem.attributes[iaxis].values))
            others = [x for x in all if x not in ivalues]
            if len(others) == 1:
                others = others[0]
            splits.append(self.modified_by_seg(modified_seg(self.seg, iaxis, others)))
        elif isinstance(on, list):
            these = [x for x in on if x in ivalues]
            others = [x for x in on if x not in ivalues]
            if len(others) == 1:
                others = others[0]
            if len(these) == 1:
                these = these[0]
            splits.append(self.modified_by_seg(modified_seg(self.seg, iaxis, these)))
            splits.append(self.modified_by_seg(modified_seg(self.seg, iaxis, others)))
        else:
            if on in ivalues:
                splits.append(self)
            else:
                splits.append (self.modified_by_seg(modified_seg(self.seg, iaxis, [])))
        return splits

    def split_on_axis(self, iaxis):
        splits = []
        on = self.seg[iaxis]
        if on is None:
            all = list(range(len(self.model.attSystem.attributes[iaxis].values)))
        elif isinstance(on, list):
            all = on
        for ivalue in all:
            splits.append(self.modified_by_seg(modified_seg(self.seg, iaxis, ivalue)))
        return splits

    def split_by_shares(self, iaxis, shares:dict):
        splits = []
        for ivalue, share in shares.items():
            seg = Segop(self.model, self.seg, self.change, share * self.share)
            if seg.needs_split(iaxis, ivalue):
                segs = seg.split_on_axis(iaxis)
                for sseg in segs:
                    sseg.set_value(iaxis, ivalue)
                splits.extend(segs)
            else:
                seg.set_value(iaxis, ivalue)
                splits.append(seg)
        return splits

    #return 3-tuple sout, sin, tosum
    def apply(self):
        sout = []
        sin = []
        tosum = []
        axis = 0
        for on, to in zip(self.seg, self.change):
            if on is None:
                sout.append(NOSLICE)
                sin.append(NOSLICE)
                axis += 1
            else:
                sout.append(on)
                if isinstance(on, list):
                    if to is None:
                        sin.append(on)
                    else:
                        sin.append(to)
                        tosum.append(axis)
                    axis += 1
                else:
                    if to is None:
                        sin.append(on)
                    else:
                        sin.append(to)
        return tuple(sout), tuple(sin), (tuple(tosum) if len(tosum) > 0 else None)

    def __str__(self):
        text = ""
        if self.share != 1:
            text += "for " + str(self.share) + " "
        text += "on " + str(self.seg)
        text += " do " + str(self.change)
        return text