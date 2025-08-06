# analysis/thresholds.py

def get_safe_limit(rpm):
    """
    Dynamically computes the safe temperature limit for a given RPM.
    Ensures that as RPM increases, so does the thermal threshold.
    Compatible with synthetic data and real-world scaling.

    For example:
    - At 1000 RPM → Safe limit = 40°C
    - At 3000 RPM → Safe limit = 60°C
    - At 4000 RPM → Safe limit = 70°C
    """
    return 0.01 * rpm + 30


