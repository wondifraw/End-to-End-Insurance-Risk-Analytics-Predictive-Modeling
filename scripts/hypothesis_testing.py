from src.preprocessor import Preprocessor
from src.stat_tests import run_all_hypothesis_tests

# Load data
file_path = "../data/MachineLearningRating_v3.txt"
preprocessor = Preprocessor(file_path)
preprocessor.load_data()
df = preprocessor.df

# Run hypothesis tests
results = run_all_hypothesis_tests(df)

# Print report
for key, res in results.items():
    stat, p, groups = res['stat'], res['p'], res['groups']
    if p < 0.05:
        interpretation = f"We reject the null hypothesis for {key.replace('_', ' ')} (p = {p:.4f}). "
        recommendation = f"Business recommendation: Consider segmentation or pricing adjustment between {groups[0]} and {groups[1]}."
    else:
        interpretation = f"We fail to reject the null hypothesis for {key.replace('_', ' ')} (p = {p:.4f}). "
        recommendation = f"Business recommendation: No evidence for segmentation between {groups[0]} and {groups[1]}."
    print(f"{key}:\n  {interpretation}\n  {recommendation}\n") 