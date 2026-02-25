import streamlit as st
import numpy as np
import random
import copy

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="AI Finance RL Optimizer", layout="wide")

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    .main-title {
        font-size: 32px;
        font-weight: bold;
        color: #2E86C1;
    }
    .section-title {
        font-size: 20px;
        font-weight: 600;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">AI-Based Personal Finance Optimization System (Reinforcement Learning)</div>', unsafe_allow_html=True)

st.markdown("Optimize your monthly budget using Reinforcement Learning to learn the best financial strategy.")

# ---------------- USER INPUT ----------------
st.markdown('<div class="section-title">Enter Monthly Financial Details</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    income = st.number_input("Total Monthly Income (Rs)", min_value=0.0)
    rent = st.number_input("Rent / Housing (Rs)", min_value=0.0)
    emi = st.number_input("EMI / Loans (Rs)", min_value=0.0)
    food = st.number_input("Food & Groceries (Rs)", min_value=0.0)

with col2:
    transport = st.number_input("Transport (Rs)", min_value=0.0)
    shopping = st.number_input("Shopping (Rs)", min_value=0.0)
    entertainment = st.number_input("Entertainment (Rs)", min_value=0.0)
    medical = st.number_input("Medical & Health (Rs)", min_value=0.0)

# ---------------- RL LOGIC ----------------
if st.button("Run RL Optimization"):

    if income == 0:
        st.error("Income must be greater than zero.")
        st.stop()

    fixed = rent + emi

    variable_dict = {
        "Food": food,
        "Transport": transport,
        "Shopping": shopping,
        "Entertainment": entertainment,
        "Medical": medical
    }

    class FinanceEnv:
        def __init__(self, income, fixed, variable_dict):
            self.initial_income = income
            self.initial_fixed = fixed
            self.initial_variable = variable_dict
            self.reset()

        def reset(self):
            self.income = self.initial_income
            self.fixed = self.initial_fixed
            self.variable = copy.deepcopy(self.initial_variable)
            return self.get_state()

        def get_state(self):
            total_exp = self.fixed + sum(self.variable.values())
            savings = self.income - total_exp
            savings_rate = savings / self.income

            if savings_rate < 0:
                return "LOSS"
            elif savings_rate < 0.05:
                return "VERY_LOW"
            elif savings_rate < 0.15:
                return "LOW"
            elif savings_rate < 0.25:
                return "MEDIUM"
            else:
                return "HIGH"

        def step(self, action):
            categories = list(self.variable.keys())
            self.variable[categories[action]] *= 0.9

            total_exp = self.fixed + sum(self.variable.values())
            savings = self.income - total_exp
            savings_rate = savings / self.income

            if savings_rate >= 0.25:
                reward = 20
            elif savings_rate >= 0.15:
                reward = 10
            elif savings_rate >= 0.05:
                reward = 5
            else:
                reward = -15

            return self.get_state(), reward

    # Initialize RL
    env = FinanceEnv(income, fixed, variable_dict)
    states = ["LOSS", "VERY_LOW", "LOW", "MEDIUM", "HIGH"]
    actions = list(range(len(variable_dict)))
    q_table = {state: [0]*len(actions) for state in states}

    alpha = 0.1
    gamma = 0.9
    epsilon = 0.2
    episodes = 600

    # Training
    for episode in range(episodes):
        state = env.reset()
        for step in range(12):
            if random.uniform(0,1) < epsilon:
                action = random.choice(actions)
            else:
                action = np.argmax(q_table[state])

            next_state, reward = env.step(action)

            old_value = q_table[state][action]
            next_max = max(q_table[next_state])

            q_table[state][action] = old_value + alpha * (reward + gamma * next_max - old_value)
            state = next_state

    # Final Recommendation
    current_state = env.reset()
    best_action_index = np.argmax(q_table[current_state])
    best_category = list(variable_dict.keys())[best_action_index]

    total_exp = fixed + sum(variable_dict.values())
    initial_savings = income - total_exp
    initial_rate = round(initial_savings/income, 2)

    st.markdown('<div class="section-title">Financial Analysis</div>', unsafe_allow_html=True)

    colA, colB, colC = st.columns(3)

    colA.metric("Current Savings Rate", f"{initial_rate*100}%")
    colB.metric("Financial State", current_state)
    colC.metric("Recommended Action", f"Reduce {best_category}")

    st.markdown('<div class="section-title">RL Model Details</div>', unsafe_allow_html=True)

    st.write("Environment: Monthly Personal Finance Simulator")
    st.write("Agent: Q-Learning Optimizer")
    st.write("Policy: State → Optimal Expense Reduction Strategy")
    st.write("Goal: Maximize Long-Term Savings Rate")
