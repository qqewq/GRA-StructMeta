
```python
from abc import ABC, abstractmethod

class GRAFrame(ABC):
    """Abstract base class for all GRA frames."""

    def __init__(self, name, parent=None, meta=None):
        self.name = name
        self.parent = parent
        self.meta = meta or {}
        self.params = None  # can be set after instantiation

    @abstractmethod
    def instantiate(self, **kwargs):
        """
        Create a concrete model/function from parameters.
        Typically stores the parameters in self.params and returns a callable.
        """
        pass

    @abstractmethod
    def score(self, data):
        """
        Evaluate the instantiated model against data.
        Should return a scalar; lower is better (e.g., chi-squared).
        """
        pass
```

