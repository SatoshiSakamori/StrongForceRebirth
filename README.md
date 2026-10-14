# StrongForceRebirth

**A critical, exploratory hypothesis — not an established physical theory**

Original idea: Satoshi Sakamori (坂森 聡)

## Original intuition / 元の着想

宇宙が極端な加速膨張（Big Rip）へ進むと、強い力で結びついた状態も破壊されるのではないか。QCDの結合が引き延ばされれば、ストリング・ブレーキングによって粒子・反粒子が生まれる。この粒子生成が宇宙膨張に反作用し、膨張を弱める可能性はないだろうか？

The key question is **not** whether string breaking exists (it does), but whether cosmological tidal disruption can produce a significant *energy transfer/backreaction* capable of changing the phantom-driven expansion.

## Current scientific assessment (2026-10-14)

| Claim | Status |
| --- | --- |
| Phantom expansion can eventually disrupt bound structures, potentially including nucleons | Established within particular Big Rip models; the Big Rip itself is unconfirmed |
| QCD flux tubes may break by quark–antiquark pair production | Supported by lattice QCD in applicable QCD systems |
| Cosmological tidal disruption of hadrons triggers that same QCD process | **Not demonstrated here** |
| That process directly drains the phantom component with only metric-mediated coupling in Einstein/semiclassical gravity | **No direct transfer term in this setting**; each complete sector is separately covariantly conserved |
| An added phantom–QCD coupling provides positive, sufficient, stable energy transfer | **Not demonstrated**; an explicit candidate and falsification conditions are specified in the research note |
| The resulting particles halt a Big Rip or cause rebirth | **No demonstration** |

Ordinary accelerated expansion (e.g. a cosmological constant) does **not** imply eventual destruction of nuclei. The relevant quantity for tidal relative acceleration is \(\ddot a/a=H^2+\dot H\), not \(H\) alone.

### Priority investigation: direct phantom-to-QCD energy transfer

[日本語の研究ノート・導出・反証条件](research/phantom_qcd_energy_transfer.md) distinguishes a definite result under stated assumptions from open dynamical questions. With separate actions \(S_X[g,\phi]+S_{QCD}[g,A,q]\), both full stress tensors obey their own conservation equations. Particle creation and gravitational backreaction do not by themselves insert a sink into the phantom continuity equation. This is a statement about classical/semiclassical Einstein gravity with no cross-sector operators, not a prohibition of every quantum-gravitational effect or indirect backreaction.

The note proposes an **additional, hypothetical** gauge-kinetic coupling \(-B(\phi)F^2/4\), for which the specified sector split yields \(Q=\dot B\langle F^2\rangle_{ren}/4\). Its sign, irreversible particle yield, magnitude, stability and observational viability still require a microscopic calculation; a wrong-sign scalar is not a healthy completion.

[Executable controls](research/verify_energy_transfer.py) and [recorded results](research/calculation_results.json) cover dust/radiation FLRW solutions, finite-duration transfer, free-field particle production, and the coupling's classical sign. Run `python3 research/verify_energy_transfer.py` from the repository root (standard library only). Analytic comparisons and convergence checks pass. **These controls are not real-time QCD or a self-consistent semiclassical backreaction solution.** The original intuition remains preserved above as a research question.

## Corrected equations and interpretation

For a spatially flat FLRW universe and energy densities \(\rho\) in natural units \(c=1\):

\[
H^2=\frac{8\pi G}{3}(\rho_X+\rho_m),\qquad
\dot H=-4\pi G[(1+w_X)\rho_X+\rho_m],
\]

where \(w_X<-1\) characterizes hypothetical phantom energy and pressureless matter has \(w_m=0\).

A **phenomenological** energy-transfer term \(Q\) can be explored by:

\[
\dot\rho_X+3H(1+w_X)\rho_X=-Q,\qquad
\dot\rho_m+3H\rho_m=Q.
\]

