from flask import Flask, render_template, request
import numpy_financial as nf

app = Flask(__name__)

def calculate_metrics(rate, cashflows):
    npv = round(nf.npv(rate, cashflows), 2)
    irr = round(nf.irr(cashflows) * 100, 2)
    avg_profit = sum(cashflows[1:]) / (len(cashflows) - 1)
    arr = round((avg_profit / abs(cashflows[0])) * 100, 2)

    meaning = f"NPV = {npv}. This means the project {'adds' if npv > 0 else 'loses'} value overall. "
    meaning += f"IRR = {irr}%. A higher IRR is better. "
    meaning += f"ARR = {arr}%. This shows the average yearly return."

    # Smart recommendations
    if npv > 0 and irr > rate * 100:
        rec = "This project looks profitable. You can continue investing or expand it carefully."
    elif npv < 0:
        rec = "This project may not be profitable. Try reducing costs, shortening time, or choosing another project."
    else:
        rec = "This project’s return is moderate. Try optimizing investments or reviewing your cash flow plan."

    return {"npv": npv, "irr": irr, "arr": arr, "meaning": meaning, "recommendation": rec}


@app.route("/", methods=["GET", "POST"])
def index():
    resultA = resultB = None
    better_project = None

    if request.method == "POST":
        rate = float(request.form["rate"]) / 100

        cashflowsA = list(map(float, request.form.getlist("cashflowsA")))
        cashflowsB = list(map(float, request.form.getlist("cashflowsB")))

        resultA = calculate_metrics(rate, cashflowsA)
        resultB = calculate_metrics(rate, cashflowsB)

        # Comparison logic
        if resultA["npv"] > resultB["npv"]:
            better_project = "Project A seems more profitable based on NPV."
        elif resultB["npv"] > resultA["npv"]:
            better_project = "Project B seems more profitable based on NPV."
        else:
            better_project = "Both projects perform similarly."

    return render_template("index.html",
                           resultA=resultA,
                           resultB=resultB,
                           better_project=better_project)


if __name__ == "__main__":
    app.run(debug=True)
