```markdown
# Data Sources for Cosmology Experiment

This folder is for storing datasets used in the cosmology experiment. Due to size, we do not include them in the repository, but provide instructions to download.

## CMB
- Planck 2018 compressed likelihood: [Planck Legacy Archive](https://pla.esac.esa.int/) or use the `plancklens` package.
- We recommend using the `Planck18` distance priors (R, l_a, Ω_b h²) from [arXiv:1807.06209](https://arxiv.org/abs/1807.06209).

## BAO
- SDSS DR12 (BOSS) consensus: [SDSS DR12](https://www.sdss.org/dr12/)
- DES Y3 BAO measurements: [DES data](https://www.darkenergysurvey.org/)
- For convenience, use the collection from [NASA/IPAC](https://ned.ipac.caltech.edu/)

## SNe
- Pantheon+ : [Pantheon+ SH0ES](https://github.com/PantheonPlusSH0ES/DataRelease)

## Mock Euclid
- Euclid Flagship mock: available through [Euclid Consortium](https://www.euclid-ec.org/) (members only); public mocks may be released later.

We provide a script `download_data.py` (not yet) to fetch small samples.
```

