import streamlit as st
import numpy as np
import random

st.set_page_config(page_title="FinSight AI - RL Finance Optimizer", layout="wide")

st.title("💡 FinSight AI")
st.subheader("AI-Powered Personal Finance Optimization using Reinforcement Learning")

# ===================== INPUT SECTION =====================

st.markdown("### Enter Your Monthly Finances")

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
    medical = st.number_input("Medical (₹)", min_value=0)


if st.button("Generate AI Financial Report"):

    # ===================== BASIC CALCULATIONS =====================

    fixed = rent + emi

    variable = {
        "Food": food,
        "Transport": transport,
        "Shopping": shopping,
        "Entertainment": entertainment,
        "Medical": medical
    }

    valid_variable = {k: v for k, v in variable.items() if v > 0}

    total_expense = fixed + sum(variable.values())
    savings = income - total_expense
    savings_rate = savings / income

    # ===================== DASHBOARD METRICS =====================

    st.markdown("---")
    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Total Income", f"₹{income}")
    m2.metric("Total Expenses", f"₹{total_expense}")
    m3.metric("Net Savings", f"₹{savings}")
    m4.metric("Savings Rate", f"{round(savings_rate*100,2)}%")

    # ===================== FINANCIAL HEALTH SCORE =====================

    health_score = min(max(int(savings_rate * 200), 0), 100)

    st.markdown("### Financial Health Score")
    st.progress(health_score)
    st.write(f"Score: {health_score}/100")

    # ===================== RL ENVIRONMENT =====================

    class FinanceEnv:

        def __init__(self):
            self.reset()

        def reset(self):
            self.variable = valid_variable.copy()
            return self.get_state()

        def get_state(self):
            total = fixed + sum(self.variable.values())
            s = income - total
            rate = s / income

            if rate < 0:
                return 0
            elif rate < 0.1:
                return 1
            elif rate < 0.2:
                return 2
            elif rate < 0.35:
                return 3
            else:
                return 4

        def step(self, action_index):
            categories = list(self.variable.keys())
            category = categories[action_index]

            self.variable[category] *= 0.9  # reduce 10%

            next_state = self.get_state()

            total = fixed + sum(self.variable.values())
            reward = (income - total) / income

            return next_state, reward


    if len(valid_variable) == 0:
        st.warning("No adjustable expenses available for optimization.")
    else:

        env = FinanceEnv()

        state_size = 5
        action_size = len(valid_variable)

        q_table = np.zeros((state_size, action_size))

        episodes = 600
        alpha = 0.1
        gamma = 0.9
        epsilon = 0.2

        # ===================== TRAINING =====================

        for _ in range(episodes):
            state = env.reset()

            for _ in range(6):
                if random.uniform(0,1) < epsilon:
                    action = random.randint(0, action_size - 1)
                else:
                    action = np.argmax(q_table[state])

                next_state, reward = env.step(action)

                q_table[state][action] += alpha * (
                    reward + gamma * np.max(q_table[next_state]) - q_table[state][action]
                )

                state = next_state

        # ===================== OPTIMAL POLICY =====================

        current_env = FinanceEnv()
        current_state = current_env.reset()

        best_action_index = np.argmax(q_table[current_state])
        best_category = list(valid_variable.keys())[best_action_index]

        # Projected improvement
        projected = valid_variable.copy()
        projected[best_category] *= 0.9

        projected_total = fixed + sum(projected.values())
        projected_savings = income - projected_total
        projected_rate = projected_savings / income

        state_labels = {
            0: "LOSS",
            1: "VERY LOW",
            2: "LOW",
            3: "MEDIUM",
            4: "HIGH"
        }

        st.markdown("### 🤖 RL-Based Optimal Policy Recommendation")

        st.success(
            f"Current State: {state_labels[current_state]} \n\n"
            f"Optimal Action: Reduce **{best_category}** by 10% \n\n"
            f"Savings Rate improves from {round(savings_rate*100,2)}% "
            f"to {round(projected_rate*100,2)}%"
        )

        st.markdown("### 🧠 Learned Policy (Q-Table)")
        st.dataframe(q_table)
