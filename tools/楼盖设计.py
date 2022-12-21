import matplotlib.pyplot as plt

variable_load_k = 4.5  # 活荷载标准值

# 容重与自重
roof_covering_soil_bulk_density = 18  # kN/m³
roofing_surface = 0.52
reinforced_concrete_bulk_density = 25  # kN/m³
ceiling_self_weight = 0.2
psi_c, psi_q = 0.7, 0.5  # ψ \psi
gamma_G, gamma_Q = 1.3, 1.5

covering_soil_thickness, ceiling_thickness, ceiling_width = 0.3, 0.08, 2.1

column = 0.5  # 柱宽 m
grad_main, graid_minor, grad_ceiling = 6.300, 6.800, 2.100  # 轴网中梁的长度

l_0_main = grad_main  # 按弹性理论计算，主梁长度取支承中心线间距离
h_ceiling, h_main = ceiling_thickness, l_0_main / 12
b_ceiling, b_main = ceiling_width, h_main / 2.5
l_n_minor = graid_minor - b_main
l_0_minor = l_n_minor
h_minor = l_0_minor / 15
b_minor = h_minor / 2.5
l_0_minor_end = min(1.025 * l_n_minor, l_n_minor + b_main / 2)
l_n_ceiling = grad_ceiling - b_minor
l_0_ceiling = l_n_ceiling
l_0_ceiling_end = min(l_n_ceiling + h_ceiling / 2, l_n_ceiling + b_minor / 2)
print(
    f"板 h: {h_ceiling:.2f}m b: {b_ceiling:.2f}m; \n主梁 h: {h_main:.2f}m b: {b_main:.2f}m; \n次梁 h: {h_minor:.2f}m b: {b_minor:.2f}m"
)
s_n_minor = grad_ceiling - b_minor  # 次梁净距

c = 20
f_c, f_t, f_y_300, f_y_400 = 14.3, 1.43, 270, 360
d_ceiling = 10
d_minor = 20
d_main = 25
d_stirrup = 10
alpha_1, beta_1 = 1.0, 0.8
alpha_s_max = 0.384
xi_b = 0.518

# 2号主梁设计弯矩，请自行按弯矩包络图确定
M_designed_value_main_2 = 38.3


def alpha_ms_inquire():
    lst = [
        [
            -1 / 16,
            1 / 14,
            -1 / 11,
            1 / 16,
            -1 / 14,
            1 / 16,
            -1 / 14,
            1 / 16,
            -1 / 11,
            1 / 14,
            -1 / 16,
        ],
        [
            -1 / 24,
            1 / 14,
            -1 / 11,
            1 / 16,
            -1 / 14,
            1 / 16,
            -1 / 14,
            1 / 16,
            -1 / 11,
            1 / 14,
            -1 / 24,
        ],
    ]
    for alpha_ms in lst:
        yield alpha_ms


def etas_inquire():
    lst = [[2.7, 3.0, 2.7, 3.0, 2.7, 3.0, 2.7]]
    for etas in lst:
        yield etas


def alpha_vs_inquire():
    lst = [[0.5, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.55, 0.5]]
    for alpha_vs in lst:
        yield alpha_vs


def permanent_load_calculate(covering_soil_thickness, ceiling_thickness):
    return (
        roof_covering_soil_bulk_density * covering_soil_thickness
        + roofing_surface
        + reinforced_concrete_bulk_density * ceiling_thickness
        + ceiling_self_weight
    )


def load_calculate(permanent_load_k, variable_load_k):
    return permanent_load_k * gamma_G, variable_load_k * gamma_Q


def M_design_value_calculate(alpha_ms, g, q, l_0, l_0_e):
    M_design_values = []
    for i in range(len(alpha_ms)):
        if i in [0, 1, 2, len(alpha_ms) - 3, len(alpha_ms) - 2, len(alpha_ms) - 1]:
            M_design_values.append(alpha_ms[i] * (g + q) * l_0_e**2)
        else:
            M_design_values.append(alpha_ms[i] * (g + q) * l_0**2)
    return M_design_values


