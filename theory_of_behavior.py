Appendix D:  Python Implementation of the Algorithm

The Theory of Behavior - A Fundamental Comprehensive Algorithm for Human Behavior
D.M. Chabon, Applied Behavioral Science Strategies

The following code implements the mathematical formulation presented in Appendix C, demonstrating the computational tractability of the model and facilitating replication and extension by other researchers. 
The implementation is demonstrated using a sample scenario in which a young man decides how to allocate a cash bonus across four behavioral options.

"""
The Theory of Behavior
A Fundamental Comprehensive Algorithm for Human Behavior
D.M. Chabon, Applied Behavioral Science Strategies

Python Implementation
"""

# ============================================================
# CORE COMPUTATION
# ============================================================

def compute_valence(K, S, C):
    """
    Compute the valence of a single attribute.
    V(aj) = C x (S x K)
    
    Parameters:
        K : float [0,1] - Rank (relative strength of attribute)
        S : float [0,1] - Saturation (proximity to optimal level)
        C : float [0,1] - Contingency (perceived probability of occurrence)
    
    Returns:
        float - valence value of the attribute
    """
    return C * (S * K)


def compute_B_value(attributes):
    """
    Compute the B value for a single behavioral option.
    B(Bi) = R(Bi) - P(Bi)
    where R = sum of reward attribute valences
          P = sum of punishment attribute valences
    
    Parameters:
        attributes : list of dicts, each containing:
            'name'   : str   - attribute name
            'K'      : float - rank
            'S'      : float - saturation
            'C'      : float - contingency
            'type'   : str   - 'reward', 'punishment', or 'extinction'
    
    Returns:
        dict containing B value, R total, P total, and attribute details
    """
    R_total = 0.0
    P_total = 0.0
    attribute_details = []

    for attr in attributes:
        if attr['type'] == 'extinction':
            valence = 0.0
        else:
            valence = compute_valence(attr['K'], attr['S'], attr['C'])
        
        if attr['type'] == 'reward':
            R_total += valence
        elif attr['type'] == 'punishment':
            P_total += valence

        attribute_details.append({
            'name': attr['name'],
            'type': attr['type'],
            'K': attr['K'],
            'S': attr['S'],
            'C': attr['C'],
            'valence': round(valence, 4)
        })

    B = R_total - P_total
    return {
        'R': round(R_total, 4),
        'P': round(P_total, 4),
        'B': round(B, 4),
        'attributes': attribute_details
    }


def compute_B_star(B, D):
    """
    Apply decision salience D (from umwelt U) to B value.
    B*(Bi) = D x B(Bi)
    
    Parameters:
        B : float - raw B value
        D : float [0,1] - decision salience from umwelt
    
    Returns:
        float - salience-adjusted B value
    """
    return round(D * B, 4)


def select_behavior(options, D, epsilon=0.01):
    """
    Compare B* values across all perceived available options
    and select the enacted behavior.
    B* = argmax{B*(Bi)} for all Bi in Omega
    
    Parameters:
        options  : list of dicts, each containing 'name' and 'attributes'
        D        : float [0,1] - decision salience from umwelt
        epsilon  : float - threshold for conflict condition detection
    
    Returns:
        dict containing full results and enacted behavior
    """
    results = []

    for option in options:
        b_result = compute_B_value(option['attributes'])
        B_star = compute_B_star(b_result['B'], D)
        results.append({
            'name': option['name'],
            'R': b_result['R'],
            'P': b_result['P'],
            'B': b_result['B'],
            'B_star': B_star,
            'attributes': b_result['attributes']
        })

    # Sort by B* descending
    results.sort(key=lambda x: x['B_star'], reverse=True)

    # Check for conflict condition
    conflict = False
    if len(results) >= 2:
        if abs(results[0]['B_star'] - results[1]['B_star']) < epsilon:
            conflict = True

    enacted = results[0]

    return {
        'D': D,
        'all_options': results,
        'enacted': enacted,
        'conflict': conflict
    }


def bayesian_update(K, S, C, outcome, reliability, importance, alpha=0.1):
    """
    Update K, S, C values based on outcome of enacted behavior.
    
    S(aj)t+1 = S(aj)t + alpha[Outcome(aj) - S(aj)t]
    C(aj)t+1 = C(aj)t + alpha[Reliability(aj) - C(aj)t]
    K(aj)t+1 = K(aj)t + alpha[Importance(aj) - K(aj)t]
    
    Parameters:
        K, S, C      : float - current values
        outcome      : float [0,1] - actual outcome magnitude
        reliability  : float [0,1] - actual reliability observed
        importance   : float [0,1] - revised importance assessment
        alpha        : float [0,1] - learning rate
    
    Returns:
        dict with updated K, S, C values
    """
    S_new = round(S + alpha * (outcome - S), 4)
    C_new = round(C + alpha * (reliability - C), 4)
    K_new = round(K + alpha * (importance - K), 4)

    return {'K': K_new, 'S': S_new, 'C': C_new}


