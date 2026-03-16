#!/usr/bin/env python3
"""
Out-of-Domain Inheritance Demo for GRA Frames

This example demonstrates how GRA frames can inherit from one another,
and how mutation can produce child frames that belong to different domains.
The reset controller manages a population of frames that evolve over time,
with inheritance tracking via the `parent` attribute.
"""

import sys
import numpy as np
sys.path.append('src')
from core import GRAFrame, GRAResetController, GRAAgent
from core.metrics import chi2

# ----------------------------------------------------------------------
# Define a hierarchy of frames for different domains
# ----------------------------------------------------------------------

class BaseFrame(GRAFrame):
    """Abstract base for all frames in this demo."""
    def instantiate(self, **kwargs):
        self.params = kwargs
        return lambda x: x  # placeholder

    def score(self, data):
        # To be overridden
        raise NotImplementedError

class LinearFrame(BaseFrame):
    """Frame for linear models: y = a*x + b."""
    def instantiate(self, a=1.0, b=0.0):
        self.params = {'a': a, 'b': b}
        return lambda x: a * x + b

    def score(self, data):
        x, y = data
        if self.params is None:
            return 1e9
        a, b = self.params['a'], self.params['b']
        y_pred = a * x + b
        return chi2(y, y_pred)

class QuadraticFrame(BaseFrame):
    """Frame for quadratic models: y = a*x^2 + b*x + c."""
    def instantiate(self, a=0.0, b=1.0, c=0.0):
        self.params = {'a': a, 'b': b, 'c': c}
        return lambda x: a * x**2 + b * x + c

    def score(self, data):
        x, y = data
        if self.params is None:
            return 1e9
        a, b, c = self.params['a'], self.params['b'], self.params['c']
        y_pred = a * x**2 + b * x + c
        return chi2(y, y_pred)

class ExponentialFrame(BaseFrame):
    """Frame for exponential models: y = a * exp(b*x)."""
    def instantiate(self, a=1.0, b=0.1):
        self.params = {'a': a, 'b': b}
        return lambda x: a * np.exp(b * x)

    def score(self, data):
        x, y = data
        if self.params is None:
            return 1e9
        a, b = self.params['a'], self.params['b']
        y_pred = a * np.exp(b * x)
        # Avoid log of negative
        if np.any(y_pred <= 0):
            return 1e9
        return chi2(y, y_pred)

# ----------------------------------------------------------------------
# Generate synthetic data from a linear process (with noise)
# ----------------------------------------------------------------------
np.random.seed(42)
x_data = np.linspace(0, 5, 20)
true_a, true_b = 2.5, 1.2
y_true = true_a * x_data + true_b
y_obs = y_true + np.random.normal(0, 1.0, size=x_data.shape)
data = (x_data, y_obs)

print("True underlying process: linear with a=2.5, b=1.2")

# ----------------------------------------------------------------------
# Create initial population with a mix of frames
# ----------------------------------------------------------------------
frames = []
# Add a few linear frames with random parameters
for i in range(3):
    f = LinearFrame(f"linear_{i}")
    f.instantiate(a=np.random.uniform(0,5), b=np.random.uniform(0,3))
    frames.append(f)
# Add a few quadratic frames
for i in range(3):
    f = QuadraticFrame(f"quad_{i}")
    f.instantiate(a=np.random.uniform(0,1), b=np.random.uniform(0,3), c=np.random.uniform(-2,2))
    frames.append(f)
# Add a few exponential frames
for i in range(3):
    f = ExponentialFrame(f"exp_{i}")
    f.instantiate(a=np.random.uniform(0.5,5), b=np.random.uniform(-0.5,0.5))
    frames.append(f)

print(f"Initial population size: {len(frames)}")

# ----------------------------------------------------------------------
# Define reset policy (keep top 30%)
# ----------------------------------------------------------------------
def top_k_policy(scores, frames, k=0.3):
    sorted_frames = sorted(frames, key=lambda f: scores[f.name])
    n_keep = max(1, int(len(frames) * k))
    survivors = sorted_frames[:n_keep]
    killed = sorted_frames[n_keep:]
    return survivors, killed

