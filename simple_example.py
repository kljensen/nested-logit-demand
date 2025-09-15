#!/usr/bin/env python
"""
Simple Nested Logit Example with Nevo Cereal Data
"""

import numpy as np

from src.simple_data_loader import load_nevo_data_simple
from src.simple_elasticity import calculate_elasticities_simple
from src.simple_estimation import estimate_nested_logit_simple


def main() -> None:
    print("=" * 70)
    print("NESTED LOGIT DEMAND ESTIMATION - NEVO CEREAL DATA")
    print("=" * 70)

    # Step 1: Load data
    print("\n1. Loading Nevo cereal data...")
    df = load_nevo_data_simple()
    print(f"   - Loaded {len(df)} observations")
    print(f"   - Markets: {df['market_ids'].nunique()}")
    print(f"   - Products: {df['product_ids'].nunique()}")
    print("   - Nests: 2 (mushy vs non-mushy cereals)")

    # Step 2: Estimate model
    print("\n2. Estimating nested logit model (OLS)...")
    product_chars = ["sugar"]  # Just use sugar as characteristic

    results = estimate_nested_logit_simple(data=df, product_chars=product_chars)

    # Step 3: Display results
    print("\n3. ESTIMATION RESULTS:")
    print("-" * 50)
    print(f"   Sample size: {results.n_obs} observations")
    print(f"   R-squared:   {results.r_squared:.4f}")
    print()
    print(f"   Price coefficient (α):  {results.alpha:7.4f}  (SE: {results.alpha_se:.4f})")
    print(f"   Nesting parameter (σ):  {results.sigma:7.4f}  (SE: {results.sigma_se:.4f})")
    print()
    print("   Product characteristics:")
    for char, coef in results.beta.items():
        se = results.beta_se.get(char, 0)
        print(f"     {char:10s}: {coef:7.4f}  (SE: {se:.4f})")

    # Step 4: Interpret results
    print("\n4. INTERPRETATION:")
    print("-" * 50)

    if results.alpha > 0:
        print(f"   ✓ Price coefficient is negative in demand (α = -{results.alpha:.4f})")
        print("     (We entered -price in regression, so positive coef means negative effect)")
    else:
        print("   ⚠ Warning: Unexpected price coefficient sign")

    if 0 < results.sigma < 1:
        print(f"   ✓ Nesting parameter σ = {results.sigma:.3f} is in valid range (0,1)")
        print("     Products within nests are closer substitutes")
    elif results.sigma <= 0:
        print("   ⚠ σ ≤ 0: Model reduces to simple logit")
    else:
        print("   ⚠ σ > 1: Nesting parameter outside valid range")

    # Step 5: Calculate elasticities for first market
    print("\n5. ELASTICITY ANALYSIS (First Market):")
    print("-" * 50)

    # Get first market data
    market_1 = df[df["market_ids"] == df["market_ids"].iloc[0]].copy()

    elasticity_matrix = calculate_elasticities_simple(
        shares=market_1["shares"].values,
        prices=market_1["prices"].values,
        nest_ids=market_1["nest_id"].values,
        alpha=results.alpha,
        sigma=results.sigma,
    )

    # Own-price elasticities
    own_elasticities = np.diag(elasticity_matrix)
    print("   Own-price elasticities (first 5 products):")
    for i in range(min(5, len(own_elasticities))):
        print(f"     Product {i + 1}: {own_elasticities[i]:7.4f}")

    print("\n   Summary statistics:")
    print(f"     Mean own-price elasticity: {own_elasticities.mean():7.4f}")
    print(f"     Min:  {own_elasticities.min():7.4f}")
    print(f"     Max:  {own_elasticities.max():7.4f}")

    # Check substitution patterns
    print("\n   Substitution patterns (Product 1 to others):")
    for j in range(1, min(5, len(market_1))):
        within_nest = market_1.iloc[0]["nest_id"] == market_1.iloc[j]["nest_id"]
        elast = elasticity_matrix[0, j]
        nest_type = "same nest" if within_nest else "different nest"
        print(f"     To Product {j + 1} ({nest_type}): {elast:7.5f}")

    print("\n" + "=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
