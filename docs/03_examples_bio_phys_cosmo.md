(Этот файл будет большим, поэтому дам его краткую версию с основными блоками. Полный текст можно будет расширить позже.)

```markdown
# 3. Examples: Bio, Phys, Cosmo

This document describes three concrete experiments implemented in the repository, demonstrating GRA metaprogramming in different domains.

## 3.1 Micro‑physics: Discovering Newton’s Second Law

**Goal**: Show that GRA frames can rediscover a fundamental law from noisy data.

**Data**: Synthetic observations of position, velocity, acceleration for an object under constant force. Actually we generate (x, v, a) with a = F/m + noise.

**Frames**:
- `ConstantAccelFrame`: assumes a = constant, fits a to data.
- `LinearDragFrame`: assumes a = -k v + constant.
- `NewtonFrame`: assumes a = F/m, fits F and m.

**Reset policy**: Keep only frames with low χ², kill others, mutate survivors by tweaking the assumed functional form (e.g., add a term).

**Outcome**: After several generations, the NewtonFrame dominates and accurately recovers F and m.

## 3.2 Biology: Life Threshold (Autopoiesis)

**Goal**: Simulate a system that transitions from non‑life to proto‑life to life, and let GRA frames capture the thresholds.

**Model**: A simple cellular automaton or reaction network with parameters controlling self‑maintenance. A "life score" measures degree of autopoiesis (e.g., boundary maintenance, self‑repair).

**Frames**:
- `NonLivingFrame`: predicts no life score.
- `ProtoLifeFrame`: predicts low life score, simple metabolism.
- `LifeFrame`: predicts high life score, with reproduction.

**Reset policy**: As the system evolves, frames that incorrectly predict the life score are killed. Over time, the population shifts from NonLiving to ProtoLife to Life.

**Outcome**: The GRA process automatically identifies the correct "theory of life" for the given simulation.

## 3.3 Cosmology: Competing Models of Dark Energy (with real data)

This is the flagship experiment. We use real cosmological data (CMB, BAO, SNe) to let GRA frames explore alternatives to ΛCDM.

**Data** (see `data/README.md` for sources):
- CMB: Planck 2018 distance priors (100θ_MC, R, l_a) or compressed likelihood.
- BAO: SDSS DR12, DES Y3, etc. (D_V/r_d, H(z) r_d).
- SNe: Pantheon+ (distance moduli and covariance).

**Frames**:
- `LCDMFrame`: flat ΛCDM with parameters (Ω_m, H0).
- `CPLFrame`: dark energy with w(a) = w0 + wa(1-a).
- `ModifiedGravityFrame`: simple phenomenological MG parametrisation (e.g., μ, Σ).
- `SplineFrame`: non‑parametric w(z) represented by cubic spline knots.

Each frame must implement:
- `instantiate(params)`: returns a function that computes H(z) or distance moduli.
- `score(data)`: computes χ² or likelihood against the combined data set.

**Reset policy**: Rank frames by AIC or BIC (to penalise complexity). Keep top 20%, kill rest. Mutation operators:
- For parametric frames: slightly perturb parameters.
- For non‑parametric frames: add/remove a knot, change regularisation.
- Cross‑over: combine two frames (e.g., take early universe from one, late from another).

**Outcome**: After many generations, the surviving frames represent the most parsimonious descriptions of the data. If ΛCDM is truly the best, it should dominate; otherwise, alternatives may emerge.

**Implementation details** are in `experiments/exp_cosmo_from_cmb_bao_sn.ipynb`.
```

