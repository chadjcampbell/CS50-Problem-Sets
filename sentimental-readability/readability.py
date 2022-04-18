from cs50 import get_string


def main():

    text = get_string("Text: ")

    lettercount = count_letters(text)

    wordcount = count_words(text)

    sentencecount = count_sentences(text)

    index = round(0.0588 * float((lettercount / wordcount) * 100) - 0.296 * float((sentencecount / wordcount) * 100) - 15.8)

    if index < 1:
        print("Before Grade 1")
    elif index > 16:
        print("Grade 16+")
    else:
        print(f"Grade {index}")


def count_letters(text):
    lettercount = 0
    for i in range(len(text)):
        if text[i].isalpha():
            lettercount += 1
    return lettercount


def count_words(text):
    wordcount = 1
    space = " "
    for i in range(len(text)):
        if text[i] == space:
            wordcount += 1
    return wordcount


def count_sentences(text):
    sentencecount = 0
    end1 = "."
    end2 = "!"
    end3 = "?"
    for i in range(len(text)):
        if text[i] == end1 or text[i] == end2 or text[i] == end3:
            sentencecount += 1
    return sentencecount


if __name__ == "__main__":
    main()