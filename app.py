import streamlit as st
import pandas as pd
 
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
# INTRODUCTION
# ============================================================
 
st.markdown("### This model illustrates a formally specified behavioral decision algorithm")
 
st.markdown("---")
 
st.markdown("**The concept:**")
st.markdown("""
Decisions are defined as behaviors that are selected from options. The process to consider 
making any specific decision, a decision in itself, is referred to as salience.
 
All behavior options have attributes — a quality, trait, or feature inherent to that option. 
It is proposed that the impact of each option's attributes are evaluated using three factors — 
**Rank (K)**: relative importance; **Saturation (S)**: proximity to optimal level; 
**Contingency (C)**: probability of realization. The algorithm computes V = C × (S × K), 
sums rewards minus punishments to produce B, applies decision salience D, and enacts 
the highest B* option.
""")
 
st.markdown("---")
 
st.markdown("**The illustration:**")
st.markdown("""
A young man receives a cash bonus and considers four behavioral options: buying a new car, 
holding on to the money (doing nothing), investing in a CD or investing in stock. 
The decision outcome will vary with the weight of each option's factors. See how each 
factor works — expand each option below to adjust its **Rank (K)**, **Saturation (S)**, 
and **Contingency (C)** values. The decision he will make (illustrated in the bar chart) 
updates instantly as you adjust any slider.
""")
 
st.markdown("---")
 
# ============================================================
# ABOUT
# ============================================================
 
with st.expander("ℹ️ About The Theory of Behavior", expanded=False):
    st.markdown("""
    **The Theory of Behavior** is a formally specified, invariant algorithm 
    modeling how people reach behavioral decisions.
    
    **Four distinctive properties:**
    - **Invariant** — identical process across all individuals regardless of physiological, genetic, or cultural variation
    - **Recursive** — the decision to consider a decision is itself a behavioral computation  
    - **Bayesian** — attribute values update continuously through experience
    - **Quantifying** — previously unquantifiable states (satisfaction, anxiety, fear, despair) defined as computable conditions
    
    **The core equations:**
    - V(aⱼ) = C × (S × K) — attribute valence
    - B(Bᵢ) = R(Bᵢ) − P(Bᵢ) — behavioral option value
    - B*(Bᵢ) = D × B(Bᵢ) — salience adjusted value
    
    **K** = Rank (0–10) | **S** = Saturation (0–1) | **C** = Contingency (0–1) | **D** = Decision Salience (0–1)
    
    **Full paper:** [SSRN](https://ssrn.com/abstract=6242578) | 
    **Code:** [GitHub](https://github.com/dmchabon/theory-of-behavior)
    """)
 
st.markdown("---")
 
# ============================================================
# LAYOUT
# ============================================================
 
slider_col, result_col = st.columns([1, 2])
 
