import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="The Theory of Behavior",
    page_icon="🧠",
    layout="wide"
)

# ============================================================
# CORE ALGORITHM
# ============================================================

def compute_valence(K, S, C):
    return round(C * (S * K), 4)

def compute_B_value(attributes):
    R_total = 0.0
    P_total = 0.0
    for attr in attributes:
        if attr['type'] == 'extinction':
            valence = 0.0
        else:
            valence = compute_valence(attr['K'], attr['S'], attr['C'])
        if attr['type'] == 'reward':
            R_total += valence
        elif attr['type'] == 'punishment':
            P_total += valence
    B = R_total - P_total
    return round(R_total, 4), round(P_total, 4), round(B, 4)

def select_behavior(options, D, epsilon=0.01):
    results = []
    for option in options:
        R, P, B = compute_B_value(option['attributes'])
        B_star = round(D * B, 4)
        results.append({
            'name': option['name'],
            'R': R, 'P': P, 'B': B, 'B_star': B_star
        })
    results.sort(key=lambda x: x['B_star'], reverse=True)
    conflict = len(results) >= 2 and abs(results[0]['B_star'] - results[1]['B_star']) < epsilon
    return results, conflict

# ============================================================
# HEADER
# ============================================================

st.title("The Theory of Behavior")
st.subheader("A Fundamental Comprehensive Algorithm for Human Behavior")
st.markdown("*D.M. Chabon — Applied Behavioral Science Strategies*")
st.markdown("---")

# ============================================================
# ABOUT
# ============================================================

with st.expander("ℹ️ About this app", expanded=False):
    st.markdown("""
    This app demonstrates **The Theory of Behavior** — a formally specified, invariant algorithm 
    modeling how people reach behavioral decisions.
    
    **Four distinctive properties:**
    - **Invariant** — identical process across all individuals regardless of physiological, genetic, or cultural variation
    - **Recursive** — the decision to consider a decision is itself a behavioral computation  
    - **Bayesian** — attribute values update continuously through experience
    - **Quantifying** — previously unquantifiable states (satisfaction, anxiety, fear, despair) defined as computable conditions
    
    **The core equations:**
    - V(aⱼ) = C × (S × K)
    - B(Bᵢ) = R(Bᵢ) − P(Bᵢ)  
    - B*(Bᵢ) = D × B(Bᵢ)
    
    **Full paper:** [SSRN](https://ssrn.com/abstract=6242578) | 
    **Code:** [GitHub](https://github.com/dmchabon/theory-of-behavior)
    """)

# ============================================================
# SCENARIO
# ============================================================

st.markdown("## The Bonus Decision Scenario")
st.markdown("""
A young man receives a cash bonus and considers four behavioral options. 
Adjust the sliders to change his perceived attribute values and watch the algorithm predict which behavior he will enact.
""")

st.markdown("---")

# ============================================================
# SLIDERS
# ============================================================

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Adjust Attribute Values")
    st.markdown("**Decision Salience**")
    D = st.slider("D — Decision Salience (from umwelt)", 0.0, 1.0, 0.8, 0.1)
    
    st.markdown("**Buy New Car — Reward Attributes**")
    k_travel = st.slider("Nicer Travel — Rank (K)", 0, 10, 8)
    k_girlfriend = st.slider("Impress Girlfriend — Rank (K)", 0, 10, 8)
    k_extrinsic_car = st.slider("Extrinsic Value (Car) — Rank (K)", 0, 10, 8)
    
    st.markdown("**Do Nothing — Reward Attributes**")
    k_cash = st.slider("Have Cash — Rank (K)", 0, 10, 7)
    
    st.markdown("**Invest in CD — Reward Attributes**")
    k_security_cd = st.slider("Security (CD) — Rank (K)", 0, 10, 7)

# ============================================================
# COMPUTE
# ============================================================

options = [
    {
        'name': 'Invest in CD',
        'attributes': [
            {'name': 'Security',       'K': k_security_cd, 'S': 0.4, 'C': 0.9, 'type': 'reward'},
            {'name': 'Return',         'K': 3, 'S': 0.8, 'C': 0.9, 'type': 'reward'},
            {'name': 'Extrinsic Value','K': 1, 'S': 0.1, 'C': 0.1, 'type': 'reward'},
        ]
    },
    {
        'name': 'Invest in Stock',
        'attributes': [
            {'name': 'Security',       'K': 3, 'S': 0.7, 'C': 0.3, 'type': 'reward'},
            {'name': 'Return',         'K': 6, 'S': 0.7, 'C': 0.4, 'type': 'reward'},
            {'name': 'Extrinsic Value','K': 7, 'S': 0.7, 'C': 0.2, 'type': 'reward'},
        ]
    },
    {
        'name': 'Buy New Car',
        'attributes': [
            {'name': 'Nicer Travel',      'K': k_travel,      'S': 0.7, 'C': 0.4, 'type': 'reward'},
            {'name': 'Impress Girlfriend','K': k_girlfriend,  'S': 0.6, 'C': 0.3, 'type': 'reward'},
            {'name': 'Extrinsic Value',   'K': k_extrinsic_car,'S': 0.7, 'C': 0.7, 'type': 'reward'},
        ]
    },
    {
        'name': 'Do Nothing',
        'attributes': [
            {'name': 'Have Cash', 'K': k_cash, 'S': 0.9, 'C': 0.9, 'type': 'reward'},
        ]
    },
]

results, conflict = select_behavior(options, D)

# ============================================================
# RESULTS
# ============================================================

with col2:
    st.markdown("### Behavioral Decision Computation")
    
    enacted = results[0]
    
    if conflict:
        st.warning("⚠️ CONFLICT CONDITION: Two options have near-equal B* values — hesitation or ambivalence predicted.")
    
    st.success(f"✅ ENACTED BEHAVIOR: **{enacted['name']}** (B* = {enacted['B_star']})")
    
    st.markdown("**Ranked Options by B* Value:**")
    
    # Bar chart
    import pandas as pd
    df = pd.DataFrame({
        'Option': [r['name'] for r in results],
        'B*': [r['B_star'] for r in results]
    })
    st.bar_chart(df.set_index('Option'))
    
    # Details table
    st.markdown("**Full Computation:**")
    table_data = []
    for r in results:
        marker = " ← ENACTED" if r['name'] == enacted['name'] else ""
        table_data.append({
            'Option': r['name'] + marker,
            'R (Rewards)': r['R'],
            'P (Punishments)': r['P'],
            'B = R−P': r['B'],
            'B* = D×B': r['B_star']
        })
    st.dataframe(pd.DataFrame(table_data), hide_index=True)

# ============================================================
# INVARIANCE NOTE
# ============================================================

st.markdown("---")
st.markdown("""
### Demonstrating Invariance

Try adjusting the sliders above. Notice that:
- The **same algorithm** runs regardless of what values you enter
- **Different attribute values** produce different enacted behaviors  
- This demonstrates **invariance** — the process is universal, the inputs vary

*"The alignment problem may be fundamentally a Rank problem."*
""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown("""
**D.M. Chabon** — Applied Behavioral Science Strategies  
📄 [Full Paper on SSRN](https://ssrn.com/abstract=6242578) | 
💻 [GitHub Repository](https://github.com/dmchabon/theory-of-behavior) |
📧 d.m.chabon@thetheoryofbehavior.org  
*Critique anticipated and invited.*
""")
