import re
from embedder import most_similar

MEMORY_FILE = "memory.txt"


# -------------------------
# Load memory
# -------------------------
def load_memory():
    data = []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                match = re.search(r"word=(.*?) \| latin=(.*?) \| .*meaning=(.*?) \|", line)
                if match:
                    word = match.group(1)
                    latin = match.group(2)
                    meaning = match.group(3)

                    data.append((word, latin, meaning))
    except FileNotFoundError:
        open(MEMORY_FILE, "w").close()

    return data


# -------------------------
# Save new knowledge
# -------------------------
def save_entry(word, latin, meaning, synonyms=""):
    with open(MEMORY_FILE, "a", encoding="utf-8") as f:
        f.write(
            f"\nword={word} | latin={latin} | type=unknown | "
            f"meaning={meaning} | synonyms={synonyms} | confidence=1.0\n"
        )


# -------------------------
# Search exact match
# -------------------------
def exact_search(word, data):
    for w, latin, meaning in data:
        if w.lower() == word.lower():
            return latin, meaning
    return None


# -------------------------
# Main translator
# -------------------------
def translate(word, data):
    result = exact_search(word, data)

    if result:
        return result

    # fallback semantic suggestion
    best, score = most_similar(word, data)

    if best:
        print(f"\n[AI suggestion] {best[1]} (confidence: {score:.2f})")
        confirm = input("Accept? (y/n): ")

        if confirm.lower() == "y":
            return best[1], best[2]

    return None


# -------------------------
# CLI
# -------------------------
def main():
    print("Latin Translator (local AI + memory.txt)")
    print("Type 'exit' to quit.\n")

    while True:
        word = input("Translate English word: ").strip()

        if word.lower() == "exit":
            break

        data = load_memory()
        result = translate(word, data)

        if result:
            latin, meaning = result
            print(f"\n→ Latin: {latin}")
            print(f"→ Meaning: {meaning}\n")

        else:
            print("\nNo result found.")
            latin = input("Enter Latin translation: ")
            meaning = input("Enter meaning: ")
            synonyms = input("Enter synonyms (optional): ")

            save_entry(word, latin, meaning, synonyms)

            print("Saved to memory.txt\n")


if __name__ == "__main__":
    main()