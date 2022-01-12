from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from fuzzywuzzy import fuzz
import pandas as pd
import reviewsInitialize

reviews = reviewsInitialize.getReviews()
bubbles = reviewsInitialize.getBubbles()

# Lists initialization
# TODO: check if I don't need to use user_reviews/user_bubbles lists **

user_reviews = list()
user_bubbles = list()
sentiment_score = list()
program_feedback = list()

# counters for results

count_aperfect = 0
count_perfect = 0
count_fairenough = 0
count_manythings = 0
count_disaster = 0

# counters for bubbles with specific comment
# counters for 1-5 bubbles with comment 'ABSOLUTELY PERFECT'
count_fiveb_with_ap = count_fourb_with_ap = count_threeb_with_ap = count_twob_with_ap = count_oneb_with_ap = 0
# counters for 1-5 bubbles with comment 'PERFECT'
count_fiveb_with_p = count_fourb_with_p = count_threeb_with_p = count_twob_with_p = count_oneb_with_p = 0
# counters for 1-5 bubbles with comment 'FAIR ENOUGH'
count_fiveb_with_fe = count_fourb_with_fe = count_threeb_with_fe = count_twob_with_fe = count_oneb_with_fe = 0
# counters for 1-5 bubbles with comment 'MANY THINGS NEEDS TO GET BETTER'
count_fiveb_with_mt = count_fourb_with_mt = count_threeb_with_mt = count_twob_with_mt = count_oneb_with_mt = 0
# counters for 1-5 bubbles with comment 'DISASTER'
count_fiveb_with_ds = count_fourb_with_ds = count_threeb_with_ds = count_twob_with_ds = count_oneb_with_ds = 0

# Global variables initialization
pfinalfive_aperfect = pfinalfour_aperfect = pfinalthree_aperfect = pfinaltwo_aperfect = pfinalone_aperfect = 0
pfinalfive_perfect = pfinalfour_perfect = pfinalthree_perfect = pfinaltwo_perfect = pfinalone_perfect = 0
pfinalfive_fe = pfinalfour_fe = pfinalthree_fe = pfinaltwo_fe = pfinalone_fe = 0
pfinalfive_many = pfinalfour_many = pfinalthree_many = pfinaltwo_many = pfinalone_many = 0
pfinalfive_ds = pfinalfour_ds = pfinalthree_ds = pfinaltwo_ds = pfinalone_ds = 0

# we don't actually need a separated counter for bubbles/results since every result got a bubble
# so it's the same total number
count_total = 0

# the line below fills user_reviews and removes the brackets,single quotes,double quotes
# reviews counter
counter_reviews = 0
for k in reviews:
    user_reviews.append(*k)
    counter_reviews += 1

# fill in sentiment_score array

for s in range(len(reviews)):
    sent_vader = list(SentimentIntensityAnalyzer().polarity_scores(reviews[s]).values())
    sentiment_score.append(sent_vader[3])

# getting positive or negative depending from sentiment_score[i]

for j in range(len(sentiment_score)):
    if sentiment_score[j] >= 0.70:
        program_feedback.append("ABSOLUTELY PERFECT")
        count_aperfect += 1
    elif 0.70 > sentiment_score[j] >= 0.40:
        program_feedback.append("PERFECT")
        count_perfect += 1
    elif 0.40 > sentiment_score[j] >= 0.1:
        program_feedback.append("FAIR ENOUGH")
        count_fairenough += 1
    elif 0.1 > sentiment_score[j] >= -0.4:
        program_feedback.append("MANY THINGS NEEDS TO GET BETTER")
        count_manythings += 1
    else:
        program_feedback.append("DISASTER")
        count_disaster += 1
    count_total += 1

# get the first character of Rating column and fill bubbles_array

