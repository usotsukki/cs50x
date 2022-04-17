from cs50 import get_string
# variables
sentences = 0
words = 1
characters = 0

# prompt input
text = get_string("Text: ")

# text analisys
for c in text:
    if c.isalpha():
        characters += 1
    elif c == ' ':
        words += 1
    elif (c == '.') or (c == "!") or (c == '?'):
        sentences += 1

# grade calculations
L = characters / words * 100
S = sentences / words * 100
index = round(0.0588 * L - 0.296 * S - 15.8)

# output
if index < 1:
    print("Before Grade 1")
elif index > 16:
    print("Grade 16+")
else:
    print(f"Grade {index}")