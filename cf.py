# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn import cross_validation as cv
from sklearn.metrics.pairwise import pairwise_distances

from sklearn.metrics import mean_squared_error
from math import sqrt


def rmse(prediction, ground_truth):
    prediction = prediction[ground_truth.nonzero()].flatten()
    ground_truth = ground_truth[ground_truth.nonzero()].flatten()
    return sqrt(mean_squared_error(prediction, ground_truth))


def predict(rating, similarity, type='user'):
    if type == 'user':
        mean_user_rating = rating.mean(axis=1)
        rating_diff = (rating - mean_user_rating[:,np.newaxis])
        pred = mean_user_rating[:,np.newaxis] + similarity.dot(rating_diff) / np.array([np.abs(similarity).sum(axis=1)]).T
    elif type == 'item':
        pred = rating.dot(similarity) / np.array([np.abs(similarity).sum(axis=1)])
    return pred


if __name__ == '__main__':
    header = ['user_id', 'item_id', 'rating', 'timestamp']
    df = pd.read_csv('ratings.dat', sep='::', names=header, engine='python')
    users = df.user_id.unique()
    items = df.item_id.unique()
    n_users = users.shape[0]
    n_items = items.shape[0]

    sorterIndex = dict(zip(users, range(len(users))))
    df['user_id'] = df['user_id'].map(sorterIndex)
    sorterIndex = dict(zip(items, range(len(items))))
    df['item_id'] = df['item_id'].map(sorterIndex)

    train_data, test_data = cv.train_test_split(df, test_size=0.25)

    train_data_matrix = np.zeros((n_users, n_items))
    for line in train_data.itertuples():
        train_data_matrix[line[1], line[2]] = line[3]
    test_data_matrix = np.zeros((n_users, n_items))
    for line in test_data.itertuples():
        test_data_matrix[line[1], line[2]] = line[3]

    user_similarity = pairwise_distances(train_data_matrix, metric="cosine")
    item_similarity = pairwise_distances(train_data_matrix.T, metric="cosine")

    item_prediction = predict(train_data_matrix, item_similarity, type='item')
    user_prediction = predict(train_data_matrix, user_similarity, type='user')

    print ('User based CF RMSE: ' + str(rmse(user_prediction, test_data_matrix)))
    print ('Item based CF RMSe: ' + str(rmse(item_prediction, test_data_matrix)))
