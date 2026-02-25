import streamlit as st

st.set_page_config(page_title="FinSight AI - Finance Optimizer", layout="wide")

st.title("💡 FinSight AI")
st.subheader("AI-Powered Personal Finance Optimization System")

st.markdown("### Enter Your Monthly Financial Details")

# ================= INPUT SECTION =================

col1, col2, col3, col4 = st.columns(4)

with col1:
    income = st.number_input("Total Income (₹)", min_value=1)

with col2:
    rent = st.number_input("Rent / Housing (₹)", min_value=0)

with col3:
    emi = st.number_input("EMI / Loans (₹)", min_value=0)

with col4:
    food = st.number_input("Food & Groceries (₹)", min_value=0)

col5, col6, col7, col8 = st.columns(4)

with col5:
    transport = st.number_input("Transport (₹)", min_value=0)

with col6:
    shopping = st.number_input("Shopping (₹)", min_value=0)

with col7:
    entertainment = st.number_input("Entertainment (₹)", min_value=0)

with col8:
    medical = st.number_input("Medical / Health (₹)", min_value=0)


# ================= EVALUATION ENGINE =================

def evaluate_actions(income, fixed, variable):

    total_expense = fixed + sum(variable.values())
    current_savings = income - total_expense
    current_rate = current_savings / income

    results = {}

    for category, value in variable.items():

        if value == 0:
            continue

        # simulate 10% reduction
        reduced_value = value * 0.9

        simulated_variable = variable.copy()
        simulated_variable[category] = reduced_value

        new_total = fixed + sum(simulated_variable.values())
        new_savings = income - new_total
        new_rate = new_savings / income

        improvement = new_rate - current_rate

        # Essential penalty
        penalty = 0
        if category in ["Food", "Medical"]:
            penalty = 1

        # Reward Function
        reward = (5 * improvement) + (2 * new_rate) - penalty

        results[category] = {
            "new_rate": new_rate,
            "improvement": improvement,
            "reward": reward
        }

    return current_rate, results


# ================= BUTTON =================

if st.button("Generate Financial Report"):

    fixed = rent + emi

    variable = {
        "Food": food,
        "Transport": transport,
        "Shopping": shopping,
        "Entertainment": entertainment,
        "Medical": medical
    }

    total_expense = fixed + sum(variable.values())
    savings = income - total_expense
    savings_rate = savings / income

    # ================= DASHBOARD METRICS =================

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Total Income", f"₹{income}")
    m2.metric("Total Expenses", f"₹{total_expense}")
    m3.metric("Net Savings", f"₹{savings}")
    m4.metric("Savings Rate", f"{round(savings_rate*100,2)}%")

    # ================= HEALTH SCORE =================

    health_score = min(max(int(savings_rate * 200), 0), 100)

    st.markdown("### Financial Health Score")
    st.progress(health_score)
    st.write(f"Score: {health_score}/100")

    # ================= OPTIMAL EVALUATION =================

    current_rate, results = evaluate_actions(income, fixed, variable)

    if len(results) == 0:
        st.warning("No adjustable expenses available for optimization.")
    else:

        st.markdown("### 📊 Action Evaluation Table")

        display_table = []

        for category, values in results.items():
            display_table.append([
                category,
                round(values["new_rate"] * 100, 2),
                round(values["improvement"] * 100, 2),
                round(values["reward"], 4)
            ])

        st.table(display_table)

        # Find Best Action
        best_action = max(results, key=lambda x: results[x]["reward"])
        best_values = results[best_action]

        st.markdown("### 🎯 Optimal Recommendation")

        st.success(
            f"Reduce **{best_action}** by 10%.\n\n"
            f"Savings Rate improves from {round(current_rate*100,2)}% "
            f"to {round(best_values['new_rate']*100,2)}%.\n\n"
            f"This action yields the highest calculated reward based on "
            f"savings improvement and essential expense penalties."
        )