for i in range(len(bubbles)):
    first_num = bubbles[i][0]
    user_bubbles.append(first_num[0])
    if program_feedback[i] == 'ABSOLUTELY PERFECT':
        if user_bubbles[i] == '5':
            count_fiveb_with_ap += 1
        elif user_bubbles[i] == '4':
            count_fourb_with_ap += 1
        elif user_bubbles[i] == '3':
            count_threeb_with_ap += 1
        elif user_bubbles[i] == '2':
            count_twob_with_ap += 1
        else:
            count_oneb_with_ap += 1
    elif program_feedback[i] == 'PERFECT':
        if user_bubbles[i] == '5':
            count_fiveb_with_p += 1
        elif user_bubbles[i] == '4':
            count_fourb_with_p += 1
        elif user_bubbles[i] == '3':
            count_threeb_with_p += 1
        elif user_bubbles[i] == '2':
            count_twob_with_p += 1
        else:
            count_oneb_with_p += 1
    elif program_feedback[i] == 'FAIR ENOUGH':
        if user_bubbles[i] == '5':
            count_fiveb_with_fe += 1
        elif user_bubbles[i] == '4':
            count_fourb_with_fe += 1
        elif user_bubbles[i] == '3':
            count_threeb_with_fe += 1
        elif user_bubbles[i] == '2':
            count_twob_with_fe += 1
        else:
            count_oneb_with_fe += 1
    elif program_feedback[i] == 'MANY THINGS NEEDS TO GET BETTER':
        if user_bubbles[i] == '5':
            count_fiveb_with_mt += 1
        elif user_bubbles[i] == '4':
            count_fourb_with_mt += 1
        elif user_bubbles[i] == '3':
            count_threeb_with_mt += 1
        elif user_bubbles[i] == '2':
            count_twob_with_mt += 1
        else:
            count_oneb_with_mt += 1
    else:
        if user_bubbles[i] == '5':
            count_fiveb_with_ds += 1
        elif user_bubbles[i] == '4':
            count_fourb_with_ds += 1
        elif user_bubbles[i] == '3':
            count_threeb_with_ds += 1
        elif user_bubbles[i] == '2':
            count_twob_with_ds += 1
        else:
            count_oneb_with_ds += 1

dataFrame = {'Review': user_reviews,
             'Score': sentiment_score,
             'Bubbles': user_bubbles,
             'Result': program_feedback,}


df = pd.DataFrame(data=dataFrame)
df.to_excel("output.xlsx",sheet_name='Sentiment Analysis')

