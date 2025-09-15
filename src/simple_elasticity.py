"""
Simple elasticity calculations for nested logit
"""

import numpy as np


def calculate_elasticities_simple(
    shares: np.ndarray, prices: np.ndarray, nest_ids: np.ndarray, alpha: float, sigma: float
) -> np.ndarray:
    """
    Calculate price elasticity matrix for nested logit model.

    Formulas:
    - Own-price: ε_jj = -α * p_j * [1/(1-σ) - (1-σ)*s_j - σ*s_j|g]
    - Cross-price within nest: ε_jk = α * p_k * [(1-σ)*s_k + σ*s_k|g]
    - Cross-price across nests: ε_jk = α * p_k * s_k
    """

    n_products = len(shares)
    elasticity = np.zeros((n_products, n_products))

    # Calculate within-nest shares
    within_shares = np.zeros(n_products)
    for nest in np.unique(nest_ids):
        nest_mask = nest_ids == nest
        nest_total = shares[nest_mask].sum()
        within_shares[nest_mask] = shares[nest_mask] / nest_total

    # Calculate elasticity matrix
    for j in range(n_products):
        for k in range(n_products):
            if j == k:
                # Own-price elasticity
                elasticity[j, k] = (
                    -alpha
                    * prices[j]
                    * (1 / (1 - sigma) - (1 - sigma) * shares[j] - sigma * within_shares[j])
                )
            else:
                # Cross-price elasticity
                if nest_ids[j] == nest_ids[k]:
                    # Within nest
                    elasticity[j, k] = (
                        alpha * prices[k] * ((1 - sigma) * shares[k] + sigma * within_shares[k])
                    )
                else:
                    # Across nests
                    elasticity[j, k] = alpha * prices[k] * shares[k]

    return elasticity
