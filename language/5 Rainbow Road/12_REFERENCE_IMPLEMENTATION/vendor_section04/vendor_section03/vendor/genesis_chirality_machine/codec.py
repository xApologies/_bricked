from dataclasses import dataclass
from bisect import bisect_left
from .errors import CodecError

@dataclass
class CalibratedLevelCodec:
    levels: tuple = (0.0, 1/7, 2/7, 3/7, 4/7, 5/7, 6/7, 1.0)

    def __post_init__(self):
        if len(self.levels) != 8: raise CodecError('exactly 8 levels required')
        if tuple(sorted(self.levels)) != tuple(self.levels): raise CodecError('levels must be monotonic')

    def encode(self, state_class: int) -> float:
        if not 0 <= state_class < 8: raise CodecError('state_class')
        return float(self.levels[state_class])

    def decode(self, observed: float) -> int:
        if not 0 <= observed <= 1: raise CodecError('observed level must be normalized')
        return min(range(8), key=lambda i: abs(self.levels[i]-observed))

    def thresholds(self):
        return tuple((self.levels[i]+self.levels[i+1])/2 for i in range(7))