def calculateAndPrint():
    # Bayes theorem
    # In my set of reviews,a result is chosen.What is the probability of
    # of bubble being '5' given the result is 'ABSOLUTELY PERFECT'
    # What is the probability of bubble being '4' given the result is 'ABSOLUTELY PERFECT'
    # etc, etc.

    # Probabilities of bubbles given the result is 'ABSOLUTELY PERFECT'
    global pfinalfive_aperfect, pfinalfour_aperfect, pfinalthree_aperfect, pfinaltwo_aperfect, pfinalone_aperfect
    global pfinalfive_perfect, pfinalfour_perfect, pfinalthree_perfect, pfinaltwo_perfect, pfinalone_perfect
    global pfinalfive_fe, pfinalfour_fe, pfinalthree_fe, pfinaltwo_fe, pfinalone_fe
    global pfinalfive_many, pfinalfour_many, pfinalthree_many, pfinaltwo_many, pfinalone_many
    global pfinalfive_ds, pfinalfour_ds, pfinalthree_ds, pfinaltwo_ds, pfinalone_ds

    pfinalfive_aperfect = (count_fiveb_with_ap / count_aperfect) * 100
    pfinalfour_aperfect = (count_fourb_with_ap / count_aperfect) * 100
    pfinalthree_aperfect = (count_threeb_with_ap / count_aperfect) * 100
    pfinaltwo_aperfect = (count_twob_with_ap / count_aperfect) * 100
    pfinalone_aperfect = (count_oneb_with_ap / count_aperfect) * 100

    # Probabilities of bubbles given the result is 'PERFECT'

    pfinalfive_perfect = (count_fiveb_with_p / count_perfect) * 100
    pfinalfour_perfect = (count_fourb_with_p / count_perfect) * 100
    pfinalthree_perfect = (count_threeb_with_p / count_perfect) * 100
    pfinaltwo_perfect = (count_twob_with_p / count_perfect) * 100
    pfinalone_perfect = (count_oneb_with_p / count_perfect) * 100

    # Probabilities of bubbles given the result is 'FAIR ENOUGH'

    pfinalfive_fe = (count_fiveb_with_fe / count_fairenough) * 100
    pfinalfour_fe = (count_fourb_with_fe / count_fairenough) * 100
    pfinalthree_fe = (count_threeb_with_fe / count_fairenough) * 100
    pfinaltwo_fe = (count_twob_with_fe / count_fairenough) * 100
    pfinalone_fe = (count_oneb_with_fe / count_fairenough) * 100

    # Probabilities of bubbles given the result is 'MANY THINGS NEEDS TO GET BETTER'

    pfinalfive_many = (count_fiveb_with_mt / count_manythings) * 100
    pfinalfour_many = (count_fourb_with_mt / count_manythings) * 100
    pfinalthree_many = (count_threeb_with_mt / count_manythings) * 100
    pfinaltwo_many = (count_twob_with_mt / count_manythings) * 100
    pfinalone_many = (count_oneb_with_mt / count_manythings) * 100

    # Probabilities of bubbles given the result is 'DISASTER'

    pfinalfive_ds = (count_fiveb_with_ds / count_disaster) * 100
    pfinalfour_ds = (count_fourb_with_ds / count_disaster) * 100
    pfinalthree_ds = (count_threeb_with_ds / count_disaster) * 100
    pfinaltwo_ds = (count_twob_with_ds / count_disaster) * 100
    pfinalone_ds = (count_oneb_with_ds / count_disaster) * 100


    # write in txt the finals the results
    f = open("probabilities.txt", "w")

    # probability of bubble being 1 to 5,give the result is 'ABSOLUTELY PERFECT'
    f.write("Probability of bubble being 1 to 5,give the result is 'ABSOLUTELY PERFECT'\n")
    f.write("\nThe probability of bubble being '5' given the result is 'ABSOLUTELY PERFECT' is : {:.2f}%\n".format(pfinalfive_aperfect))
    f.write("The probability of bubble being '4' given the result is 'ABSOLUTELY PERFECT' is : {:.2f}%\n".format(pfinalfour_aperfect))
    f.write("The probability of bubble being '3' given the result is 'ABSOLUTELY PERFECT' is : {:.2f}%\n".format(pfinalthree_aperfect))
    f.write("The probability of bubble being '2' given the result is 'ABSOLUTELY PERFECT' is : {:.2f}%\n".format(pfinaltwo_aperfect))
    f.write("The probability of bubble being '1' given the result is 'ABSOLUTELY PERFECT' is : {:.2f}%\n".format(pfinalone_aperfect))

    # probability of bubble being 1 to 5,give the result is 'PERFECT'
    f.write("\nProbability of bubble being 1 to 5,give the result is 'PERFECT'\n")
    f.write("\nThe probability of bubble being '5' given the result is 'PERFECT' is : {:.2f}%\n".format(pfinalfive_perfect))
    f.write("The probability of bubble being '4' given the result is 'PERFECT' is : {:.2f}%\n".format(pfinalfour_perfect))
    f.write("The probability of bubble being '3' given the result is 'PERFECT' is : {:.2f}%\n".format(pfinalthree_perfect))
    f.write("The probability of bubble being '2' given the result is 'PERFECT' is : {:.2f}%\n".format(pfinaltwo_perfect))
    f.write("The probability of bubble being '1' given the result is 'PERFECT' is : {:.2f}%\n".format(pfinalone_perfect))

    # probability of bubble being 1 to 5,give the result is 'FAIR ENOUGH'
    f.write("\nProbability of bubble being 1 to 5,give the result is 'FAIR ENOUGH'\n")
    f.write("\nThe probability of bubble being '5' given the result is 'FAIR ENOUGH' is : {:.2f}%\n".format(pfinalfive_fe))
    f.write("The probability of bubble being '4' given the result is 'FAIR ENOUGH' is : {:.2f}%\n".format(pfinalfour_fe))
    f.write("The probability of bubble being '3' given the result is 'FAIR ENOUGH' is : {:.2f}%\n".format(pfinalthree_fe))
    f.write("The probability of bubble being '2' given the result is 'FAIR ENOUGH' is : {:.2f}%\n".format(pfinaltwo_fe))
    f.write("The probability of bubble being '1' given the result is 'FAIR ENOUGH' is : {:.2f}%\n".format(pfinalone_fe))

    # probability of bubble being 1 to 5,give the result is 'MANY THINGS NEEDS TO GET BETTER'
    f.write("\nProbability of bubble being 1 to 5,give the result is 'MANY THINGS NEEDS TO GET BETTER'\n")
    f.write("\nThe probability of bubble being '5' given the result is 'MANY THINGS NEEDS TO GET BETTER' is : {:.2f}%\n".format(pfinalfive_many))
    f.write("The probability of bubble being '4' given the result is 'MANY THINGS NEEDS TO GET BETTER' is : {:.2f}%\n".format(pfinalfour_many))
    f.write("The probability of bubble being '3' given the result is 'MANY THINGS NEEDS TO GET BETTER' is : {:.2f}%\n".format(pfinalthree_many))
    f.write("The probability of bubble being '2' given the result is 'MANY THINGS NEEDS TO GET BETTER' is : {:.2f}%\n".format(pfinaltwo_many))
    f.write("The probability of bubble being '1' given the result is 'MANY THINGS NEEDS TO GET BETTER' is : {:.2f}%\n".format(pfinalone_many))

    # probability of bubble being 1 to 5,give the result is 'DISASTER'
    f.write("\nProbability of bubble being 1 to 5,give the result is 'DISASTER'\n")
    f.write("\nThe probability of bubble being '5' given the result is 'DISASTER' is : {:.2f}%\n".format(pfinalfive_ds))
    f.write("The probability of bubble being '4' given the result is 'DISASTER' is : {:.2f}%\n".format(pfinalfour_ds))
    f.write("The probability of bubble being '3' given the result is 'DISASTER' is : {:.2f}%\n".format(pfinalthree_ds))
    f.write("The probability of bubble being '2' given the result is 'DISASTER' is : {:.2f}%\n".format(pfinaltwo_ds))
    f.write("The probability of bubble being '1' given the result is 'DISASTER' is : {:.2f}%\n".format(pfinalone_ds))
    f.close()
