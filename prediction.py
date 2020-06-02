import pickle

#doc_new = ['obama is running for president in 2016']
class pred:

    #function to run for prediction
    def detecting_fake_news(var):    
    #retrieving the best model for prediction call
        load_model = pickle.load(open('./final_model.sav', 'rb'))
        prediction = load_model.predict([var])
        prob = load_model.predict_proba([var])
        return ("The given statement is ",prediction[0],"The truth probability score is ",prob[0][1])
