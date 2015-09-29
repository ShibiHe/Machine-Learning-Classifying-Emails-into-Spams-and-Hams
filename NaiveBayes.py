__author__ = 'frankhe'
import csv

total_success = 0
total_email = 0


def read_csv(name):
    f = open(name)
    reader = csv.reader(f)
    distribution = [int(x) for x in list(reader)[0]]
    return distribution


def calc_probability(distribution):
    """laplace smoothing using K"""
    K = 1
    CATEGORY = len(distribution)
    N = 0
    for count in distribution:
        N += count
    probability_distribution = []
    for count in distribution:
        probability_distribution.append(float((count + K)) / float(N + K * CATEGORY))
    return probability_distribution


def test(data_name, p_ham, p_spam, result_is_spam=True):
    f = open(data_name)
    guess_successfully = 0
    email_id = 0
    p_is_spam = 0
    p_is_ham = 0
    for line in f.readlines():
        data = [int(x) for x in line.split()]
        data[1] -= 1    # 1-77386 -> 0-77385
        if data[0]==email_id:
            p_is_spam += p_spam[data[1]] * data[2]
            p_is_ham += p_ham[data[1]] * data[2]
        else:
            email_id = data[0]
            if email_id==1:
                continue
            if p_is_spam>p_is_ham:
                guess_is_spam = True
            else:
                guess_is_spam = False
            if guess_is_spam==result_is_spam:
                guess_successfully += 1
            p_is_ham = 0
            p_is_spam = 0
    global total_success
    global total_email
    total_success += guess_successfully
    total_email += email_id
    print "test result for ", data_name
    print guess_successfully, ' / ', email_id

hamDistribution = read_csv("ham_train.csv")
spamDistribution = read_csv("spam_train.csv")
p_spam = calc_probability(spamDistribution)
p_ham = calc_probability(hamDistribution)

# module 1: TEST
test("spam_test.txt", p_ham, p_spam)
test("ham_test.txt", p_ham, p_spam, False)
print "accuracy:", float(total_success)/total_email

# module 2: LIST MOST IMPORTANT WORDS
p_ratio_spam = [x / y for x,y in zip(p_spam, p_ham)]
p_ratio_spam = list(enumerate(p_ratio_spam))
p_ratio_spam = sorted(p_ratio_spam, key=lambda x: x[1], reverse=True)
# print '\n',p_ratio_spam[:10]
p_ratio_ham = [y / x for x,y in zip(p_spam, p_ham)]
p_ratio_ham = list(enumerate(p_ratio_ham))
p_ratio_ham = sorted(p_ratio_ham, key=lambda x: x[1], reverse=True)
# print '\n',p_ratio_ham[:10]

# module 3: PRINT IMPORTANT WORDS
f = open("The_most_important_words.txt",mode='w')
number_of_important_words = 1200
words=set()
for i in range(number_of_important_words/2):
    f.write(str(p_ratio_spam[i][0]) + ' ')
    words.add(p_ratio_spam[i][0])
for i in range(number_of_important_words):
    f.write(str(p_ratio_ham[i][0]) + ' ')
    words.add(p_ratio_ham[i][0])
# print len(words)
