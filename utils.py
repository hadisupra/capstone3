import pandas as pd
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter

#from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter
#from langchain.text_splitters import RecursiveCharacterTextSplitter
MAX_TOKENS = 4096

df = pd.read_csv("RESUME.csv",dtype=str,nrows=500)
print(df.columns)
df.info()
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]
print(df.columns)

# Preprocess the DataFrame
# Combine relevant columns into a single text column

df["Text"] = df[["Resume_str", "Category"]].fillna("").agg(" ".join, axis=1)
# tokenizer for OpenAI models
enc = tiktoken.get_encoding("cl100k_base")
df["token_count"] = df["Text"].apply(lambda x: len(enc.encode(x)))
df_filtered = df[df["token_count"] <= MAX_TOKENS].reset_index(drop=True)

def count_tokens(text):
    import tiktoken
    enc = tiktoken.get_encoding("cl100k_base")
    return len(enc.encode(text))

def batch_by_token(df, max_total_tokens):
    batches = []
    current_batch = []
    current_tokens = 0

    for _, row in df.iterrows():
        if current_tokens + row["token_count"] > max_total_tokens:
            batches.append(current_batch)
            current_batch = [row]
            current_tokens = row["token_count"]
        else:
            current_batch.append(row)
            current_tokens += row["token_count"]

    if current_batch:
        batches.append(current_batch)

    return [pd.DataFrame(batch) for batch in batches]

# batches = batch_by_token(df_filtered, 280000)

# import matplotlib.pyplot as plt
# df["token_count"].hist(bins=50)
# plt.title("Token Count Distribution")
# plt.xlabel("Tokens")
# plt.ylabel("Rows")
# plt.show()

def load_and_chunk_csv(path, chunk_size=100):
    df = df_filtered.copy()
    df["Text"] = df[["Resume_str", "Category"]].fillna("").agg(" ".join, axis=1)
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=10)
    chunk_size=500,
    chunk_overlap=50,
    separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]

    chunks = splitter.split_text("\n".join(df["Text"].tolist()))
    return chunks



