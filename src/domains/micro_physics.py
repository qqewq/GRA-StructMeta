
```python
import numpy as np
from src.core.gra_frame import GRAFrame

class ConstantAccelFrame(GRAFrame):
    def instantiate(self, a=0.0):
        self.params = {'a': a}
        return lambda t: 0.5 * a * t**2   # x(t) for constant acceleration

    def score(self, data):
        # data: (t_vals, x_obs)
        t, x_obs = data
        if self.params is None:
            return 1e9
        a = self.params['a']
        x_pred = 0.5 * a * t**2
        return np.sum((x_obs - x_pred)**2)

class LinearDragFrame(GRAFrame):
    def instantiate(self, k=0.1, v0=0.0):
        self.params = {'k': k, 'v0': v0}
        # simplified: assume v(t) = v0 * exp(-k t)
        return lambda t: v0 * np.exp(-k * t)

    def score(self, data):
        # data: (t_vals, v_obs)
        t, v_obs = data
        if self.params is None:
            return 1e9
        k, v0 = self.params['k'], self.params['v0']
        v_pred = v0 * np.exp(-k * t)
        return np.sum((v_obs - v_pred)**2)

class NewtonFrame(GRAFrame):
    def instantiate(self, F=1.0, m=1.0):
        self.params = {'F': F, 'm': m}
        return lambda t: 0.5 * (F/m) * t**2   # x(t) for constant force

    def score(self, data):
        t, x_obs = data
        if self.params is None:
            return 1e9
        F, m = self.params['F'], self.params['m']
        x_pred = 0.5 * (F/m) * t**2
        return np.sum((x_obs - x_pred)**2)
```