def Fn_designed_values_calculate(alpha_vs, g, q, l_0, l_0_e):
    Fn_design_values = []
    for i in range(len(alpha_vs)):
        if i in [0, 1, len(alpha_vs) - 2, len(alpha_vs) - 1]:
            Fn_design_values.append(alpha_vs[i] * (g + q) * l_0_e)
        else:
            Fn_design_values.append(alpha_vs[i] * (g + q) * l_0)
    return Fn_design_values


def ceiling_M_design_value_calculate(alpha_ms, g_k, q_k, l_0, l_0_e):
    g, q = load_calculate(g_k, q_k)
    print(f"板永久载荷设计值为 {g} kN/m²，板活载荷设计值为 {q} kN/m²")
    return M_design_value_calculate(alpha_ms, g, q, l_0, l_0_e)


def minor_M_design_value_calculate(alpha_ms, g_k, q_k, l_0, l_0_e):
    g_k = (
        g_k * grad_ceiling
        + reinforced_concrete_bulk_density * (h_minor - h_ceiling) * b_minor
    )
    print(f"次梁永久载荷为 {g_k:.2f} kN/m")
    q_k *= grad_ceiling * gamma_Q
    g, q = load_calculate(g_k, q_k)
    print(f"次梁永久载荷设计值为 {g:.2f} kN/m，次梁活载荷设计值为 {q} kN/m")
    return g, q, M_design_value_calculate(alpha_ms, g, q, l_0, l_0_e)


def minor_Fn_designed_values_calculate(alpha_vs, g, q, l_0, l_0_e):
    return Fn_designed_values_calculate(alpha_vs, g, q, l_0, l_0_e)


def main_M_design_value_calculate(alpha_ms, g_k, l_0, q_k=variable_load_k):
    ...


def is_alpha_s_illegal(alpha_ses):
    for alpha_s in alpha_ses:
        if alpha_s > alpha_s_max:
            print("-" * 10 + f"Warning: alpha_s大于alpha_s_max：{alpha_s_max}" + "-" * 10)
    print(f"alpha_s小于alpha_s_max：{alpha_s_max}")


def is_xi_illegal(xis):
    for xi in xis:
        if xi > xi_b:
            print("-" * 10 + f"Warning: xi大于xi_b：{xi_b}" + "-" * 10)
    print(f"xi小于xi_b：{xi_b}")


def alpha_ses_calculate(M_designed_values, h_0):
    return [m * 1e3 / (alpha_1 * f_c * b_ceiling * h_0**2) for m in M_designed_values]


def xis_calculate(alpha_ses):
    return [1 - (1 - alpha_s) ** 0.5 for alpha_s in alpha_ses]


def gamma_ses_calculate(alpha_ses):
    return [(1 + (1 - alpha_s) ** 0.5) / 2 for alpha_s in alpha_ses]


def A_ses_calculate(xis, h_0, f_y):
    return [1e3 * xi * b_ceiling * h_0 * alpha_1 * f_c / f_y for xi in xis]


def A_ses_calculate2(Ms, gamma_ses, h_0, f_y):
    return [1e6 * m / (gamma_s * f_y * h_0) for m, gamma_s in zip(Ms, gamma_ses)]


def ceiling_reinforcement(M_designed_values_ceiling):
    h_0 = h_ceiling * 1000 - c - d_ceiling / 2
    print(f"板 h_0为{h_0}mm")
    alpha_ses = alpha_ses_calculate(M_designed_values_ceiling, h_0)
    print(f"板 alpha_s支座-跨中依次为{[round(alpha_s, 3) for alpha_s in alpha_ses]}")
    is_alpha_s_illegal(alpha_ses)
    xis = xis_calculate(alpha_ses)
    print(f"板 xi支座-跨中依次为{[round(xi, 3) for xi in xis]}")
    is_xi_illegal(xis)
    A_ses = A_ses_calculate(xis, h_0, f_y_300)
    print(f"板 A_s支座-跨中依次为{[round(A_s, 3) for A_s in A_ses]}")


def b_f_calculate():
    return min(grad_ceiling, b_minor + s_n_minor, b_minor + 12 * h_ceiling)


