https://orcid.org/my-orcid?orcid=0009-0004-1872-1153
https://doi.org/10.5281/zenodo.19048992
```markdown
# GRA-StructMeta: Metaprogramming of Structures with GRA-obnulënka

[![arXiv](https://img.shields.io/badge/arXiv-2512.15920-b31b1b.svg)](https://arxiv.org/abs/2512.15920)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**GRA-StructMeta** is a demonstration laboratory for **metaprogramming of structures** — frames, ontologies, classes of laws — using the GRA (Goal–Reality–Agent) reset mechanism ("obnulënka"). It shows how classical programming gives way to a higher-level paradigm where **structures compete, mutate, and are reset** based on their alignment with data or goals.

> "Classical programming is dying. Metaprogramming of structures — the next level."

## 🧠 Core Idea

In GRA, every model or theory is represented as a **GRAFrame** – an abstract container that defines:
- How to **instantiate** a concrete model from parameters,
- How to **score** that model against reality (data, consistency, etc.).

A **GRAResetController** manages a population of frames, applying a **reset policy** that kills underperforming frames and replaces them with mutations of successful ones. This is GRA-obnulënka: a continuous cycle of **selection and regeneration** of structural hypotheses.

## 🧰 Repository Structure

- `src/core/` – The minimal GRA engine: frames, reset controller, agents.
- `src/domains/` – Domain‑specific frames for micro‑physics, biology, cosmology.
- `experiments/` – Jupyter notebooks demonstrating GRA in action.
- `examples/` – Simple Python scripts to get started.
- `docs/` – Detailed concept explanations and use cases.

## 🚀 Quick Start

```bash
git clone https://github.com/yourname/GRA-StructMeta.git
cd GRA-StructMeta
pip install -e .
python examples/minimal_frame_demo.py
```

## 🔬 Experiments

1. **Micro‑law search** (`exp_micro_law_search.ipynb`): GRA frames compete to discover Newton’s second law from synthetic data.
2. **Life threshold** (`exp_bio_life_threshold.ipynb`): Frames for non‑life, proto‑life, and life are reset as a system crosses into autopoiesis.
3. **Cosmology with real data** (`exp_cosmo_from_cmb_bao_sn.ipynb`): Frames for ΛCDM, w₀wₐ, and modified gravity are compared against CMB/BAO/SNe observations. This demonstrates GRA as an automatic meta‑theory explorer.

## 📚 Documentation

- [Concept overview](docs/01_concept_overview.md)
- [GRA Frames and Reset](docs/02_gra_frames_and_resets.md)
- [Examples: Bio, Phys, Cosmo](docs/03_examples_bio_phys_cosmo.md)
- [Euclid‑ready: Future cosmology data](docs/04_euclid_ready.md)

## 🤝 Contributing

Contributions are welcome! If you have a new domain or a cool experiment, open an issue or PR.

## 📄 Citation

If you use this work, please cite the arXiv paper:

```bibtex
@article{gra2025,
  title={GRA Meta‑obnulënka: A Hierarchical Architecture for Structural Metaprogramming},
  author={oleg bitsoev},
  journal={arXiv preprint arXiv:2512.15920},
  year={2025}
}
```

## 📜 License

MIT
```



