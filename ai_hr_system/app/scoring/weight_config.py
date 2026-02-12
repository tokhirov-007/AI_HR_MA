"""
Configuration for how different aspects of the interview are weighted 
based on question difficulty.
"""

# Weight mapping: (Knowledge, Honesty, Time, Problem Solving)
# sum should be 1.0

WEIGHT_CONFIG = {
    "easy": {
        "knowledge": 0.3,
        "honesty": 0.4,
        "time": 0.3,
        "problem_solving": 0.0
    },
    "medium": {
        "knowledge": 0.4,
        "honesty": 0.3,
        "time": 0.2,
        "problem_solving": 0.1
    },
    "hard": {
        "knowledge": 0.5,
        "honesty": 0.2,
        "time": 0.0,
        "problem_solving": 0.3
    }
}

def get_weights(difficulty: str) -> dict:
    """Return weights for a specific difficulty level"""
    return WEIGHT_CONFIG.get(difficulty.lower(), WEIGHT_CONFIG["medium"])