calculateAndPrint()

# CRITERIA
# A1 : Location,A2 : Personnel,A3 : Cleanliness,A4 : Room Space,A5 : Breakfast,
# A6 : Quiet,A7 : Parking,A8 : Interior Design,A9 : Bed
# if two strings are of widely differing lengths,fuzz.token_set_ratio() comes in
fw = open("criteria.txt","w")
location_counter = 0
staff_counter = 0
br_counter = 0
quiet_counter = 0
bed_counter = 0
clean_counter = 0
roomspace_counter = 0
parking_counter = 0
design_counter = 0

# CRITERIA A1 : Location
word_synonym = ["area","location","district"]
count_inits = 0
for i in word_synonym:
    for j in user_reviews:
        init = fuzz.token_set_ratio(j.lower(),i)
        if i in j:
            location_counter += 1
            if init > 90:
                count_inits += 1
fw.write(f"Criteria word: {word_synonym[1].upper()}\n")
fw.write(f"In how many reviews word {word_synonym[1].upper()} and its synonyms appeared : {location_counter}\n")
fw.write(f"In how many reviews the score was over 90% matching with the word {word_synonym[1]} and its synonyms : {count_inits}\n")
fw.write("\n")

# CRITERIA A2 : Staff
word_synonym = ["personnel","staff","crew"]
count_inits = 0
for i in word_synonym:
    for j in user_reviews:
        init = fuzz.token_set_ratio(j.lower(),i)
        if i in j:
            staff_counter += 1
            if init > 90:
                count_inits += 1
fw.write(f"Criteria word: {word_synonym[1].upper()}\n")
fw.write(f"In how many reviews word {word_synonym[1].upper()} and its synonyms appeared : {staff_counter}\n")
fw.write(f"In how many reviews the score was over 90% matching with the word {word_synonym[1]} and its synonyms : {count_inits}\n")
fw.write("\n")

# CRITERIA A3 : Breakfast
word_synonym = ["brunch","breakfast","early meal"]
count_inits = 0
for i in word_synonym:
    for j in user_reviews:
        init = fuzz.token_set_ratio(j.lower(),i)
        if i in j:
            br_counter += 1
            if init > 90:
                count_inits += 1
fw.write(f"Criteria word: {word_synonym[1].upper()}\n")
fw.write(f"In how many reviews word {word_synonym[1].upper()} and its synonyms appeared : {br_counter}\n")
fw.write(f"In how many reviews the score was over 90% matching with the word {word_synonym[1]} and its synonyms : {count_inits}\n")
fw.write("\n")

# CRITERIA A4 : Quiet
word_synonym = ["quietness","quiet"]
count_inits = 0
for i in word_synonym:
    for j in user_reviews:
        init = fuzz.token_set_ratio(j.lower(),i)
        if i in j:
            quiet_counter += 1
            if init > 90:
                count_inits += 1
fw.write(f"Criteria word: {word_synonym[1].upper()}\n")
fw.write(f"In how many reviews word {word_synonym[1].upper()} and its synonyms appeared : {quiet_counter}\n")
fw.write(f"In how many reviews the score was over 90% matching with the word {word_synonym[1]} and its synonyms : {count_inits}\n")
fw.write("\n")

# CRITERIA A5 : Bed
word_synonym = ["bed"]
count_inits = 0
for i in word_synonym:
    for j in user_reviews:
        init = fuzz.token_set_ratio(j.lower(),i)
        if i in j:
            bed_counter += 1
            if init > 90:
                count_inits += 1
fw.write(f"Criteria word: {word_synonym[0].upper()}\n")
fw.write(f"In how many reviews word {word_synonym[0].upper()} and its synonyms appeared : {bed_counter}\n")
fw.write(f"In how many reviews the score was over 90% matching with the word {word_synonym[0]} and its synonyms : {count_inits}\n")
fw.write("\n")

# CRITERIA A6 : Cleanliness
word_synonym = ["clean","cleanliness","purity","tidiness"]
count_inits = 0
for i in word_synonym:
    for j in user_reviews:
        init = fuzz.token_set_ratio(j.lower(),i)
        if i in j:
            clean_counter += 1
            if init > 90:
                count_inits += 1
