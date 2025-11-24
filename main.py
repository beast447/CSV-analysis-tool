import pandas as pd
import re
from collections import Counter
import sys

# 1. Load your CSV --------------------------
df = pd.read_csv(sys.argv[1])

# 2. Select the key columns -----------------

text_col = 'In as much detail as you would like, please explain why you are, or are not interested in extending or re-enlisting.'
intent_col = 'Would you be interested in extending or re-enlisting?'

df = df[[intent_col, text_col]].dropna()

# 3. Simple preprocessing + keyword extraction
def extract_keywords(subset):
    all_text = " ".join(subset[text_col].astype(str))

    # basic tokenizer
    words = re.findall(r"[A-Za-z']+", all_text.lower())

    # remove filler words / stopwords
    stopwords = {
        "the","and","to","a","of","in","is","for","it","that","on","my",
        "with","as","be","have","i","me","so","but","are","not","or","at",
        "if","im","id","ill","we","you","your","our","they","them","their","interested",
        "am", "m", "want","because", "re", "a", "will", "like", "t", "guard", "would", "get",
        "years"
    }

    words = [w for w in words if w not in stopwords]

    return Counter(words).most_common(50)

# 4. Split into YES (reenlisting) and NO (getting out) groups
yes_reasons = df[df[intent_col] == "Yes"]
no_reasons = df[df[intent_col] == "No"]

# 5. Extract top keywords
top_yes = extract_keywords(yes_reasons)
top_no = extract_keywords(no_reasons)

# 6. Show the top 5 for each group
print("Top 5 Reenlisting Reasons (Yes):")
print(top_yes[:5])
print("\nTop 5 Getting Out Reasons (No):")
print(top_no[:5])
