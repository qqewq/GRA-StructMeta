
```markdown
# 4. Euclid‑ready: Preparing for Future Data

The European Space Agency’s Euclid mission will release its first cosmology data in October 2026. This repository is designed to be easily adapted to Euclid data.

## Current state

- We already use synthetic or existing data (Planck, DES, Pantheon+) to demonstrate the GRA cosmology pipeline.
- The frame interface is agnostic to data format; only the `score` method needs to change.

## Steps to integrate Euclid data

1. **Replace data loader**: when Euclid data becomes public, modify `data/load_euclid.py` (to be written) to read shear power spectra, galaxy clustering, or 3x2pt likelihoods.
2. **Adapt frames**: Some frames may need to compute predictions for weak lensing or clustering. We already have a `WLFrame` in `domains/cosmo_universe.py` (to be extended).
3. **Run the reset controller** with the new data – the same GRA mechanics will automatically rank models against Euclid’s precision.

## Why GRA is perfect for Euclid

- Euclid will produce an enormous amount of data, and many theoretical models will be tested. GRA provides a way to **automatically search the model space**.
- The reset mechanism naturally handles the **tension** between goodness‑of‑fit and model complexity (via information criteria in the reset policy).
- By keeping the best‑fitting frames, we can identify which extensions to ΛCDM (if any) are preferred.

## Example: Simulated Euclid mock

In `experiments/`, we provide `exp_cosmo_euclid_mock.ipynb` (placeholder) that uses the Euclid Flagship mock data (available from the Euclid Consortium) to test the pipeline before the real data arrives.
```
