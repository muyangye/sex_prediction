import csv

# Read data
def read_data():
    total_male = total_female = 0
    char_freqs = {}

    # Collect data from the csv traning set
    with open("freqs.csv", encoding="utf-8", newline="") as f:
        reader = csv.reader(f)
        # Skip the first line
        next(reader)
        for row in reader:
            char = row[0]
            num_male = int(row[1])
            num_female = int(row[2])
            char_freqs[char] = [num_female, num_male]
            total_male += num_male
            total_female += num_female

    # Collect data from the txt training set
    lines = open("freqs.txt", encoding="utf_8").readlines()[1:]
    for line in lines:
        line = line.strip().split(",")
        # Don"t need id
        name = line[1]
        sex = line[2]
        if (sex == "1"): total_male += 1
        else: total_female += 1
        for char in name:
            if (char not in char_freqs):
                char_freqs[char] = [0, 0]
            char_freqs[char][int(sex)] += 1
    
    return (total_male, total_female, char_freqs)


# Naive Bayes logic
def main():
    total_male, total_female, char_freqs = read_data()
    # char_freqs is essentially char_probabilities now
    # char_freqs[char][0] = P(char|female), char_freqs[char][1] = P(char|male)
    for char in char_freqs:
        # P(char|sex) = number of occurence of a char in a sex / total number of that sex
        char_freqs[char][0] /= total_female
        char_freqs[char][1] /= total_male

    while True:
        print("Please enter the name you want to predict(enter exit to exit): ")
        name = input()
        if (name == "exit"):
            break
        # Suppose name = ABC
        # p_temp_male = P(A|male) * P(B|male) * P(C|male), p_temp_female = P(A|female) * P(B|female) * P(C|female)
        p_temp_male = p_temp_female = 1
        for char in name:
            # If the user inputs an invalid character
            if (char not in char_freqs):
                # Then simply predict without that character
                print("Sorry! [" + char + "] in the name you provided is not included in the training set! Only predicting based on rest of the characters!")
                continue
            p_temp_male *= char_freqs[char][1]
            p_temp_female *= char_freqs[char][0]
        p_male = p_temp_male * total_male / (p_temp_male * total_male + p_temp_female * total_female)
        p_female = p_temp_female * total_female / (p_temp_male * total_male + p_temp_female * total_female)
        print("Probability of Male: " + str(p_male*100) + "%")
        print("Probability of Female: " + str(p_female*100) + "%")
        print("\n")


if __name__ == "__main__":
    main()