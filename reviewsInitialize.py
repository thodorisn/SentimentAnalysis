import pandas as pd

def getReviews():
    data = pd.read_excel(r'/Users/thodorisnik/Dropbox/Sxoli/SentimentAnalysisThesis/SentimentAnalysis/reviews.xlsx', sheet_name='Reviews')
    df = pd.DataFrame(data, columns=['Full Review'])
    return df.values

def getBubbles():
    data = pd.read_excel(r'/Users/thodorisnik/Dropbox/Sxoli/SentimentAnalysisThesis/SentimentAnalysis/reviews.xlsx', sheet_name='Reviews')
    rate = pd.DataFrame(data, columns=['Rating'])
    return rate.values