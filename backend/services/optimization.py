import numpy as np

class MultiArmedBanditService:
    @staticmethod
    def thompson_sampling(variations):
        """
        Expects a list of dictionaries, each with 'id', 'clicks', and 'conversions' (or impressions).
        We'll treat 'clicks' as successes and 'total_views' as trials for CTR optimization.
        """
        sampled_values = []
        for v in variations:
            # Beta distribution parameters: alpha (successes + 1), beta (failures + 1)
            # Using 1 as a prior for a uniform distribution
            alpha = v.get('clicks', 0) + 1
            beta = (v.get('impressions', 100) - v.get('clicks', 0)) + 1
            
            # Ensure beta is at least 1
            beta = max(1, beta)
            
            sample = np.random.beta(alpha, beta)
            sampled_values.append((v['id'], sample))
            
        # Return the ID of the variation with the highest sampled value
        return max(sampled_values, key=lambda x: x[1])[0]

    @staticmethod
    def simulate_performance(variations):
        """
        Simulates some traffic and clicks to show the learning process.
        """
        # Assign hidden 'true' CTRs to variations for the simulation
        true_ctrs = {v['id']: np.random.uniform(0.01, 0.15) for v in variations}
        
        for v in variations:
            new_impressions = 100
            new_clicks = np.random.binomial(new_impressions, true_ctrs[v['id']])
            
            v['clicks'] = v.get('clicks', 0) + new_clicks
            v['impressions'] = v.get('impressions', 0) + new_impressions
            
        return variations

