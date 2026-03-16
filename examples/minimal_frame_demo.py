```python
#!/usr/bin/env python3
"""
Minimal example of using GRA frames and reset controller.
"""
import sys
sys.path.append('src')
from core import GRAFrame, GRAResetController, GRAAgent

# Define a simple frame for a constant model
class ConstantFrame(GRAFrame):
    def instantiate(self, c=1.0):
        self.params = {'c': c}
        return lambda x: c

    def score(self, data):
        # data is a list of target values
        if self.params is None:
            return 1e9
        c = self.params['c']
        return sum((d - c)**2 for d in data)

# Create initial population
frames = [ConstantFrame(f"const_{i}") for i in range(5)]
for i, f in enumerate(frames):
    f.instantiate(c=float(i))

# Data
data = [2.1, 1.9, 2.0, 2.2, 1.8]

# Reset policy: keep top 2
def policy(scores, frames):
    sorted_frames = sorted(frames, key=lambda f: scores[f.name])
    survivors = sorted_frames[:2]
    killed = sorted_frames[2:]
    return survivors, killed

controller = GRAResetController(frames, policy)

# Agent: mutate by adding small noise to c
def mutate(frame):
    new_c = frame.params['c'] + 0.1
    child = ConstantFrame(frame.name+"_child", parent=frame)
    child.instantiate(c=new_c)
    return child

agent = GRAAgent([mutate])

# Run a few steps
for step in range(5):
    scores, survivors, killed = controller.step(data)
    print(f"Step {step}, survivors: {[f.name for f in survivors]}")
    children = [agent.propose_child(survivors[0]) for _ in killed]
    controller.frames = survivors + children

best = min(controller.frames, key=lambda f: f.score(data))
print(f"Best constant: {best.params['c']}")
```
