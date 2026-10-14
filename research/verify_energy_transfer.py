"""Reproducible controls, NOT a real-time QCD or semiclassical backreaction solver.

Python 3 standard library only. Run from repository root:
    python3 research/verify_energy_transfer.py
Writes research/calculation_results.json; all units in the controls are dimensionless.
"""
import cmath
import json
import math
from pathlib import Path
import platform


def rk4_step(f, t, y, h):
    k1 = f(t, y)
    k2 = f(t + h / 2, [a + h * b / 2 for a, b in zip(y, k1)])
    k3 = f(t + h / 2, [a + h * b / 2 for a, b in zip(y, k2)])
    k4 = f(t + h, [a + h * b for a, b in zip(y, k3)])
    return [a + h * (b + 2*c + 2*d + e) / 6
            for a, b, c, d, e in zip(y, k1, k2, k3, k4)]


def exact_fluid(n, xi, wr=0.0, delta=0.1, x0=0.9, b0=0.1):
    s = 3 * (delta - xi)
    d = 1 + wr + delta - xi
    x = x0 * math.exp(s * n)
    # Parameter range in this experiment has d > 0.
    b = b0 * math.exp(-3 * (1 + wr) * n) + xi * x0 / d * (
        math.exp(s * n) - math.exp(-3 * (1 + wr) * n))
    return x, b


def simpson(f, end, steps=40000):
    h = end / steps
    return h / 3 * (f(0) + f(end) + sum(
        (4 if j % 2 else 2) * f(j*h) for j in range(1, steps)))


def fluid_controls():
    rows = []
    for wr in (0.0, 1/3):
        for xi in (0.0, 0.05, 0.1, 0.15, 0.9):
            def rhs(n, y):
                x, b = y
                return [3*(0.1-xi)*x, -3*(1+wr)*b + 3*xi*x]
            errors = []
            conservation = []
            for h in (0.01, 0.005):
                y = [0.9, 0.1]
                worst = 0.0
                for j in range(round(20/h)):
                    n = j*h
                    y = rk4_step(rhs, n, y, h)
                    exact = exact_fluid((j+1)*h, xi, wr)
                    worst = max(worst, *(abs(a-b)/max(abs(b), 1e-100)
                                         for a, b in zip(y, exact)))
                    dx, db = rhs(n+h, y)
                    residual = dx + db + 3*(-0.1*y[0] + (1+wr)*y[1])
                    conservation.append(abs(residual)/max(sum(y), 1e-100))
                errors.append(worst)
            assert errors[-1] < 1e-6
            assert max(conservation) < 1e-13
            x, b = exact_fluid(20, xi, wr)
            H = math.sqrt(x+b)
            Hdot = -1.5*(-0.1*x + (1+wr)*b)
            row = dict(w_receiver=wr, xi=xi, max_relative_error_h_001=errors[0],
                       max_relative_error_h_0005=errors[1],
                       max_relative_continuity_residual=max(conservation),
                       H_at_N20=H, Hdot_at_N20=Hdot,
                       acceleration_over_a_at_N20=H*H+Hdot,
                       asymptotic_w_eff=-1.1+xi,
                       big_rip_in_this_ansatz=xi < 0.1)
            if xi < 0.1:
                # t = integral dN/H; omitted tail beyond N=200 is analytic asymptotically.
                d = 1+wr+0.1-xi
                s = 3*(0.1-xi)
                tail = 2*math.exp(-s*200/2)/(s*math.sqrt(0.9*(1+xi/d)))
                integrand = lambda n: 1/math.sqrt(sum(exact_fluid(n, xi, wr)))
                integral = simpson(integrand, 200)
                coarse_integral = simpson(integrand, 200, steps=20000)
                row['time_quadrature_step_halving_difference'] = abs(integral-coarse_integral)
                assert abs(integral-coarse_integral) < 1e-8
                row['finite_time_limit_H0_units'] = integral + tail
            rows.append(row)
    # Transfer only for N in [2,4]; it is insufficient if constant-w phantom survives.
    x, b = exact_fluid(2, 0)
    x4, b4 = exact_fluid(2, 0.3, x0=x, b0=b)
    pulse = dict(description='xi=0.3 for 2<=N<=4; otherwise xi=0; dust',
                 rho_X_at_N4=x4, rho_m_at_N4=b4,
                 rho_X_at_N20=x4*math.exp(0.3*16),
                 rho_m_at_N20=b4*math.exp(-3*16),
                 big_rip_returns=True)
    return rows, pulse


