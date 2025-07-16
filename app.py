from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/linear", methods=["GET", "POST"])
def linear():
    result = ""
    if request.method == "POST":
        equation = request.form["equation"]
        result = solve_linear(equation)
    return render_template("linear.html", result=result)

@app.route("/inequality", methods=["GET", "POST"])
def inequality():
    result = ""
    if request.method == "POST":
        equation = request.form["equation"]
        result = solve_inequality(equation)
    return render_template("inequality.html", result=result)

@app.route("/simultaneous", methods=["GET", "POST"])
def simultaneous():
    result = ""
    if request.method == "POST":
        eq1 = request.form["eq1"]
        eq2 = request.form["eq2"]
        result = solve_simultaneous(eq1, eq2)
    return render_template("simultaneous.html", result=result)

@app.route("/quadratic", methods=["GET", "POST"])
def quadratic():
    result = ""
    if request.method == "POST":
        equation = request.form["equation"]
        result = solve_quadratic(equation)
    return render_template("quadratic.html", result=result)


def solve_linear(equation):
    try:
        lst = equation.replace(" ", "").replace("-", "+-").split("=")
        if len(lst) != 2:
            return "일차방정식이 아닙니다."
        left, right = lst

        def parse(expr):
            terms = expr.replace("-", "+-").split("+")
            x_coef = 0
            const = 0
            for term in terms:
                if not term:
                    continue
                if 'x' in term:
                    val = term.replace('x', '')
                    if val == '' or val == '+': val = 1
                    elif val == '-': val = -1
                    else: val = int(val)
                    x_coef += val
                else:
                    const += int(term)
            return x_coef, const

        lx, lc = parse(left)
        rx, rc = parse(right)

        x_total = lx - rx
        c_total = rc - lc

        if x_total == 0:
            return "모든 실수가 해입니다." if c_total == 0 else "해가 없습니다."
        else:
            return f"x = {round(c_total / x_total, 2)}"
    except:
        return "입력 오류. 예: 2x+3=7"


def solve_inequality(equation):
    try:
        for op in ['<=', '>=', '<', '>']:
            if op in equation:
                left, right = equation.split(op)
                ine = op
                break
        else:
            return "부등식이 아닙니다."

        def parse(expr):
            terms = expr.replace("-", "+-").replace(" ", "").split("+")
            x_coef = 0
            const = 0
            for term in terms:
                if not term: continue
                if 'x' in term:
                    val = term.replace('x', '')
                    if val == '' or val == '+': val = 1
                    elif val == '-': val = -1
                    else: val = int(val)
                    x_coef += val
                else:
                    const += int(term)
            return x_coef, const

        lx, lc = parse(left)
        rx, rc = parse(right)

        x_total = lx - rx
        c_total = rc - lc

        if x_total == 0:
            return "항등식이거나 해가 없습니다."

        result = round(c_total / x_total, 2)
        if x_total < 0:
            if ine == '<': ine = '>'
            elif ine == '>': ine = '<'
            elif ine == '<=': ine = '>='
            elif ine == '>=': ine = '<='

        return f"x {ine} {result}"
    except:
        return "입력 오류. 예: 2x + 3 <= 7"


def solve_simultaneous(eq1, eq2):
    try:
        def parse(eq):
            left, right = eq.replace("-", "+-").replace(" ", "").split("=")
            terms = left.split("+")
            a = b = 0
            for term in terms:
                if 'x' in term:
                    val = term.replace('x', '')
                    a += int(val or '1')
                elif 'y' in term:
                    val = term.replace('y', '')
                    b += int(val or '1')
            c = int(right)
            return a, b, c

        a1, b1, c1 = parse(eq1)
        a2, b2, c2 = parse(eq2)

        D = a1 * b2 - a2 * b1
        if D == 0:
            return "해가 없거나 무수히 많음"

        Dx = c1 * b2 - c2 * b1
        Dy = a1 * c2 - a2 * c1
        x = round(Dx / D, 2)
        y = round(Dy / D, 2)
        return f"x = {x}, y = {y}"
    except:
        return "입력 오류. 예: 2x+3y=7"


def solve_quadratic(equation):
    try:
        left, right = equation.replace(" ", "").split("=")
        right = f"-({right})"
        full = f"{left}+{right}"
        full = full.replace("-", "+-")
        terms = full.split("+")
        a = b = c = 0
        for term in terms:
            if 'x^2' in term:
                val = term.replace('x^2', '')
                a += int(val or '1')
            elif 'x' in term:
                val = term.replace('x', '')
                b += int(val or '1')
            elif term:
                c += int(term)

        D = b ** 2 - 4 * a * c
        if D < 0:
            return "허근 (실수 해 없음)"
        elif D == 0:
            x = -b / (2 * a)
            return f"중근: x = {round(x, 2)}"
        else:
            sqrt_D = D ** 0.5
            x1 = (-b + sqrt_D) / (2 * a)
            x2 = (-b - sqrt_D) / (2 * a)
            return f"x = {round(x1, 2)}, x = {round(x2, 2)}"
    except:
        return "입력 오류. 예: x^2+3x+2=0"

if __name__ == "__main__":
    app.run(debug=True)