# ============================================================
# DISPLAY
# ============================================================

def print_results(result):
    """Display full computation results clearly."""
    
    print("\n" + "="*60)
    print("THE THEORY OF BEHAVIOR — BEHAVIORAL DECISION COMPUTATION")
    print("="*60)
    print(f"\nDecision Salience (D from Umwelt): {result['D']}")
    print("\n--- OPTION EVALUATION ---")

    for option in result['all_options']:
        print(f"\n  {option['name']}")
        print(f"  {'Attribute':<25} {'Type':<12} {'K':>5} {'S':>5} {'C':>5} {'Valence':>8}")
        print(f"  {'-'*62}")
        for attr in option['attributes']:
            print(f"  {attr['name']:<25} {attr['type']:<12} "
                  f"{attr['K']:>5} {attr['S']:>5} {attr['C']:>5} {attr['valence']:>8.4f}")
        print(f"  {'':25} {'R Total:':>18} {option['R']:>8.4f}")
        print(f"  {'':25} {'P Total:':>18} {option['P']:>8.4f}")
        print(f"  {'':25} {'B Value:':>18} {option['B']:>8.4f}")
        print(f"  {'':25} {'B* (x D):':>18} {option['B_star']:>8.4f}")

    print("\n--- BEHAVIORAL SELECTION ---")
    print(f"\n  Ranked options by B* value:")
    for i, option in enumerate(result['all_options']):
        marker = " <-- ENACTED" if i == 0 else ""
        print(f"  {i+1}. {option['name']:<20} B* = {option['B_star']:.4f}{marker}")

    if result['conflict']:
        print("\n  CONFLICT CONDITION DETECTED: Two or more options")
        print("  produce near-equal B* values — hesitation or")
        print("  ambivalence is predicted.")

    print(f"\n  ENACTED BEHAVIOR: {result['enacted']['name']}")
    print("="*60)


# ============================================================
# TEST SCENARIO: THE BONUS DECISION
# ============================================================

if __name__ == "__main__":

    # Decision salience from umwelt (D = 8/10)
    D = 0.8

    # Define behavioral options with attributes
    options = [
        {
            'name': 'Invest in CD',
            'attributes': [
                {'name': 'Security',       'K': 0.7, 'S': 0.4, 'C': 0.9, 'type': 'reward'},
                {'name': 'Return',         'K': 0.3, 'S': 0.8, 'C': 0.9, 'type': 'reward'},
                {'name': 'Extrinsic Value','K': 0.1, 'S': 0.1, 'C': 0.1, 'type': 'reward'},
            ]
        },
        {
            'name': 'Invest in Stock',
            'attributes': [
                {'name': 'Security',       'K': 0.3, 'S': 0.7, 'C': 0.3, 'type': 'reward'},
                {'name': 'Return',         'K': 0.6, 'S': 0.7, 'C': 0.4, 'type': 'reward'},
                {'name': 'Extrinsic Value','K': 0.7, 'S': 0.7, 'C': 0.2, 'type': 'reward'},
            ]
        },
        {
            'name': 'Buy New Car',
            'attributes': [
                {'name': 'Nicer Travel',      'K': 0.8, 'S': 0.7, 'C': 0.4, 'type': 'reward'},
                {'name': 'Impress Girlfriend','K': 0.8, 'S': 0.6, 'C': 0.3, 'type': 'reward'},
                {'name': 'Extrinsic Value',   'K': 0.8, 'S': 0.7, 'C': 0.7, 'type': 'reward'},
            ]
        },
        {
            'name': 'Do Nothing',
            'attributes': [
                {'name': 'Have Cash',      'K': 0.7, 'S': 0.9, 'C': 0.9, 'type': 'reward'},
            ]
        },
    ]

    # Run the algorithm
    result = select_behavior(options, D)

    # Display results
    print_results(result)

    # Example Bayesian update after buying the car
    # Suppose the car was less impressive to girlfriend than expected
    print("\n--- BAYESIAN UPDATE EXAMPLE ---")
    print("After buying the car, girlfriend less impressed than anticipated.")
    print("Contingency update for 'Impress Girlfriend' attribute:\n")
    
    updated = bayesian_update(
        K=0.8, S=0.6, C=0.3,
        outcome=0.6,
        reliability=0.1,  # girlfriend less impressed than expected
        importance=0.8,
        alpha=0.1
    )
    print(f"  Previous values: K=0.8, S=0.6, C=0.3")
    print(f"  Updated values:  K={updated['K']}, S={updated['S']}, C={updated['C']}")
    print(f"  Contingency dropped from 0.3 to {updated['C']} — next time")
    print(f"  'Impress Girlfriend' carries less behavioral force.")

Add python impletation.