The opposite signs are necessary for total covariant stress-energy conservation in this homogeneous model. **Q is an assumption to be derived or constrained, not a consequence of QCD.** Positive Q means energy flows from X to matter. Q=0 is the baseline. Merely adding matter, without specifying the source and ensuring conservation, is not a physical solution.

Key distinctions:
- \(\dot H=0\): expansion rate momentarily stationary;
- \(\ddot a=0\): acceleration vanishes (\(H^2+\dot H=0\));
- \(H=0\): expansion halts; a bounce/rebirth needs still more physics.

For \(w_X=-1.1\), a mixture with matter has \(\dot H\le0\) if \(\rho_m\ge0.1\rho_X\), while \(\ddot a\le0\) needs \(\rho_m\ge2.3\rho_X\). These are instantaneous conditions, **not** proof the Big Rip is avoided.

## Reassessment of the old 'near light speed' claim

The previous estimate set \(F\sim mrH^2=\sigma\) with \(\sigma\sim1\,\mathrm{GeV/fm}\), \(r=1\,\mathrm{fm}\), and \(m=m_p/3\), producing \(Hr/c\approx1.79\). Algebraically,

\[
\frac{Hr}{c}=\sqrt{\frac{\sigma r}{mc^2}}.
\]

This ratio being of order one follows from the chosen QCD energy scales; it does **not** demonstrate horizon formation between quarks, a causal cutoff, matter creation from phantom energy, or a cosmic bounce. Furthermore, an accurate tidal estimate uses \(H^2+\dot H\), and a confined relativistic quantum system cannot be adequately modeled with a constituent-quark Newtonian force balance. See `feasibility_check.ipynb` for a labeled dimensional illustration only.

## Reproducible exploratory notebooks

- [feasibility_check.ipynb](feasibility_check.ipynb): dimensional estimate, with explicit limitations; **not** a feasibility validation.
- [strong_force_rebirth.ipynb](strong_force_rebirth.ipynb): conservation-respecting FLRW *phenomenological* comparison \(Q=0\) vs illustrative \(Q=3\xi H\rho_X\). This is **not a QCD prediction** and does not demonstrate cosmic rebirth.

## Falsifiable research questions

1. Calculate QCD bound-state response to a specified time-dependent curved spacetime using an appropriate quantum-field treatment; does string breaking occur and at what rate?
2. Derive the microscopic source of energy for any produced pairs. Is there a coupling that makes \(Q>0\) for the phantom component?
3. Bound the homogeneous energy-transfer rate against phantom energy growth and dilution of existing hadrons.
4. Evolve \(\rho_X,\rho_m,H,a\) consistently and test singularity avoidance; separately establish any reheating, bounce, or new hot dense phase.
5. Check observational viability and stability of the proposed phantom/coupling sector.

## Sources

- Caldwell, Kamionkowski & Weinberg (2003), *Phantom Energy: Dark Energy with w < −1 Causes a Cosmic Doomsday*: https://doi.org/10.1103/PhysRevLett.91.071301
- DeTar et al. (1999), *String breaking in lattice quantum chromodynamics*: https://doi.org/10.1103/PhysRevD.59.031501
- Bulava et al. (2019), *String breaking by light and strange quarks in QCD*: https://arxiv.org/abs/1902.04006
- Curbelo et al. (2006), *Interacting Phantom Energy and Avoidance of the Big Rip Singularity*: https://arxiv.org/abs/astro-ph/0502141
- Zago & Kosowsky (2019), *Quantum particle production effects on the cosmic expansion*: https://doi.org/10.1103/PhysRevD.100.045023

These papers establish relevant *ingredients* or examples, not the full StrongForceRebirth hypothesis.

## Historical note

Earlier versions asserted that an \(Hr\) close to \(c\) validated the conjecture and used \(\dot H=\alpha(\rho_{vac}-\rho_0e^{\beta Ht})\) as though it followed from the Einstein equations. Both claims have been withdrawn. The original intuition remains a question worthy of a properly specified model.
