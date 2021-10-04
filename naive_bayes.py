lines = open('train.txt', encoding='utf-8').readlines()[1:]
totalMale = totalFemale = 0
characterToSex = {}
for line in lines:
    # Don't need id
    line = line.strip().split(',')
    characters = line[1]
    sex = line[2]
    if (sex == '1'):
        totalMale += 1
    else:
        totalFemale += 1
    for character in characters:
        if (character not in characterToSex):
            characterToSex[character] = {}
        if (sex not in characterToSex[character]):
            characterToSex[character]['1'] = 0
            characterToSex[character]['0'] = 0
        characterToSex[character][sex] += 1
total = totalMale + totalFemale

# We need to calculate P(sex|char)
# Bayes' Theorem tells us that P(sex|char) = P(char|sex) * P(sex) / P(char)
# Note P(char|sex) = number of char in a specific sex / total number of that sex
# And that P(sex) = total number of that sex / total number of all sex
# So P(char|sex) * P(sex) = number of char in a specific sex / total number of all sex

while True:
    print('Please enter the name you want to predict(enter exit to exit): ')
    name = input()
    if (name == 'exit'):
        break
    maleProb = totalMale / total
    femaleProb = totalFemale / total
    # Naive Bayes assumes that events are conditionally independent with respect to the outcome. i.e. P(abc|sex) = P(a|sex) * P(b|sex) * P(c|sex)
    # Naive Bayes also assumes that events are independent themselves. i.e. P(abc) = P(a) * P(b) * P(c)
    # Finally, by Bayes' Theorem, P(sex|abc) = P(abc|sex) * P(sex) / P(abc) = P(a|sex) * P(b|sex) * P(c|sex) * P(sex) / [P(a) * P(b) * P(c)]
    # Proved in line 25, P(char|sex) * P(sex) = number of char in a specific sex / total number of all sex. And P(a) = P(b) = P(c) = 1 / number of all chars
    for char in name:
        if (char not in characterToSex):
            print("Sorry! One character in the name you provided is not included in the training set!")
            quit()
        maleProb *= characterToSex[char]['1'] / totalMale * len(characterToSex)
        femaleProb *= characterToSex[char]['0'] / totalFemale * len(characterToSex)
    # normalization so that probabilities add up to 1
    # Actually with normalization, we don't need to * len(characterToSex) every time. But leave it there as it is more direct
    finalMaleProb = maleProb / (maleProb + femaleProb) 
    finalFemaleProb = femaleProb / (maleProb + femaleProb)
    print('The chance that guy is male is: ' + str(finalMaleProb*100) + '%')
    print('The chance that guy is female is: ' + str(finalFemaleProb*100) + '%')