# ----------------------------------------------------------------------
# Define mutation operators that can produce children of different types
# ----------------------------------------------------------------------
def mutate_perturb(frame):
    """Perturb parameters slightly, keeping same frame type."""
    if isinstance(frame, LinearFrame):
        a = frame.params['a'] * np.random.uniform(0.9, 1.1)
        b = frame.params['b'] * np.random.uniform(0.9, 1.1)
        child = LinearFrame(frame.name + "_child", parent=frame)
        child.instantiate(a=a, b=b)
    elif isinstance(frame, QuadraticFrame):
        a = frame.params['a'] * np.random.uniform(0.9, 1.1)
        b = frame.params['b'] * np.random.uniform(0.9, 1.1)
        c = frame.params['c'] * np.random.uniform(0.9, 1.1)
        child = QuadraticFrame(frame.name + "_child", parent=frame)
        child.instantiate(a=a, b=b, c=c)
    elif isinstance(frame, ExponentialFrame):
        a = frame.params['a'] * np.random.uniform(0.9, 1.1)
        b = frame.params['b'] * np.random.uniform(0.9, 1.1)
        child = ExponentialFrame(frame.name + "_child", parent=frame)
        child.instantiate(a=a, b=b)
    else:
        child = frame
    return child

def mutate_change_type(frame):
    """Switch to a different frame type, inheriting approximate behaviour."""
    # For simplicity, we just create a random frame of a different type.
    # In practice, you could try to map parameters.
    types = [LinearFrame, QuadraticFrame, ExponentialFrame]
    current_type = type(frame)
    new_type = np.random.choice([t for t in types if t != current_type])
    # Create with random parameters
    if new_type == LinearFrame:
        child = LinearFrame(frame.name + "_changed", parent=frame)
        child.instantiate(a=np.random.uniform(0,5), b=np.random.uniform(0,3))
    elif new_type == QuadraticFrame:
        child = QuadraticFrame(frame.name + "_changed", parent=frame)
        child.instantiate(a=np.random.uniform(0,1), b=np.random.uniform(0,3), c=np.random.uniform(-2,2))
    else:
        child = ExponentialFrame(frame.name + "_changed", parent=frame)
        child.instantiate(a=np.random.uniform(0.5,5), b=np.random.uniform(-0.5,0.5))
    return child

# Agent with two mutation operators
agent = GRAAgent([mutate_perturb, mutate_change_type])

# Controller
controller = GRAResetController(frames, lambda s,f: top_k_policy(s,f,k=0.3))

# ----------------------------------------------------------------------
# Run reset cycles
# ----------------------------------------------------------------------
n_epochs = 20
history = []  # list of best scores

for epoch in range(n_epochs):
    scores, survivors, killed = controller.step(data)
    best_score = min(scores.values())
    history.append(best_score)

    # Generate children to replace killed
    children = []
    for _ in killed:
        parent = np.random.choice(survivors)
        child = agent.propose_child(parent)
        children.append(child)

    controller.frames = survivors + children

    if epoch % 5 == 0:
        print(f"Epoch {epoch:2d}: best score = {best_score:.4f}, population size = {len(controller.frames)}")

# ----------------------------------------------------------------------
# Show final best frame
# ----------------------------------------------------------------------
final_scores = {f.name: f.score(data) for f in controller.frames}
best_frame = min(controller.frames, key=lambda f: final_scores[f.name])
print("\n" + "="*50)
print("Final best frame:")
print(f"  Name: {best_frame.name}")
print(f"  Type: {type(best_frame).__name__}")
print(f"  Params: {best_frame.params}")
print(f"  Score: {final_scores[best_frame.name]:.4f}")
print(f"  Parent: {best_frame.parent.name if best_frame.parent else None}")
print("="*50)

# Plot data and best model
import matplotlib.pyplot as plt
x_plot = np.linspace(0, 5, 100)
model = best_frame.instantiate()(x_plot) if hasattr(best_frame, 'instantiate') else None
if model is not None:
    plt.figure(figsize=(8,5))
    plt.errorbar(x_data, y_obs, yerr=1.0, fmt='o', label='Data', capsize=3)
    plt.plot(x_plot, model, 'r-', label=f'Best model ({type(best_frame).__name__})')
    plt.plot(x_plot, true_a * x_plot + true_b, 'k--', label='True linear')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.legend()
    plt.title('Out-of-Domain Inheritance Demo')
    plt.grid(alpha=0.3)
    plt.show()