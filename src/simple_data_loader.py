"""
Simple data loader for Nevo cereal data
"""
import numpy as np
import pandas as pd
import pyblp

def load_nevo_data_simple():
    """Load and prepare Nevo cereal data for nested logit estimation."""

    # Load the raw data
    df = pd.read_csv(pyblp.data.NEVO_PRODUCTS_LOCATION)

    # Create nests based on mushy characteristic (1 = mushy, 0 = non-mushy)
    df['nest_id'] = df['mushy'].astype(int)

    # Calculate outside option share (assume market size is 1)
    market_shares_sum = df.groupby('market_ids')['shares'].sum()
    df = df.merge(
        market_shares_sum.rename('inside_share_total'),
        left_on='market_ids',
        right_index=True
    )
    df['outside_share'] = 1 - df['inside_share_total']

    # Calculate within-nest shares
    nest_shares = df.groupby(['market_ids', 'nest_id'])['shares'].sum()
    df = df.merge(
        nest_shares.rename('nest_share'),
        left_on=['market_ids', 'nest_id'],
        right_index=True
    )
    df['within_nest_share'] = df['shares'] / df['nest_share']

    # Create log differences for estimation
    df['log_share_diff'] = np.log(df['shares']) - np.log(df['outside_share'])
    df['log_within_share'] = np.log(df['within_nest_share'])

    return df