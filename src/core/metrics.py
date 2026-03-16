
```python
import numpy as np

def chi2(data, model, cov=None):
    """
    Compute chi-squared between data and model.
    data: (x, y) or (y, cov) depending on usage.
    """
    # Placeholder – actual implementation depends on data format.
    # For cosmology, often we have a vector of measurements and covariance.
    if cov is None:
        return np.sum((data - model) ** 2)
    else:
        diff = data - model
        return diff @ np.linalg.solve(cov, diff)

def aic(chi2_val, k, n_data=None):
    """Akaike Information Criterion."""
    return chi2_val + 2 * k

def bic(chi2_val, k, n_data):
    """Bayesian Information Criterion."""
    return chi2_val + k * np.log(n_data)
```
