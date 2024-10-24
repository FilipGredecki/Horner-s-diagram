from sympy import symbols, sympify
import numpy as np
import plotly.graph_objs as go
# x^5 - 3x^4 -23x^3 + 51x^2 + 94x - 120


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
    
def create_polynominal(coefs):
    """
    returns a polynomial formula
    """

    str_expresion = ''
    for n in range(len(coefs)):
        str_expresion += f'{str(coefs[n])}*x**{len(coefs)-n-1}'
        if n+1 < len(coefs):
            str_expresion += '+'
    poly = sympify(str_expresion)
    return poly

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
        x = symbols('x')
        result = int(poly.subs(x, ratio))
        
        if result == 0:
            sqrt_set.add(ratio)
    return sqrt_set

def horner(coefs, sqrt):
    """
    performs the horner diagram
    """
    new_coef = [coefs[0]]
    for i in range(len(coefs)-1):
        nw = new_coef[i] * sqrt + coefs[i+1]
        new_coef.append(nw)
    if new_coef[-1] == 0:
        new_coef.pop()
    return new_coef

def convert_list_into_product(poly_fac):
    """
    converts arrays to product
    """
    product = ''
    for i in range(len(poly_fac)-1):
        product += str(poly_fac[i]) + '*'
    product += f'({str(create_polynominal(poly_fac[-1]))})'
    return product

def f_x(x_values, poly):
    """
    Calculates polynomial values for given x values
    """
    x = symbols('x')
    return [float(poly.subs(x, val)) for val in x_values]

def main():
    coefs = load_coefficients()
    poly = create_polynominal(coefs)
    p_set, q_set = find_p_q(coefs)
    sqrt_set = find_sqrt(poly, p_set, q_set)
    
    poly_fac = []
    for sqrt in sqrt_set:
        poly_fac.append(f'(x+({sqrt*-1}))')
        coefs =horner(coefs,sqrt)
    poly_fac.append(coefs)

    copleted_product = convert_list_into_product(poly_fac)
    copleted_product = copleted_product.replace('+(-','-').replace('+(', '+'). replace('))', ')')

    
    print(f'wielomian{poly} ma miejsca zerowe w punktach: {sqrt_set}')
    print(f'wielomian po podzieleniu przez pierwiastki: {copleted_product}')


    if len(sqrt_set) == 1:
        x_values = np.linspace(int(min(sqrt_set))-10, int(max(sqrt_set)+10), 200)
        y_values = f_x(x_values, poly)
    elif len(sqrt_set) > 1:
        x_values = np.linspace(int(min(sqrt_set))-10, int(max(sqrt_set)+10), int(10*(max(sqrt_set)+10-(min(sqrt_set)-10+10))))
        y_values = f_x(x_values, poly)
    else:
        x_values = np.linspace(-10, 10, 100)
        y_values = f_x(x_values, poly)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values,
        mode='lines',
        name='function graph'))
    if sqrt_set:
        fig.add_trace(go.Scatter(
            x=list(sqrt_set), 
            
            y=[0] * len(sqrt_set),  
            mode='markers',
            marker=dict(size=10, color='red'),
            name='zero place'))
    fig.update_layout(
        title=f"f(x)={poly}",
        xaxis_title="x",
        yaxis_title="f(x)")
    fig.show()

if __name__ == "__main__":
    main()
