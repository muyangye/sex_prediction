import csv
totalMale = totalFemale = 0
charFreqs = {}

# Collect data from the csv traning set
with open('freqs.csv', newline='') as f:
    reader = csv.reader(f)
    for row in reader:
        # Skip the first line
        if (row[0] == 'char'): continue
        char = row[0]
        numMale = int(row[1])
        numFemale = int(row[2])
        charFreqs[char] = [numFemale, numMale]
        totalMale += numMale
        totalFemale += numFemale

# Collect data from the txt training set
lines = open('freqs.txt', encoding='utf-8').readlines()[1:]
for line in lines:
    line = line.strip().split(',')
    # Don't need id
    name = line[1]
    sex = line[2]
    if (sex == '1'): totalMale += 1
    else: totalFemale += 1
    for char in name:
        if (char not in charFreqs):
            charFreqs[char] = [0, 0]
        charFreqs[char][int(sex)] += 1

# charFreqs is essentially charProbabilities now
# charFreqs[char][0] = P(char|female), charFreqs[char][1] = P(char|male)
for char in charFreqs:
    # P(char|sex) = number of occurence of a char in a sex / total number of that sex
    charFreqs[char][0] /= totalFemale
    charFreqs[char][1] /= totalMale

while True:
    print('Please enter the name you want to predict(enter exit to exit): ')
    name = input()
    if (name == 'exit'):
        break
    # Suppose name = ABC
    # pTempMale = P(A|male) * P(B|male) * P(C|male), pTempFemale = P(A|female) * P(B|female) * P(C|female)
    pTempMale = pTempFemale = 1
    for char in name:
        # If the user inputs an invalid character
        if (char not in charFreqs):
            # Then simply predict without that character
            print("Sorry! [" + char + "] in the name you provided is not included in the training set! Only predicting based on rest of the characters!")
            continue
        pTempMale *= charFreqs[char][1]
        pTempFemale *= charFreqs[char][0]
    pMale = pTempMale * totalMale / (pTempMale * totalMale + pTempFemale * totalFemale)
    pFemale = pTempFemale * totalFemale / (pTempMale * totalMale + pTempFemale * totalFemale)
    print("Probability of Male: " + str(pMale*100) + '%')
    print("Probability of Female: " + str(pFemale*100) + '%')
    print('\n')