def minor_reinforcement(M_designed_values_minor):
    h_0 = h_minor * 1000 - c - d_minor / 2 - d_stirrup
    print(f"次梁 一排纵筋h_0为{h_0:.0f}mm")
    alpha_ses = alpha_ses_calculate(M_designed_values_minor, h_0)
    print(f"次梁 alpha_s支座-跨中依次为{[round(alpha_s, 5) for alpha_s in alpha_ses]}")
    is_alpha_s_illegal(alpha_ses)
    xis = xis_calculate(alpha_ses)
    print(f"次梁 xi支座-跨中依次为{[round(xi, 5) for xi in xis]}")
    is_xi_illegal(xis)
    A_ses = A_ses_calculate(xis, h_0, f_y_400)
    print(f"次梁 A_s支座-跨中依次为{[round(A_s, 5) for A_s in A_ses]}mm²")
    print("-" * 10 + f"Warning: 次梁还未配箍筋" + "-" * 10)


def draw_bending_moment_envelope_diagram(*args):
    for Ms in args:
        x = map(lambda x: x * l_0_main / 3, range(7))
        x, Ms = list(x), list(Ms)
        plt.plot(x, Ms)
        t = 0
        for i, j in zip(x, Ms):
            plt.annotate(
                f"{j:.2f}",  # 标注的文本
                xy=(i, j),  # 标注的位置
                xytext=(i - 0.5, j + 8),  # 文本的位置
            )

    for i in range(7):
        x = i * l_0_main / 3
        plt.axvline(x=x, linestyle='dotted', color='#87CEEB')
        plt.annotate(
            f"{x:.2f}",  # 标注的文本
            xy=(x, 0),  # 标注的位置
            xytext=(x, 8),  # 文本的位置
        )

    plt.axhline(y=0, color='k')
    plt.gca().invert_yaxis()
    plt.savefig("bending_moment_envelope_diagram.png")


def main_reinforcement(etas, g, q):
    g = (
        g * gamma_G * max(etas)
        + (h_main - h_ceiling)
        * b_main
        * l_0_main
        / 3
        * reinforced_concrete_bulk_density
        * gamma_G
    )
    q = q * gamma_Q * max(etas)
    print(f"主梁永久载荷设计值为 {g:.2f} kN/m²，主梁活载荷设计值为 {q:.2f} kN/m²")
    M_1_max = 0.244 * g * l_0_main + 0.289 * g * l_0_main
    M_B_max = -0.267 * g * l_0_main - 0.311 * g * l_0_main
    M_2_max = -0.067 * g * l_0_main - 0.2 * g * l_0_main
    V_A_max = 0.733 * g + 0.866 * q
    V_Bl_max = -1.267 * g - 1.311 * q
    V_Br_max = 1 * g + 1.222 * q
    print("M_1_max\tM_B_max\tM_2_max\tV_A_max\tV_Bl_max\tV_Br_max")
    print(
        f"{M_1_max:7.2f}\t{M_B_max:7.2f}\t{M_2_max:7.2f}\t{V_A_max:7.2f}\t{V_Bl_max:8.2f}\t{V_Br_max:8.2f}"
    )
    # 1,3 Q
    M_b = -0.267 * g * l_0_main - 0.133 * q * l_0_main
    M_1l = (g + q) * l_0_main / 3 + M_b / 3
    M_1r = (g + q) * l_0_main / 3 + M_b * 2 / 3
    M_2l = M_b + g * l_0_main / 3
    Ms1 = (0, M_1l, M_1r, M_b, M_2l, M_2l, M_b)
    print("1,3活荷载:")
    print("M_1l\tM_1r\tM_b\tM_2l")
    print(f"{M_1l:8.2f}{M_1r:8.2f}{M_b:8.2f}{M_2l:8.2f}")
    # 1,2 Q
    M_b = -0.267 * g * l_0_main - 0.311 * q * l_0_main
    M_1l = (g + q) * l_0_main / 3 + M_b / 3
    M_1r = (g + q) * l_0_main / 3 + M_b * 2 / 3
    M_c = -0.267 * g * l_0_main - 0.089 * q * l_0_main
    M_2l = (g + q) * l_0_main / 3 + M_c + (M_b - M_c) * 2 / 3
    M_2r = (g + q) * l_0_main / 3 + M_c + (M_b - M_c) / 3
    Ms2 = (0, M_1l, M_1r, M_b, M_2l, M_2r, M_c)
    print("1,2活荷载:")
    print("M_1l\tM_1r\tM_b\tM_2l\tM_2r\tM_c")
    print(f"{M_1l:8.2f}{M_1r:8.2f}{M_b:8.2f}{M_2l:8.2f}{M_2r:8.2f}{M_c:8.2f}")
    # 2 Q
    M_b = -0.267 * g * l_0_main - 0.133 * q * l_0_main
    M_c = -0.267 * g * l_0_main - 0.133 * q * l_0_main
    M_2l = (g + q) * l_0_main / 3 + M_b
    M_2r = (g + q) * l_0_main / 3 + M_b
    M_1l = g * l_0_main / 3 + M_b / 3
    M_1r = g * l_0_main / 3 + M_b * 2 / 3
    Ms3 = (0, M_1l, M_1r, M_b, M_2l, M_2r, M_c)
    print("2活荷载:")
    print("M_1l\tM_1r\tM_b\tM_2l\tM_2r\tM_c")
    print(f"{M_1l:8.2f}{M_1r:8.2f}{M_b:8.2f}{M_2l:8.2f}{M_2r:8.2f}{M_c:8.2f}")
    draw_bending_moment_envelope_diagram(Ms1, Ms2, Ms3)

    h_0 = h_main * 1000 - c - d_ceiling - d_minor - d_main / 2
    print(f"次梁 一排纵筋h_0为{h_0:.0f}mm")
    M_designed_values_main = [
        M_1_max,
        -M_B_max + (V_A_max + V_Bl_max) * column / 2,
        -M_2_max,
        M_designed_value_main_2,
    ]
    alpha_ses = alpha_ses_calculate(M_designed_values_main, h_0)
    print(f"主梁 alpha_s支座-跨中依次为{[round(alpha_s, 5) for alpha_s in alpha_ses]}")
    is_alpha_s_illegal(alpha_ses)
    gamma_ses = gamma_ses_calculate(alpha_ses)
    print(f"主梁 gamma_ses支座-跨中依次为{[round(gamma_s, 5) for gamma_s in gamma_ses]}")
    A_ses = A_ses_calculate2(M_designed_values_main, gamma_ses, h_0, f_y_400)
    print(f"主梁 A_s支座-跨中依次为{[round(A_s, 5) for A_s in A_ses]}mm²")
    print("-" * 10 + f"Warning: 主梁还未配箍筋" + "-" * 10)


