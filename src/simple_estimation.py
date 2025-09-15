"""
Simple nested logit estimation with OLS
"""

from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm  # type: ignore[import-untyped]


@dataclass
class NestedLogitResults:
    """Results from nested logit estimation."""

    alpha: float  # Price coefficient
    sigma: float  # Nesting parameter
    beta: dict[str, float]  # Product characteristic coefficients
    alpha_se: float  # Standard error for alpha
    sigma_se: float  # Standard error for sigma
    beta_se: dict[str, float]  # Standard errors for beta
    r_squared: float
    n_obs: int


def estimate_nested_logit_simple(
    data: pd.DataFrame,
    product_chars: list[str],
) -> NestedLogitResults:
    """
    Estimate nested logit model using OLS.

    Estimating equation (Berry 1994):
    ln(s_j) - ln(s_0) = X_j'β - α*price_j + σ*ln(s_j|g) + ε_j
    """

    # Prepare dependent variable
    y = data["log_share_diff"].values

    # Prepare independent variables
    X_list = []
    var_names = []

    # Add product characteristics
    for char in product_chars:
        X_list.append(data[char].values)
        var_names.append(char)

    # Add price (negative of price for intuitive alpha)
    X_list.append(-data["prices"].values)  # type: ignore[operator]
    var_names.append("price")

    # Add log within-nest share
    X_list.append(data["log_within_share"].values)
    var_names.append("sigma")

    # Stack into matrix and add constant
    X = np.column_stack(X_list)  # type: ignore[arg-type]
    X = sm.add_constant(X)
    var_names = ["const"] + var_names

    # Run OLS regression
    model = sm.OLS(y, X)
    results = model.fit(cov_type="HC1")  # Heteroskedasticity-robust SEs

    # Extract coefficients and standard errors
    params = results.params
    se = results.bse

    # Parse results
    beta = {}
    beta_se = {}

    for i, name in enumerate(var_names):
        if name == "price":
            alpha = params[i]
            alpha_se = se[i]
        elif name == "sigma":
            sigma = params[i]
            sigma_se = se[i]
        elif name != "const":
            beta[name] = params[i]
            beta_se[name] = se[i]

    return NestedLogitResults(
        alpha=alpha,
        sigma=sigma,
        beta=beta,
        alpha_se=alpha_se,
        sigma_se=sigma_se,
        beta_se=beta_se,
        r_squared=results.rsquared,
        n_obs=len(y),
    )
