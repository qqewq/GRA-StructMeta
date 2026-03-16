
```markdown
# 2. GRA Frames and Reset Controller: Usage Guide

This document explains how to use the core classes in `src/core/`.

## GRAFrame (abstract base class)

```python
from abc import ABC, abstractmethod

class GRAFrame(ABC):
    def __init__(self, name, parent=None, meta=None):
        self.name = name
        self.parent = parent   # optional parent frame (for inheritance tracking)
        self.meta = meta or {}

    @abstractmethod
    def instantiate(self, **kwargs):
        """Return a concrete model/function given parameters."""
        pass

    @abstractmethod
    def score(self, data):
        """Return a score (lower is better, e.g., χ²) for the instantiated model."""
        pass
```

## Implementing a custom frame

For example, a frame representing a linear model:

```python
class LinearFrame(GRAFrame):
    def instantiate(self, a=1.0, b=0.0):
        # returns a function f(x) = a*x + b
        return lambda x: a*x + b

    def score(self, data):
        # data: (x_vals, y_vals)
        x, y = data
        # fit parameters to data (or use given ones)
        # here we assume the frame already has parameters set externally
        # in practice you'd store the parameters in the instance
        # for simplicity, we use a simple least squares error
        if not hasattr(self, 'params'):
            return 1e9   # huge error if not instantiated
        a, b = self.params
        y_pred = a*x + b
        return np.sum((y - y_pred)**2)
```

But better: separate the parameter choice from scoring. Usually you'll store the best‑fit parameters inside the frame after instantiation.

## GRAResetController

```python
class GRAResetController:
    def __init__(self, frames, reset_policy):
        self.frames = frames          # list of GRAFrame objects
        self.reset_policy = reset_policy   # function(scores, frames) -> survivors, killed

    def step(self, data):
        scores = {}
        for f in self.frames:
            # optionally, first instantiate with some strategy (e.g., sample parameters)
            # here we assume the frame already has parameters set before step
            scores[f.name] = f.score(data)

        survivors, killed = self.reset_policy(scores, self.frames)
        self.frames = survivors
        return scores, survivors, killed
```

## Reset Policies

A reset policy is a callable that takes a dict of scores and the list of frames, and returns two lists: survivors and killed.

Example: keep top 50%, kill bottom 50%, then replace killed with mutations of survivors.

```python
def top_k_policy(scores, frames, k=0.5):
    # sort frames by score (lower is better)
    sorted_frames = sorted(frames, key=lambda f: scores[f.name])
    n_keep = int(len(frames) * k)
    survivors = sorted_frames[:n_keep]
    killed = sorted_frames[n_keep:]
    return survivors, killed
```

## GRAAgent

Agents generate new frames from existing ones.

```python
class GRAAgent:
    def __init__(self, mutation_ops):
        self.mutation_ops = mutation_ops   # list of functions that take a frame and return a new frame

    def propose_child(self, parent_frame):
        # randomly choose a mutation op and apply
        import random
        op = random.choice(self.mutation_ops)
        return op(parent_frame)
```

## Putting it together

```python
frames = [LinearFrame("linear1"), LinearFrame("linear2"), ...]
policy = lambda s,f: top_k_policy(s,f,k=0.5)
controller = GRAResetController(frames, policy)
agent = GRAAgent([lambda p: p, ...])   # trivial mutation: copy

for epoch in range(10):
    scores, survivors, killed = controller.step(data)
    # generate children from survivors
    children = [agent.propose_child(random.choice(survivors)) for _ in killed]
    controller.frames = survivors + children
```

See `examples/minimal_frame_demo.py` for a runnable example.
```

---
