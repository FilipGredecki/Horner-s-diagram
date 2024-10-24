import sympy as sp
import numpy as np
import plotly.graph_objs as go

#x^4-4x^3-2x^2+12x+9
# x3-6x2+9x
# x4-4x4+4x2

def load_coefficients():
    """ 
    returns arrays of coefficients
    """
    coefs = []
    n = 0
    print('to exit press x')
    while True:
        
        coef = input(f'give the coefficient at  x^{n}: ')
        try:
            coef = int(coef)
        except ValueError:
            if coef == 'x':
                break
            print('enter the correct number')
            continue
        coefs.insert(0,coef)
        n += 1
    return coefs

def create_polynominal(coefs: list):
    """
    returns a polynomial formula
    """
    str_expresion = ''
    for n in range(len(coefs)):
        str_expresion += f'{str(coefs[n])}*x**{len(coefs)-n-1}'
        if n+1 < len(coefs):
            str_expresion += '+'
    poly = sp.sympify(str_expresion)
    return poly

def create_deri_coefs(coefs):
    """
    create derivative coefficients
    """
    deri_coefs = []
    for n in range(len(coefs)):
        deri_coef = coefs[n]*(len(coefs)-n-1)
        if n + 1 < len(coefs):
            deri_coefs.append(deri_coef)
    return deri_coefs

def find_p_q(coefs):
    """
    looks for divisors of the intercept and the coefficient with the highest power
    """
    if abs(coefs[-1]) == 0:
        n = 2
        while True:
            if abs(coefs[-n]) != 0:
                p = abs(coefs[-n])
                p_set = set()
                p_set.add(0)
                break
            else:
                n += 1
    else:
        p = abs(coefs[-1])
        p_set = set()
    q = abs(coefs[0])
    
    
    for i in range(1,p+1):
        if p % i == 0:
            p_set.add(i)
            p_set.add(-i)
    
    q_set = set()
    for i in range(1,q+1):
        if q % i == 0:
            q_set.add(i)
            q_set.add(-i)
    
    return p_set, q_set

def sort_set(sqrt_set):
    sqrt_sorted_tab = sorted(sqrt_set)  # Zamienia zbiór na listę i sortuje
    return sqrt_sorted_tab

def find_sqrt(poly, p_set, q_set):
    """
    looks for the root of a polynomial
    """
    ratio_set = set()
    for p in p_set:
        for q in q_set:
            ratio_set.add(p/q)
    sqrt_set = set()
    for ratio in ratio_set:
        x = sp.symbols('x')
        result = poly.subs(x, ratio)
        if int(result) == 0 :
            sqrt_set.add(ratio)
    sqrt_sorted_tab = sort_set(sqrt_set)
    return sqrt_sorted_tab

def ff(deri_poly, number):
    x = sp.symbols('x')
    result = deri_poly.subs(x, number)
    if result > 0:
        return '+'
    else:
        return '-'

def calculate_the_monotonicity_of_the_function(sqrt_tab_with_zeros, deri_poly): # s_t_w_z = sqrt_tab_with_zeros
    tab = sqrt_tab_with_zeros
    if len(sqrt_tab_with_zeros) >= 2:
        for i in range(0, len(sqrt_tab_with_zeros)-1, 2):
            
            number = ((tab[i]+tab[i+2])/2)
            sign = ff(deri_poly, number)
            tab[i+1] = sign
        number = tab[0] -1 
        sign =  ff(deri_poly, number)
        tab.insert(0,sign)

        number = tab[-1] + 1 
        sign =  ff(deri_poly, number)
        tab.append(sign)
    elif len(sqrt_tab_with_zeros) == 1:
        number = tab[0] -1 
        sign =  ff(deri_poly, number)
        tab.insert(0,sign)

        number = tab[-1] + 1 
        sign =  ff(deri_poly, number)
        tab.append(sign)

    return tab

def table_with_local_min_and_max(tab):
    min_tab = []
    max_tab = []
    for i in range(len(tab)-2):
        if tab[i] == '+' and tab[i+2] == '-':
            max_tab.append(tab[i+1])
        elif tab[i] == '-' and tab[i+2] == '+':
            min_tab.append(tab[i+1])
    return min_tab, max_tab

def find_max(max_tab, poly):
    x = sp.symbols('x')
    result = poly.subs(x, max_tab[0])
    results = result
    max_sq = max_tab[0]
    for sqrt in max_tab:
        x = sp.symbols('x')
        result = poly.subs(x, sqrt)
        if result > results:
            max_sq = sqrt
    return max_sq

