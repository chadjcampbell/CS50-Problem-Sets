import csv
import sys


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: python dna.py data.csv sequence.txt")

    # Read database file into a list of dictionaries
    data = []
    with open(sys.argv[1], "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    # Change STR counts to ints for comparison later
    for person in data:
        for STR in person:
            if person[STR].isdigit():
                person[STR] = int(person[STR])

    # Read DNA sequence file into a string variable
    with open(sys.argv[2], "r") as file:
        sequence = file.read()

    # Iterate through each persons STR count to see if it matches
    for person in data:
        match = 0
        for STR in person:
            if longest_match(sequence, STR) == person[STR]:
                match += 1

        # If all STR's match, print match
        if match == len(person) - 1:
            print(person["name"])
            return

    # If there are no matches, end
    print("No Match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