fw.write(f"Criteria word: {word_synonym[1].upper()}\n")
fw.write(f"In how many reviews word {word_synonym[1].upper()} and its synonyms appeared : {clean_counter}\n")
fw.write(f"In how many reviews the score was over 90% matching with the word {word_synonym[1]} and its synonyms : {count_inits}\n")
fw.write("\n")

# CRITERIA A7 : RoomSpace
word_synonym = ["room space","large room","small room"]
count_inits = 0
for i in word_synonym:
    for j in user_reviews:
        init = fuzz.token_set_ratio(j.lower(),i)
        if i in j:
            roomspace_counter += 1
            if init > 90:
                count_inits += 1
fw.write(f"Criteria word: {word_synonym[0].upper()}\n")
fw.write(f"In how many reviews word {word_synonym[0].upper()} and its synonyms appeared : {roomspace_counter}\n")
fw.write(f"In how many reviews the score was over 90% matching with the word {word_synonym[1]} and its synonyms: {count_inits}\n")
fw.write("\n")

# CRITERIA A8 : Parking
word_synonym = ["parking","parking area","parking space","parking garage","car parking"]
count_inits = 0
for i in word_synonym:
    for j in user_reviews:
        init = fuzz.token_set_ratio(j.lower(),i)
        if i in j:
            parking_counter += 1
            if init > 90:
                count_inits += 1

fw.write(f"Criteria word: {word_synonym[0].upper()}\n")
fw.write(f"In how many reviews word {word_synonym[0].upper()} and its synonyms appeared : {parking_counter}\n")
fw.write(f"In how many reviews the score was over 90% matching with the word {word_synonym[0]} and its synonyms: {count_inits}\n")
fw.write("\n")

# CRITERIA A9 : Interior Design
word_synonym = ["interior design","design","interior decoration","decor","decorating"]
count_inits = 0
for i in word_synonym:
    for j in user_reviews:
        init = fuzz.token_set_ratio(j.lower(),i)
        if i in j:
            design_counter += 1
            if init > 90:
                count_inits += 1
fw.write(f"Criteria word: {word_synonym[0].upper()}\n")
fw.write(f"In how many reviews word {word_synonym[0].upper()} and its synonyms appeared : {design_counter}\n")
fw.write(f"In how many reviews the score was over 90% matching with the word {word_synonym[0]} and its synonyms: {count_inits}\n")
fw.write("\n")
fw.close()

# Probabilities
# After loops are done, we calculate each criteria probability
# based on reviews number
# p character before every word stands for probability

plocation = (location_counter / counter_reviews) * 100
pstaff = (staff_counter / counter_reviews) * 100
pbr = (br_counter / counter_reviews) * 100
pquiet = (quiet_counter / counter_reviews) * 100
pbed = (bed_counter / counter_reviews) * 100
pclean = (clean_counter / counter_reviews) * 100
proomspace = (roomspace_counter / counter_reviews) * 100
pparking = (parking_counter / counter_reviews) * 100
pdesign = (design_counter / counter_reviews) * 100
print("Plocation: ",plocation)
print("Pstaff: ",pstaff)
print("Pbreakfast: ",pbr)
print("Pquiet: ",pquiet)
print("Pclean: ",pclean)
print("Proomspace: ",proomspace)
print("Pparking: ",pparking)
print("Pdesign: ",pdesign)


# probabilities
# printProbabilities
# 6 params -> The first 5 params get as arguments the probability of reviewScore with specific stars
# The last param get as argument the the criteria probability
# Probabilities of having 'x' bubbles (1 up to 5) given the review is 'PERFECT' and is related to location
# First time w for the file creation
# After first time,each call will got "a" argument [append]
# printProbabilities(opentype,string,pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect,plocation_counter)

def printLocationProbabilities(fopen,string,star_commentreview1,star_commentreview2,star_commentreview3,star_commentreview4,star_commentreview5):
    fw = open("probabilitiesCriteria/location.txt",fopen)
    fw.write("Probability given the review is "+string+" with 5 bubbles and related to location word: {:.2f}%\n".format((star_commentreview5 / 100) * plocation))
    fw.write("Probability given the review is "+string+" with 4 bubbles and related to location word: {:.2f}%\n".format((star_commentreview4 / 100) * plocation))
    fw.write("Probability given the review is "+string+" with 3 bubbles and related to location word: {:.2f}%\n".format((star_commentreview3 / 100) * plocation))
    fw.write("Probability given the review is "+string+" with 2 bubbles and related to location word: {:.2f}%\n".format((star_commentreview2 / 100) * plocation))
    fw.write("Probability given the review is "+string+" with 1 bubbles and related to location word: {:.2f}%\n".format((star_commentreview1 / 100) * plocation))
    fw.write("\n")
