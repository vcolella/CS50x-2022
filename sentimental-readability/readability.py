# Implents readability.c in python

def count_words(text):
    # Counts words in string
    return len(text.split())


def count_letters(text):
    # Counts letters in string
    letters = 0
    for c in text:
        if c.isalpha():
            letters += 1
    return letters


def count_sentences(text):
    # Counts sentences in text
    sentences = 0

    for c in text:
        if c == '.' or c == '!' or c == '?':
            sentences += 1

    return sentences
    

def index(text):
    # Calculates index using Coleman-Liau Formula
    words = count_words(text)
    L = count_letters(text) / words * 100
    S = count_sentences(text) / words * 100

    return 0.0588 * L - 0.296 * S - 15.8


def main():
    text = input("Text: ")

    # Get index using Coleman-Liau Formula
    i = index(text)

    if i < 1:
        print("Before Grade 1")
    elif i >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {round(i)}")


if __name__ == "__main__":
    main()