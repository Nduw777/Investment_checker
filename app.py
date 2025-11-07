from flask import Flask, render_template, request
import numpy_financial as nf

app = Flask(__name__)

def calculate_metrics(rate, cashflows):
    npv = round(nf.npv(rate, cashflows), 2)
    irr = round(nf.irr(cashflows) * 100, 2)
    avg_profit = sum(cashflows[1:]) / (len(cashflows) - 1)
    arr = round((avg_profit / abs(cashflows[0])) * 100, 2)

    # Combine results with easy meanings
    meanings = [
        f"NPV = {npv}. This means the project {'adds value (good)' if npv > 0 else 'loses value (bad)'}.",
        f"IRR = {irr}%. This shows the rate of return. A higher value means better profitability.",
        f"ARR = {arr}%. This tells the average yearly return based on accounting profit."
    ]

    # Smart recommendations based on results
    if npv > 0 and irr > rate * 100:
        rec = "Your project looks profitable! You can go ahead or even expand it carefully."
    elif npv < 0:
        rec = "Your project may lose money. Try reducing costs, shortening the project time, or investing in another option."
    else:
        rec = "Your project has medium performance. Try optimizing your plan or reviewing your cashflows."

    return meanings, rec


@app.route("/", methods=["GET", "POST"])
def index():
    meanings = []
    recommendation = ""
    if request.method == "POST":
        try:
            rate = float(request.form["rate"]) / 100
            cashflows = list(map(float, request.form["cashflows"].split(",")))
            meanings, recommendation = calculate_metrics(rate, cashflows)
        except Exception as e:
            recommendation = f"Error: {e}"
    return render_template("index.html", meanings=meanings, recommendation=recommendation)


if __name__ == "__main__":
    app.run(debug=True)