def printStaffProbabilities(fopen,string,star_commentreview1,star_commentreview2,star_commentreview3,star_commentreview4,star_commentreview5):
    fw = open("probabilitiesCriteria/staff.txt",fopen)
    fw.write("Probability given the review is "+string+" with 5 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview5 / 100) * pstaff))
    fw.write("Probability given the review is "+string+" with 4 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview4 / 100) * pstaff))
    fw.write("Probability given the review is "+string+" with 3 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview3 / 100) * pstaff))
    fw.write("Probability given the review is "+string+" with 2 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview2 / 100) * pstaff))
    fw.write("Probability given the review is "+string+" with 1 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview1 / 100) * pstaff))
    fw.write("\n")
def printBreakfastProbabilities(fopen,string,star_commentreview1,star_commentreview2,star_commentreview3,star_commentreview4,star_commentreview5):
    fw = open("probabilitiesCriteria/breakfast.txt",fopen)
    fw.write("Probability given the review is "+string+" with 5 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview5 / 100) * pbr))
    fw.write("Probability given the review is "+string+" with 4 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview4 / 100) * pbr))
    fw.write("Probability given the review is "+string+" with 3 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview3 / 100) * pbr))
    fw.write("Probability given the review is "+string+" with 2 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview2 / 100) * pbr))
    fw.write("Probability given the review is "+string+" with 1 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview1 / 100) * pbr))
    fw.write("\n")
def printQuietProbabilities(fopen,string,star_commentreview1,star_commentreview2,star_commentreview3,star_commentreview4,star_commentreview5):
    fw = open("probabilitiesCriteria/quiet.txt",fopen)
    fw.write("Probability given the review is "+string+" with 5 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview5 / 100) * pquiet))
    fw.write("Probability given the review is "+string+" with 4 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview4 / 100) * pquiet))
    fw.write("Probability given the review is "+string+" with 3 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview3 / 100) * pquiet))
    fw.write("Probability given the review is "+string+" with 2 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview2 / 100) * pquiet))
    fw.write("Probability given the review is "+string+" with 1 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview1 / 100) * pquiet))
    fw.write("\n")
def printBedProbabilities(fopen,string,star_commentreview1,star_commentreview2,star_commentreview3,star_commentreview4,star_commentreview5):
    fw = open("probabilitiesCriteria/bed.txt",fopen)
    fw.write("Probability given the review is "+string+" with 5 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview5 / 100) * pbed))
    fw.write("Probability given the review is "+string+" with 4 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview4 / 100) * pbed))
    fw.write("Probability given the review is "+string+" with 3 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview3 / 100) * pbed))
    fw.write("Probability given the review is "+string+" with 2 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview2 / 100) * pbed))
    fw.write("Probability given the review is "+string+" with 1 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview1 / 100) * pbed))
    fw.write("\n")
def printCleanlinessProbabilities(fopen,string,star_commentreview1,star_commentreview2,star_commentreview3,star_commentreview4,star_commentreview5):
    fw = open("probabilitiesCriteria/cleanliness.txt",fopen)
    fw.write("Probability given the review is "+string+" with 5 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview5 / 100) * pclean))
    fw.write("Probability given the review is "+string+" with 4 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview4 / 100) * pclean))
    fw.write("Probability given the review is "+string+" with 3 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview3 / 100) * pclean))
    fw.write("Probability given the review is "+string+" with 2 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview2 / 100) * pclean))
    fw.write("Probability given the review is "+string+" with 1 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview1 / 100) * pclean))
    fw.write("\n")
def printRoomSpaceProbabilities(fopen,string,star_commentreview1,star_commentreview2,star_commentreview3,star_commentreview4,star_commentreview5):
    fw = open("probabilitiesCriteria/roomspace.txt",fopen)
    fw.write("Probability given the review is "+string+" with 5 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview5 / 100) * proomspace))
    fw.write("Probability given the review is "+string+" with 4 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview4 / 100) * proomspace))
    fw.write("Probability given the review is "+string+" with 3 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview3 / 100) * proomspace))
    fw.write("Probability given the review is "+string+" with 2 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview2 / 100) * proomspace))
    fw.write("Probability given the review is "+string+" with 1 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview1 / 100) * proomspace))
    fw.write("\n")
def printParkingProbabilities(fopen,string,star_commentreview1,star_commentreview2,star_commentreview3,star_commentreview4,star_commentreview5):
    fw = open("probabilitiesCriteria/parking.txt",fopen)
    fw.write("Probability given the review is "+string+" with 5 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview5 / 100) * pparking))
    fw.write("Probability given the review is "+string+" with 4 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview4 / 100) * pparking))
    fw.write("Probability given the review is "+string+" with 3 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview3 / 100) * pparking))
    fw.write("Probability given the review is "+string+" with 2 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview2 / 100) * pparking))
    fw.write("Probability given the review is "+string+" with 1 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview1 / 100) * pparking))
    fw.write("\n")
def printInteriorDesignProbabilities(fopen,string,star_commentreview1,star_commentreview2,star_commentreview3,star_commentreview4,star_commentreview5):
    fw = open("probabilitiesCriteria/interiordesign.txt",fopen)
    fw.write("Probability given the review is "+string+" with 5 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview5 / 100) * pdesign))
    fw.write("Probability given the review is "+string+" with 4 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview4 / 100) * pdesign))
    fw.write("Probability given the review is "+string+" with 3 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview3 / 100) * pdesign))
    fw.write("Probability given the review is "+string+" with 2 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview2 / 100) * pdesign))
    fw.write("Probability given the review is "+string+" with 1 bubbles and related to staff word: {:.2f}%\n".format((star_commentreview1 / 100) * pdesign))
    fw.write("\n")

# Probabilities of having 'x' bubbles (1 up to 5) given the review status and is related to location
printLocationProbabilities("w","ABSOLUTELY PERFECT",pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect)
printLocationProbabilities("a","PERFECT",pfinalone_perfect,pfinaltwo_perfect,pfinalthree_perfect,pfinalfour_perfect,pfinalfive_perfect)
printLocationProbabilities("a","FAIR ENOUGH",pfinalone_fe,pfinaltwo_fe,pfinalthree_fe,pfinalfour_fe,pfinalfive_fe)
printLocationProbabilities("a","MANY THINGS NEEDS TO GET BETTER",pfinalone_many,pfinaltwo_many,pfinalthree_many,pfinalfour_many,pfinalfive_many)
printLocationProbabilities("a","DISASTER",pfinalone_ds,pfinaltwo_ds,pfinalthree_ds,pfinalfour_ds,pfinalfive_ds)

# Probabilities of having 'x' bubbles (1 up to 5) given the review status and is related to staff
printStaffProbabilities("w","ABSOLUTELY PERFECT",pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect)
printStaffProbabilities("a","PERFECT",pfinalone_perfect,pfinaltwo_perfect,pfinalthree_perfect,pfinalfour_perfect,pfinalfive_perfect)
printStaffProbabilities("a","FAIR ENOUGH",pfinalone_fe,pfinaltwo_fe,pfinalthree_fe,pfinalfour_fe,pfinalfive_fe)
printStaffProbabilities("a","MANY THINGS NEEDS TO GET BETTER",pfinalone_many,pfinaltwo_many,pfinalthree_many,pfinalfour_many,pfinalfive_many)
printStaffProbabilities("a","DISASTER",pfinalone_ds,pfinaltwo_ds,pfinalthree_ds,pfinalfour_ds,pfinalfive_ds)

# Probabilities of having 'x' bubbles (1 up to 5) given the review status and is related to breakfast
printBreakfastProbabilities("w","ABSOLUTELY PERFECT",pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect)
printBreakfastProbabilities("a","PERFECT",pfinalone_perfect,pfinaltwo_perfect,pfinalthree_perfect,pfinalfour_perfect,pfinalfive_perfect)
printBreakfastProbabilities("a","FAIR ENOUGH",pfinalone_fe,pfinaltwo_fe,pfinalthree_fe,pfinalfour_fe,pfinalfive_fe)
printBreakfastProbabilities("a","MANY THINGS NEEDS TO GET BETTER",pfinalone_many,pfinaltwo_many,pfinalthree_many,pfinalfour_many,pfinalfive_many)
printBreakfastProbabilities("a","DISASTER",pfinalone_ds,pfinaltwo_ds,pfinalthree_ds,pfinalfour_ds,pfinalfive_ds)

# Probabilities of having 'x' bubbles (1 up to 5) given the review status and is related to quiet
printQuietProbabilities("w","ABSOLUTELY PERFECT",pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect)
printQuietProbabilities("a","PERFECT",pfinalone_perfect,pfinaltwo_perfect,pfinalthree_perfect,pfinalfour_perfect,pfinalfive_perfect)
printQuietProbabilities("a","FAIR ENOUGH",pfinalone_fe,pfinaltwo_fe,pfinalthree_fe,pfinalfour_fe,pfinalfive_fe)
printQuietProbabilities("a","MANY THINGS NEEDS TO GET BETTER",pfinalone_many,pfinaltwo_many,pfinalthree_many,pfinalfour_many,pfinalfive_many)
printQuietProbabilities("a","DISASTER",pfinalone_ds,pfinaltwo_ds,pfinalthree_ds,pfinalfour_ds,pfinalfive_ds)

# Probabilities of having 'x' bubbles (1 up to 5) given the review status and is related to bed
printBedProbabilities("w","ABSOLUTELY PERFECT",pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect)
printBedProbabilities("a","PERFECT",pfinalone_perfect,pfinaltwo_perfect,pfinalthree_perfect,pfinalfour_perfect,pfinalfive_perfect)
printBedProbabilities("a","FAIR ENOUGH",pfinalone_fe,pfinaltwo_fe,pfinalthree_fe,pfinalfour_fe,pfinalfive_fe)
printBedProbabilities("a","MANY THINGS NEEDS TO GET BETTER",pfinalone_many,pfinaltwo_many,pfinalthree_many,pfinalfour_many,pfinalfive_many)
printBedProbabilities("a","DISASTER",pfinalone_ds,pfinaltwo_ds,pfinalthree_ds,pfinalfour_ds,pfinalfive_ds)

# Probabilities of having 'x' bubbles (1 up to 5) given the review status and is related to cleanliness
printCleanlinessProbabilities("w","ABSOLUTELY PERFECT",pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect)
printCleanlinessProbabilities("a","PERFECT",pfinalone_perfect,pfinaltwo_perfect,pfinalthree_perfect,pfinalfour_perfect,pfinalfive_perfect)
printCleanlinessProbabilities("a","FAIR ENOUGH",pfinalone_fe,pfinaltwo_fe,pfinalthree_fe,pfinalfour_fe,pfinalfive_fe)
printCleanlinessProbabilities("a","MANY THINGS NEEDS TO GET BETTER",pfinalone_many,pfinaltwo_many,pfinalthree_many,pfinalfour_many,pfinalfive_many)
printCleanlinessProbabilities("a","DISASTER",pfinalone_ds,pfinaltwo_ds,pfinalthree_ds,pfinalfour_ds,pfinalfive_ds)

# Probabilities of having 'x' bubbles (1 up to 5) given the review status and is related to roomspace
printRoomSpaceProbabilities("w","ABSOLUTELY PERFECT",pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect)
printRoomSpaceProbabilities("a","PERFECT",pfinalone_perfect,pfinaltwo_perfect,pfinalthree_perfect,pfinalfour_perfect,pfinalfive_perfect)
printRoomSpaceProbabilities("a","FAIR ENOUGH",pfinalone_fe,pfinaltwo_fe,pfinalthree_fe,pfinalfour_fe,pfinalfive_fe)
printRoomSpaceProbabilities("a","MANY THINGS NEEDS TO GET BETTER",pfinalone_many,pfinaltwo_many,pfinalthree_many,pfinalfour_many,pfinalfive_many)
printRoomSpaceProbabilities("a","DISASTER",pfinalone_ds,pfinaltwo_ds,pfinalthree_ds,pfinalfour_ds,pfinalfive_ds)

# Probabilities of having 'x' bubbles (1 up to 5) given the review status and is related to parking
printParkingProbabilities("w","ABSOLUTELY PERFECT",pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect)
printParkingProbabilities("a","PERFECT",pfinalone_perfect,pfinaltwo_perfect,pfinalthree_perfect,pfinalfour_perfect,pfinalfive_perfect)
printParkingProbabilities("a","FAIR ENOUGH",pfinalone_fe,pfinaltwo_fe,pfinalthree_fe,pfinalfour_fe,pfinalfive_fe)
printParkingProbabilities("a","MANY THINGS NEEDS TO GET BETTER",pfinalone_many,pfinaltwo_many,pfinalthree_many,pfinalfour_many,pfinalfive_many)
printParkingProbabilities("a","DISASTER",pfinalone_ds,pfinaltwo_ds,pfinalthree_ds,pfinalfour_ds,pfinalfive_ds)

# Probabilities of having 'x' bubbles (1 up to 5) given the review status and is related to parking
printInteriorDesignProbabilities("w","ABSOLUTELY PERFECT",pfinalone_aperfect,pfinaltwo_aperfect,pfinalthree_aperfect,pfinalfour_aperfect,pfinalfive_aperfect)
printInteriorDesignProbabilities("a","PERFECT",pfinalone_perfect,pfinaltwo_perfect,pfinalthree_perfect,pfinalfour_perfect,pfinalfive_perfect)
printInteriorDesignProbabilities("a","FAIR ENOUGH",pfinalone_fe,pfinaltwo_fe,pfinalthree_fe,pfinalfour_fe,pfinalfive_fe)
printInteriorDesignProbabilities("a","MANY THINGS NEEDS TO GET BETTER",pfinalone_many,pfinaltwo_many,pfinalthree_many,pfinalfour_many,pfinalfive_many)
printInteriorDesignProbabilities("a","DISASTER",pfinalone_ds,pfinaltwo_ds,pfinalthree_ds,pfinalfour_ds,pfinalfive_ds)
