from flask import Flask, render_template, request
import numpy as np
import numpy_financial as nf

app = Flask(__name__)

# Calculate NPV
def calculate_npv(rate, cashflows):
    return nf.npv(rate, cashflows)

# Calculate IRR
def calculate_irr(cashflows):
    return nf.irr(cashflows)

# Calculate ARR
def calculate_arr(initial_cost, cashflows):
    avg_profit = (sum(cashflows[1:]) - abs(initial_cost)) / len(cashflows[1:])
    avg_investment = abs(initial_cost) / 2
    return avg_profit / avg_investment

# Generate dynamic recommendations
def generate_dynamic_recommendations(initial_cost, cashflows, rate, npv, irr, arr, years):
    recommendations = []

    # Rule 1: NPV
    if npv <= 0:
        shortfall = abs(npv)
        recommendations.append(f"Increase total cash inflows by at least {round(shortfall,2)} or reduce initial cost by the same amount to make NPV positive.")

    # Rule 2: IRR
    if irr <= rate:
        required_irr_increase = rate - irr + 0.01  # small buffer
        recommendations.append(f"Consider increasing yearly cash inflows or shortening the project duration to increase IRR by at least {round(required_irr_increase*100,2)}%.")

    # Rule 3: ARR
    if arr <= rate:
        required_arr_increase = rate - arr + 0.01
        increase_amount = round(required_arr_increase * (initial_cost/2),2)
        recommendations.append(f"Increase average yearly profit by {increase_amount} or reduce initial investment to achieve ARR above your target.")

    # If project is good
    if not recommendations:
        recommendations.append("Project looks profitable. Stick with your plan!")

    return recommendations

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    if request.method == "POST":
        initial_cost = float(request.form["initial_cost"])
        cashflows = list(map(float, request.form["cashflows"].split(",")))
        years = int(request.form["years"])
        rate = float(request.form["rate"])

        cashflows_full = [-initial_cost] + cashflows  # include initial cost

        # Calculate financial metrics
        npv = calculate_npv(rate, cashflows_full)
        irr = calculate_irr(cashflows_full)
        arr = calculate_arr(initial_cost, cashflows_full)

        # Overall decision
        decision = "Good to invest" if npv > 0 and irr > rate and arr > rate else "Not good to invest"

        # Generate dynamic recommendations
        recommendations = generate_dynamic_recommendations(initial_cost, cashflows_full, rate, npv, irr, arr, years)

        # Prepare result dictionary
        result = {
            "NPV": round(npv, 2),
            "IRR": round(irr, 2),
            "ARR": round(arr, 2),
            "Decision": decision,
            "rate": rate,
            "recommendations": recommendations
        }

    return render_template("index.html", result=result)

# if __name__ == "__main__":
    # app.run(debug=True)
