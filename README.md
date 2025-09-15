# Nested Logit Demand Estimation

A simplified Python implementation of nested logit demand estimation using Nevo's cereal dataset with exogenous prices.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd nested-logit-demand

# Install dependencies using uv
uv sync

# Run the example
uv run python simple_example.py
```

## Project Structure

```
├── simple_example.py           # Main example demonstrating the model
├── src/
│   ├── simple_data_loader.py   # Loads and prepares Nevo cereal data
│   ├── simple_estimation.py    # OLS estimation of nested logit
│   └── simple_elasticity.py    # Price elasticity calculations
└── pyproject.toml              # Project dependencies (managed by uv)
```

## Model Overview

The nested logit model relaxes the restrictive Independence of Irrelevant Alternatives (IIA) assumption of simple logit by grouping products into "nests". Products within the same nest are closer substitutes than products across nests.

### Estimation Equation (Berry 1994)

```
ln(s_j) - ln(s_0) = X_j'β - α*price_j + σ*ln(s_j|g) + ε_j
```

Where:
- `s_j`: market share of product j
- `s_0`: outside option share
- `X_j`: product characteristics
- `price_j`: product price
- `s_j|g`: within-nest share
- `α`: price coefficient
- `σ`: nesting parameter (0 = simple logit, 1 = perfect correlation within nest)
- `β`: characteristic coefficients

### Data

Uses Nevo's cereal dataset from PyBLP:
- **Time period**: 1988-1992
- **Markets**: 94 city-quarter combinations
- **Products**: 24 cereal brands
- **Nesting**: Mushy vs non-mushy cereals

## Results

Running `simple_example.py` produces:

```
ESTIMATION RESULTS:
   Price coefficient (α):   1.5509  (SE: 0.4670)
   Nesting parameter (σ):   0.8938  (SE: 0.0114)

   Product characteristics:
     sugar: 0.0049  (SE: 0.0023)

ELASTICITY ANALYSIS:
   Mean own-price elasticity: -1.9087
   Within-nest substitution is ~8x stronger than across-nest
```

### Interpretation

- **Price coefficient**: α = 1.55 implies negative price effect on demand (we use -price in regression)
- **Nesting parameter**: σ = 0.89 indicates strong within-nest correlation
- **Elasticities**: Own-price elasticities range from -1.0 to -2.6 (elastic demand)
- **Substitution patterns**: Consumers are much more likely to substitute within mushy/non-mushy categories

## Dependencies

- `numpy`: Numerical computations
- `pandas`: Data manipulation
- `scipy`: Statistical functions
- `statsmodels`: OLS regression
- `pyblp`: Source of Nevo cereal data

## References

- Berry, S. (1994). "Estimating Discrete-Choice Models of Product Differentiation." RAND Journal of Economics.
- Nevo, A. (2000). "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand." Journal of Economics & Management Strategy.