with slider_col:
 
    st.markdown("### Attribute Values")
    D = st.slider("**D — Decision Salience** (from umwelt)", 0.0, 1.0, 0.8, 0.1)
 
    # ── BUY NEW CAR ──
    with st.expander("🚗 Buy New Car", expanded=False):
        st.markdown("*Nicer Travel*")
        car_travel_k = st.slider("K — Rank", 0, 10, 8, key="car_travel_k")
        car_travel_s = st.slider("S — Saturation", 0.0, 1.0, 0.7, 0.1, key="car_travel_s")
        car_travel_c = st.slider("C — Contingency", 0.0, 1.0, 0.4, 0.1, key="car_travel_c")
 
        st.markdown("*Impress Girlfriend*")
        car_gf_k = st.slider("K — Rank", 0, 10, 8, key="car_gf_k")
        car_gf_s = st.slider("S — Saturation", 0.0, 1.0, 0.6, 0.1, key="car_gf_s")
        car_gf_c = st.slider("C — Contingency", 0.0, 1.0, 0.3, 0.1, key="car_gf_c")
 
        st.markdown("*Extrinsic Value*")
        car_ext_k = st.slider("K — Rank", 0, 10, 8, key="car_ext_k")
        car_ext_s = st.slider("S — Saturation", 0.0, 1.0, 0.7, 0.1, key="car_ext_s")
        car_ext_c = st.slider("C — Contingency", 0.0, 1.0, 0.7, 0.1, key="car_ext_c")
 
    # ── DO NOTHING ──
    with st.expander("💰 Do Nothing", expanded=False):
        st.markdown("*Have Cash*")
        nothing_k = st.slider("K — Rank", 0, 10, 7, key="nothing_k")
        nothing_s = st.slider("S — Saturation", 0.0, 1.0, 0.9, 0.1, key="nothing_s")
        nothing_c = st.slider("C — Contingency", 0.0, 1.0, 0.9, 0.1, key="nothing_c")
 
    # ── INVEST IN CD ──
    with st.expander("🏦 Invest in CD", expanded=False):
        st.markdown("*Security*")
        cd_sec_k = st.slider("K — Rank", 0, 10, 7, key="cd_sec_k")
        cd_sec_s = st.slider("S — Saturation", 0.0, 1.0, 0.4, 0.1, key="cd_sec_s")
        cd_sec_c = st.slider("C — Contingency", 0.0, 1.0, 0.9, 0.1, key="cd_sec_c")
 
        st.markdown("*Return*")
        cd_ret_k = st.slider("K — Rank", 0, 10, 3, key="cd_ret_k")
        cd_ret_s = st.slider("S — Saturation", 0.0, 1.0, 0.8, 0.1, key="cd_ret_s")
        cd_ret_c = st.slider("C — Contingency", 0.0, 1.0, 0.9, 0.1, key="cd_ret_c")
 
        st.markdown("*Extrinsic Value*")
        cd_ext_k = st.slider("K — Rank", 0, 10, 1, key="cd_ext_k")
        cd_ext_s = st.slider("S — Saturation", 0.0, 1.0, 0.1, 0.1, key="cd_ext_s")
        cd_ext_c = st.slider("C — Contingency", 0.0, 1.0, 0.1, 0.1, key="cd_ext_c")
 
    # ── INVEST IN STOCK ──
    with st.expander("📈 Invest in Stock", expanded=False):
        st.markdown("*Security*")
        stk_sec_k = st.slider("K — Rank", 0, 10, 3, key="stk_sec_k")
        stk_sec_s = st.slider("S — Saturation", 0.0, 1.0, 0.7, 0.1, key="stk_sec_s")
        stk_sec_c = st.slider("C — Contingency", 0.0, 1.0, 0.3, 0.1, key="stk_sec_c")
 
        st.markdown("*Return Potential*")
        stk_ret_k = st.slider("K — Rank", 0, 10, 6, key="stk_ret_k")
        stk_ret_s = st.slider("S — Saturation", 0.0, 1.0, 0.7, 0.1, key="stk_ret_s")
        stk_ret_c = st.slider("C — Contingency", 0.0, 1.0, 0.4, 0.1, key="stk_ret_c")
 
        st.markdown("*Extrinsic Value*")
        stk_ext_k = st.slider("K — Rank", 0, 10, 7, key="stk_ext_k")
        stk_ext_s = st.slider("S — Saturation", 0.0, 1.0, 0.7, 0.1, key="stk_ext_s")
        stk_ext_c = st.slider("C — Contingency", 0.0, 1.0, 0.2, 0.1, key="stk_ext_c")
 
# ============================================================
# COMPUTE
# ============================================================
 
options = [
    {
        'name': 'Invest in CD',
        'attributes': [
            {'name': 'Security',       'K': cd_sec_k, 'S': cd_sec_s, 'C': cd_sec_c, 'type': 'reward'},
            {'name': 'Return',         'K': cd_ret_k, 'S': cd_ret_s, 'C': cd_ret_c, 'type': 'reward'},
            {'name': 'Extrinsic Value','K': cd_ext_k, 'S': cd_ext_s, 'C': cd_ext_c, 'type': 'reward'},
        ]
    },
    {
        'name': 'Invest in Stock',
        'attributes': [
            {'name': 'Security',       'K': stk_sec_k, 'S': stk_sec_s, 'C': stk_sec_c, 'type': 'reward'},
            {'name': 'Return',         'K': stk_ret_k, 'S': stk_ret_s, 'C': stk_ret_c, 'type': 'reward'},
            {'name': 'Extrinsic Value','K': stk_ext_k, 'S': stk_ext_s, 'C': stk_ext_c, 'type': 'reward'},
        ]
    },
    {
        'name': 'Buy New Car',
        'attributes': [
            {'name': 'Nicer Travel',      'K': car_travel_k, 'S': car_travel_s, 'C': car_travel_c, 'type': 'reward'},
            {'name': 'Impress Girlfriend','K': car_gf_k,     'S': car_gf_s,     'C': car_gf_c,     'type': 'reward'},
            {'name': 'Extrinsic Value',   'K': car_ext_k,    'S': car_ext_s,    'C': car_ext_c,    'type': 'reward'},
        ]
    },
    {
        'name': 'Do Nothing',
        'attributes': [
            {'name': 'Have Cash', 'K': nothing_k, 'S': nothing_s, 'C': nothing_c, 'type': 'reward'},
        ]
    },
]
 
results, conflict = select_behavior(options, D)
 
# ============================================================
# RESULTS
# ============================================================
 
with result_col:
    st.markdown("### Behavioral Decision Computation")
 
    enacted = results[0]
 
    if conflict:
        st.warning("⚠️ CONFLICT CONDITION: Two options have near-equal B* values — hesitation or ambivalence predicted.")
 
    st.success(f"✅ ENACTED BEHAVIOR: **{enacted['name']}** (B* = {enacted['B_star']})")
 
    st.markdown("**Ranked Options by B* Value:**")
 
    df = pd.DataFrame({
        'Option': [r['name'] for r in results],
        'B*': [r['B_star'] for r in results]
    })
    st.bar_chart(df.set_index('Option'))
 
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
 
    st.markdown("---")
    st.markdown("""
    ### Demonstrating Invariance
 
    Expand any option above and adjust its sliders. Notice that:
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