if __name__ == "__main__":
    permanent_load_ceiling = permanent_load_calculate(
        covering_soil_thickness, ceiling_thickness
    )
    print(f"板永久载荷为 {permanent_load_ceiling} kN/m²")
    print(f"板活载荷为 {variable_load_k} kN/m²")
    alpha_ms_gen = alpha_ms_inquire()
    alpha_ms = next(alpha_ms_gen)
    M_designed_values_ceiling = ceiling_M_design_value_calculate(
        alpha_ms, permanent_load_ceiling, variable_load_k, l_0_ceiling, l_0_ceiling_end
    )
    print(f"板弯矩设计值支座-跨中依次为{[round(M, 2) for M in M_designed_values_ceiling]}kN·m")
    ceiling_reinforcement(M_designed_values_ceiling)

    alpha_ms = next(alpha_ms_gen)
    g, q, M_designed_values_minor = minor_M_design_value_calculate(
        alpha_ms, permanent_load_ceiling, variable_load_k, l_0_minor, l_0_minor_end
    )
    print(f"次梁弯矩设计值支座-跨中依次为{[round(M, 2) for M in M_designed_values_minor]}kN·m")
    alpha_vs_gen = alpha_vs_inquire()
    alpha_vs = next(alpha_vs_gen)
    Fn_designed_values_minor = minor_Fn_designed_values_calculate(
        alpha_vs, g, q, l_0_minor, l_0_minor_end
    )
    print(f"次梁剪力设计值支座-跨中依次为{[round(Fn, 2) for Fn in Fn_designed_values_minor]}kN")
    b_f = b_f_calculate()
    print(f"次梁翼缘宽度为{b_f:.3f}m")
    minor_reinforcement(M_designed_values_minor)

    etas_gen = etas_inquire()
    etas = next(etas_gen)
    main_reinforcement(etas, g, q)
