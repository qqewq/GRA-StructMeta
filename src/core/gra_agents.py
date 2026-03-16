
```python
import random

class GRAAgent:
    """Generates new frames by mutating existing ones."""

    def __init__(self, mutation_ops):
        """
        mutation_ops: list of callables that take a frame and return a new frame.
        """
        self.mutation_ops = mutation_ops

    def propose_child(self, parent_frame):
        op = random.choice(self.mutation_ops)
        return op(parent_frame)
```