def find_min(min_tab, poly):
    x = sp.symbols('x')
    result = poly.subs(x, min_tab[0])
    results = result
    min_sq = min_tab[0]
    for sqrt in min_tab:
        x = sp.symbols('x')
        result = poly.subs(x, sqrt)
        if result < results:
            min_sq = sqrt
    return min_sq

def f_x(x_values, poly):
    """
    Calculates polynomial values for given x values
    """
    x = sp.symbols('x')
    return [float(poly.subs(x, val)) for val in x_values]

def main():
    coefs = load_coefficients()
    poly = create_polynominal(coefs)
    p_set, q_set = find_p_q(coefs)
    sqrt_sorted_tab = find_sqrt(poly, p_set, q_set)
    deri_coefs = create_deri_coefs(coefs)
    deri_poly = create_polynominal(deri_coefs)
    deri_p_set , deri_q_set = find_p_q(deri_coefs)
    deri_sqrt_sorted_tab = find_sqrt(deri_poly, deri_p_set, deri_q_set)
    sqrt_tab_with_zeros = []
    for sqrt in deri_sqrt_sorted_tab:
        sqrt_tab_with_zeros.append(sqrt)
        if sqrt != deri_sqrt_sorted_tab[-1]:
            sqrt_tab_with_zeros.append(0)
    tab = calculate_the_monotonicity_of_the_function(sqrt_tab_with_zeros, deri_poly)
    min_tab, max_tab = table_with_local_min_and_max(tab)
    
    max_switch = False
    if len(max_tab) >= 1: 
        max_sq = find_max(max_tab, poly)
        max_switch = True

    min_switch = False
    if len(min_tab) >= 1:
        min_sq = find_min(min_tab, poly)
        min_switch = True
    
    print(f'funkcja: {poly} z pochodną równą: {deri_poly}')
    if len(deri_sqrt_sorted_tab) >= 1:
        print(f'ma pierwiastki w punktach: {deri_sqrt_sorted_tab}')
    else:
        print('nie ma pierwiastków')

    if max_switch:
        print(f'funkcja ma maximum lokalne w punkcie: {max_sq}')
    
    if min_switch:
        print(f'funkcja ma minimum lokalne w punkcie: {min_sq}')
    print(f'kiedy funkcja jest malejąca i rosnąca: {tab}')
    print(sqrt_sorted_tab)

    if len(deri_sqrt_sorted_tab) == 1:
        x_values = np.linspace(int(min(deri_sqrt_sorted_tab)) - 10, int(max(deri_sqrt_sorted_tab) + 10), 200)
        y_values = f_x(x_values, deri_poly)
    elif len(deri_sqrt_sorted_tab) > 1:
        x_values = np.linspace(int(min(deri_sqrt_sorted_tab)) - 10, int(max(deri_sqrt_sorted_tab) + 10), 
        int(10 * (max(deri_sqrt_sorted_tab) + 10 - (min(deri_sqrt_sorted_tab) - 10 + 10))))
        y_values = f_x(x_values, deri_poly)
    else:
        x_values = np.linspace(-10, 10, 100)
        y_values = f_x(x_values, deri_poly)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        line=dict(color='pink'),
        name='deriative'
    ))

    if deri_sqrt_sorted_tab:
        fig.add_trace(go.Scatter(
            x=list(deri_sqrt_sorted_tab), 
            y=[0] * len(deri_sqrt_sorted_tab),
            mode='markers',
            marker=dict(size=15, color='red'),
            name='zero places of derivative'
        ))

    d_x_values = x_values
    d_y_values = f_x(d_x_values, poly)

    fig.add_trace(go.Scatter(
        x=d_x_values,
        y=d_y_values,
        mode='lines',
        line=dict(color='blue'),
        name='polynominal'
    ))

    if sqrt_sorted_tab:
        fig.add_trace(go.Scatter(
            x=list(sqrt_sorted_tab),
            y=[0] * len(sqrt_sorted_tab),
            mode='markers',
            marker=dict(size=10, color='purple'),
            name='zero places of polynomial'
        ))

    fig.update_layout(
        title=f"polynomial f(x)={poly}<br>derivative f'(x)={deri_poly}",
        xaxis_title="x",
        yaxis_title="f(x)"
    )

    fig.show()

main()
