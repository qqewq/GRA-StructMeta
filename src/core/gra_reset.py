
```python
class GRAResetController:
    """Manages a population of frames and applies reset policy at each step."""

    def __init__(self, frames, reset_policy):
        self.frames = list(frames)
        self.reset_policy = reset_policy

    def step(self, data):
        """Evaluate frames, apply policy, update internal list."""
        scores = {}
        for f in self.frames:
            scores[f.name] = f.score(data)

        survivors, killed = self.reset_policy(scores, self.frames)
        self.frames = survivors
        return scores, survivors, killed
```