def particle_control(tau, mass=1.0, k=1.0, step=0.002, extent=16):
    # Conformally coupled free scalar: u''+[k^2+m^2 a^2]u=0,
    # a^2=2+tanh(eta/tau). Static in/out regions give unambiguous beta.
    wi, wo = math.sqrt(k*k+mass*mass), math.sqrt(k*k+3*mass*mass)
    start, end = -extent*tau, extent*tau
    count = math.ceil((end-start)/step)
    h = (end-start)/count
    u = cmath.exp(-1j*wi*start)/math.sqrt(2*wi)
    y = [u, -1j*wi*u]
    def rhs(eta, state):
        u, v = state
        freq2 = k*k + mass*mass*(2+math.tanh(eta/tau))
        return [v, -freq2*u]
    for j in range(count):
        y = rk4_step(rhs, start+j*h, y, h)
    u, v = y
    beta2 = abs(math.sqrt(wo/2)*(u-1j*v/wo))**2
    alpha2 = abs(math.sqrt(wo/2)*(u+1j*v/wo))**2
    exact = math.sinh(math.pi*tau*(wo-wi)/2)**2 / (
        math.sinh(math.pi*tau*wi)*math.sinh(math.pi*tau*wo))
    return beta2, exact, abs(alpha2-beta2-1)


def gauge_kinetic_sign_controls():
    # Classical Abelian/commuting-color field on a prescribed background.
    # Not a particle-production calculation; verifies signs in Q=dot(B)<F^2>/4.
    H, rate, t = 0.2, 0.3, 1.0
    rows = []
    for electric in (True, False):
        sign = -1 if electric else 1
        def rho(t):
            return 0.5*math.exp((sign*rate-4*H)*t)
        energy = rho(t)
        eps = 1e-5
        derivative = (rho(t+eps)-rho(t-eps))/(2*eps)
        Q_ward = sign*rate*energy
        Q_from_continuity = derivative+4*H*energy
        assert abs(Q_ward-Q_from_continuity) < 1e-10
        rows.append(dict(field='electric' if electric else 'magnetic',
                         H=H, dlnB_dt=rate, rho=energy,
                         Q_ward=Q_ward, Q_from_continuity=Q_from_continuity,
                         interpretation='classical work, not irreversible particle production'))
    return rows


def main():
    rows, pulse = fluid_controls()
    modes = []
    for tau in (0.5, 1.0, 2.0):
        coarse, exact, _ = particle_control(tau)
        fine, _, norm = particle_control(tau, step=0.001)
        farther, _, _ = particle_control(tau, step=0.001, extent=20)
        assert abs(fine-exact)/exact < 1e-6
        assert norm < 1e-8
        assert abs(fine-farther)/exact < 1e-6
        modes.append(dict(tau=tau, numerical_beta2=fine, analytic_beta2=exact,
                          relative_error=abs(fine-exact)/exact,
                          step_halving_difference=abs(coarse-fine),
                          endpoint_extension_difference=abs(fine-farther),
                          normalization_error=norm, no_direct_X_coupling=True))
    massless, _, norm = particle_control(1.0, mass=0.0)
    assert massless < 1e-20 and norm < 1e-8
    # Illustrative scales, not measured dark energy parameters or QCD yield bounds.
    hbar_gev_s, mpl_gev, lam_gev = 6.582119569e-25, 2.435e18, 0.2
    H0_s = 70*1000/3.085677581491367e22  # illustrative km/s/Mpc
    h0_gev = H0_s*hbar_gev_s
    scales = dict(H0_assumed_km_s_Mpc=70, Lambda_QCD_assumed_GeV=lam_gev,
                  H0_over_QCD=h0_gev/lam_gev,
                  H_QCD_in_s_inverse=lam_gev/hbar_gev_s,
                  rho_background_GeV4_at_H_QCD=3*mpl_gev**2*lam_gev**2,
                  Lambda4_over_background=lam_gev**2/(3*mpl_gev**2),
                  free_field_H4_over_background=lam_gev**2/(3*mpl_gev**2),
                  phantom_dominated_remaining_seconds_delta_01=2*hbar_gev_s/(3*0.1*lam_gev))
    result = dict(python=platform.python_version(), fluid=rows, finite_pulse=pulse,
                  free_scalar_modes=modes, massless_conformal_beta2=massless, scales=scales,
                  gauge_kinetic_sign_controls=gauge_kinetic_sign_controls(),
                  scope='Controls only: no QCD rate, renormalized stress tensor, or viable phantom EFT derived.')
    dest = Path(__file__).with_name('calculation_results.json')
    dest.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
