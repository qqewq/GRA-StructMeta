
```python
import numpy as np
from src.core.gra_frame import GRAFrame

class NonLivingFrame(GRAFrame):
    def instantiate(self, threshold=0.0):
        self.params = {'threshold': threshold}
        # predicts life score always below threshold
        return lambda sim: 0.0

    def score(self, data):
        # data is the actual life score from simulation
        life_score_actual = data
        # we want to be correct: predict low life for non‑living systems
        # so if actual > threshold, penalise
        threshold = self.params['threshold']
        if life_score_actual > threshold:
            return 100.0   # high penalty
        else:
            return 0.0

class ProtoLifeFrame(GRAFrame):
    def instantiate(self, low=0.2, high=0.8):
        self.params = {'low': low, 'high': high}
        # predicts life score between low and high
        return lambda sim: (low + high)/2

    def score(self, data):
        actual = data
        low, high = self.params['low'], self.params['high']
        if low <= actual <= high:
            return 0.0
        else:
            # distance to interval
            return min(abs(actual-low), abs(actual-high))

class LifeFrame(GRAFrame):
    def instantiate(self, min_life=0.9):
        self.params = {'min_life': min_life}
        # predicts life score above min_life
        return lambda sim: min_life + 0.1   # just an example

    def score(self, data):
        actual = data
        if actual >= self.params['min_life']:
            return 0.0
        else:
            return (self.params['min_life'] - actual) * 100
```

