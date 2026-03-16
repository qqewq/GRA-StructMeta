```python
import numpy as np
from scipy.integrate import quad
from src.core.gra_frame import GRAFrame

# Helper cosmology functions (simplified)

def H_z_LCDM(z, Om, H0):
    Or = 0.0  # neglect radiation
    Ol = 1.0 - Om
    return H0 * np.sqrt(Om*(1+z)**3 + Ol)

def H_z_CPL(z, Om, w0, wa, H0):
    # w(a) = w0 + wa*(1-a)
    def integrand(zp):
        return (1 + w0 + wa * (zp/(1+zp))) / (1+zp)
    # more accurate: need to compute dark energy density evolution
    # For simplicity, we use an approximation here; real code would integrate.
    # This is just a placeholder.
    Or = 0.0
    Ol = 1.0 - Om
    # approximate: rho_de ~ exp(3 int (1+w) dln(1+z))
    # We'll just return LCDM for now; replace with actual CPL later.
    return H0 * np.sqrt(Om*(1+z)**3 + Ol)

class LCDMFrame(GRAFrame):
    def instantiate(self, Om=0.3, H0=70):
        self.params = {'Om': Om, 'H0': H0}
        return lambda z: H_z_LCDM(z, Om, H0)

    def score(self, data):
        # data is a dict containing 'z', 'H_obs', 'err_H', and similarly for other probes
        # For simplicity, we combine chi2 from Hubble and distance moduli.
        # Real implementation would compute full likelihood.
        # Placeholder:
        z = data['z']
        H_obs = data['H_obs']
        err_H = data['err_H']
        H_pred = self.instantiate()(z)   # call with stored params
        chi2_H = np.sum(((H_obs - H_pred)/err_H)**2)
        return chi2_H

class CPLFrame(GRAFrame):
    def instantiate(self, Om=0.3, w0=-1.0, wa=0.0, H0=70):
        self.params = {'Om': Om, 'w0': w0, 'wa': wa, 'H0': H0}
        return lambda z: H_z_CPL(z, Om, w0, wa, H0)

    def score(self, data):
        # similar to LCDM but with different H(z)
        pass

class ModifiedGravityFrame(GRAFrame):
    def instantiate(self, Om=0.3, H0=70, mu=0.0):
        self.params = {'Om': Om, 'H0': H0, 'mu': mu}
        # placeholder: just return LCDM
        return lambda z: H_z_LCDM(z, Om, H0)

    def score(self, data):
        pass
```

(Для космологии потребуется более серьёзная реализация, включая расчёт расстояний и интегрирование. В рамках демо можно оставить заглушки.)

