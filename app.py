import streamlit as st

st.set_page_config(page_title="FinSight AI", layout="wide")

st.title("💡 FinSight AI - Smart Finance Optimizer")
st.subheader("See Where Your Money Is Going. Fix It Intelligently.")

# ================= INPUT =================

st.markdown("### Enter Monthly Financial Details")

col1, col2, col3, col4 = st.columns(4)

with col1:
    income = st.number_input("Income (₹)", min_value=1)

with col2:
    rent = st.number_input("Rent (₹)", min_value=0)

with col3:
    emi = st.number_input("EMI (₹)", min_value=0)

with col4:
    food = st.number_input("Food (₹)", min_value=0)

col5, col6, col7, col8 = st.columns(4)

with col5:
    transport = st.number_input("Transport (₹)", min_value=0)

with col6:
    shopping = st.number_input("Shopping (₹)", min_value=0)

with col7:
    entertainment = st.number_input("Entertainment (₹)", min_value=0)

with col8:
    medical = st.number_input("Medical (₹)", min_value=0)


# ================= EVALUATION ENGINE =================

def evaluate_actions(income, fixed, variable):

    total_expense = fixed + sum(variable.values())
    current_savings = income - total_expense
    current_rate = current_savings / income

    results = {}

    for category, value in variable.items():

        if value == 0:
            continue

        reduced_value = value * 0.9
        simulated_variable = variable.copy()
        simulated_variable[category] = reduced_value

        new_total = fixed + sum(simulated_variable.values())
        new_savings = income - new_total
        new_rate = new_savings / income
        improvement = new_rate - current_rate

        penalty = 0
        if category in ["Food", "Medical"]:
            penalty = 1

        reward = (5 * improvement) + (2 * new_rate) - penalty

        results[category] = {
            "new_rate": new_rate,
            "improvement": improvement,
            "reward": reward
        }

    return current_rate, results


# ================= MAIN BUTTON =================

if st.button("Analyze My Finances"):

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

    # ================= DASHBOARD =================

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

    # ================= EXPENSE BREAKDOWN =================

    st.markdown("## 📊 Expense Breakdown (% of Income)")

    for k, v in variable.items():
        if income > 0:
            percent = round((v / income) * 100, 2)
            st.write(f"{k}: {percent}%")

    # ================= SHOCK IMPACT =================

    if savings < 0:
        st.error(f"🚨 You are losing ₹{abs(savings)} per month!")
    else:
        yearly_savings = savings * 12
        st.info(f"💰 At this rate, you will save ₹{yearly_savings} in 1 year.")

    # ================= OPTIMAL POLICY EVALUATION =================

    current_rate, results = evaluate_actions(income, fixed, variable)

    if len(results) == 0:
        st.warning("No adjustable expenses available.")
    else:

        best_action = max(results, key=lambda x: results[x]["reward"])
        best_values = results[best_action]

        improvement_percent = round(best_values["improvement"] * 100, 2)
        new_rate_percent = round(best_values["new_rate"] * 100, 2)

        st.markdown("## 🤖 AI Optimal Recommendation")

        st.success(
            f"Cut **{best_action}** by 10%.\n\n"
            f"Savings Rate improves from {round(current_rate*100,2)}% "
            f"to {new_rate_percent}%.\n\n"
            f"Immediate Improvement: {improvement_percent}%"
        )

        # ================= YEARLY IMPACT =================

        old_year = savings * 12
        projected_variable = variable.copy()
        projected_variable[best_action] *= 0.9
        new_year = (income - (fixed + sum(projected_variable.values()))) * 12

        st.markdown("### 💥 Financial Impact Projection")

        st.write(f"Current Yearly Savings: ₹{old_year}")
        st.write(f"After Optimization: ₹{int(new_year)}")
        st.write(f"Extra Money Gained in 1 Year: ₹{int(new_year - old_year)}")

        # ================= POLICY TABLE =================

        st.markdown("---")
        st.markdown("## 📚 Optimal Policy Evaluation Table")

        policy_data = []

        for category, values in results.items():
            policy_data.append([
                category,
                round(values["new_rate"] * 100, 2),
                round(values["improvement"] * 100, 2),
                round(values["reward"], 4)
            ])

        policy_data.sort(key=lambda x: x[3], reverse=True)

        st.table(
            [["Action",
              "New Savings Rate (%)",
              "Improvement (%)",
              "Reward Score"]] + policy_data
        )

        st.markdown("### 🏆 Optimal Policy Selected")

        st.success(
            f"Best Action: **{best_action}**\n\n"
            f"Highest Reward Score: {round(best_values['reward'],4)}"
        )

        # ================= EXPLANATION =================

        st.markdown("### 🧠 Why This Action?")

        st.write(
            "Each possible expense reduction is evaluated using a weighted reward function "
            "based on savings improvement and essential expense penalties. "
            f"The action '{best_action}' produces the highest net financial reward "
            "while maintaining financial stability."
        )
