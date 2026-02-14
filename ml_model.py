import numpy as np
from sklearn.ensemble import IsolationForest

def train_user_model(transaction_history):

    if len(transaction_history) < 5:
        return None

    X = np.array(transaction_history).reshape(-1, 1)

    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(X)

    return model


def predict_user_risk(model, amount):

    if model is None:
        return None, 0

    prediction = model.predict([[amount]])
    score = model.decision_function([[amount]])

    return prediction[0], score[0]