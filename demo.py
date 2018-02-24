#!/usr/bin/python3
# -*- coding: utf-8 -*-
from numpy import *
from texttable import Texttable

class recommend:
    def __init__(self, movies, ratings, neib=10, topk=20):
        self.movies = movies
        self.ratings = ratings
        self.neib = neib
        self.topk = topk
        self.users_rating = {}
        self.item_rating = {}
        self.neighbors = []
        self.recomms = []

    def computingUser(self, user):
        self.getInfo()
        self.topk = len(self.users_rating[user])
        self.getSimilarUser(user)
        self.getrecommands()

    def getrecommands(self):
        recomms = []
        tmp = {}
        for sim,User in self.neighbors:
            movies = self.users_rating[User]
            for movie in movies:
                if(movie[0] in tmp):
                    tmp[movie[0]] += sim
                else:
                    tmp[movie[0]] = sim
        for key in tmp:
            recomms.append([tmp[key], key])
        recomms.sort(reverse=True)
        recomms = recomms[:self.topk]
        self.recomms = recomms

    def getInfo(self):
        self.users_rating = {}
        self.item_rating = {}
        for rating in self.ratings:
            user_ID = rating[0]
            movie_ID = rating[1]
            movie_rating = rating[2]
            tmp = (movie_ID,movie_rating)
            if(user_ID in self.users_rating):
                self.users_rating[user_ID].append(tmp)
            else:
                self.users_rating[user_ID] = [tmp]
            if(movie_ID in self.item_rating):
                self.item_rating[movie_ID].append(user_ID)
            else:
                self.item_rating[movie_ID] = [user_ID]

    def getSimilarUser(self, user):
        similarUsers = []
        self.neighbors = []
        for rating in self.users_rating[user]:
            for userID in self.item_rating[rating[0]]:
                if(userID != user and userID not in similarUsers):
                    similarUsers.append(userID)
        for tmpUser in similarUsers:
            sim = self.similarity(user, tmpUser)
            self.neighbors.append([sim,tmpUser])
        self.neighbors.sort(reverse=True)
        self.neighbors = self.neighbors[:self.neib]

    def getUsersDict(self,userID,userID2):
        userDict = {}
        for movieID,movieRating in self.users_rating[userID]:
            userDict[movieID] = [movieRating,0]
        for movieID,movieRating in self.users_rating[userID2]:
            if(movieID in userDict):
                userDict[movieID][1] = movieRating
            else:
                userDict[movieID] = [0, movieRating]
        return userDict

    def similarity(self,user,tmpUser):
        user = self.getUsersDict(user,tmpUser)
        tmp = [0,0,0]
        for _, rating in user.items():
            rating1 = float(rating[0])
            rating2 = float(rating[1])
            tmp[0] += rating1 * rating1
            tmp[1] += rating2 * rating2
            tmp[2] += rating1 * rating2
        return tmp[2] / sqrt(tmp[0] * tmp[1])


    def result(self):
        neighbors_id = [i[1] for i in self.neighbors]
        table = Texttable()

        table2 = Texttable()
        table2.set_cols_dtype(["t", "t"])
        table2.set_cols_align(["l", "l"])
        rows2 = []
        rows2.append([u"Movie Name", u"recommend by user ID"])
        table.set_cols_dtype(["t", "t", "t"])
        table.set_cols_align(["l", "l", "l"])
        rows = []
        #rows.append([u"movie ID", u"Name", u"release", u"from userID"])
        rows.append([u"Movie ID", u"Movie Name", u"categories"])
        movie2 = None
        for item in self.recomms:
            fromID = []
            for i in self.movies:
                if i[0] == item[1]:
                    movie = i #M ['318', 'Shawshank Redemption, The (1994)', 'Drama']
                    movie2 = list(movie)
                    movie2.pop(0)
                    movie2.pop(1)
                    break
            for i in self.item_rating[item[1]]:
                if i in neighbors_id:
                    fromID.append(i)
            movie2.append(tuple(fromID))
            rows.append(movie)
            rows2.append(movie2)
        table.add_rows(rows)
        table2.add_rows(rows2)
        print(table.draw())
        print("Below is the table showing who contribute to this recomm========================")
        print(table2.draw())



def readmovie(filename):
    files = open(filename, "r", encoding="iso-8859-15")
    data = []
    for line in files.readlines():
        item = line.strip().split("::")
        data.append(item)

    return data
def readratins(filename):
    files = open(filename, "r", encoding="iso-8859-15")
    data = []
    for line in files.readlines():
        item = line.strip().split("::")
        item.pop(-1)
        data.append(item)

    return data


def main():
    movies = readmovie("movies.dat")
    ratings = readratins("ratings.dat")
    demo = recommend(movies, ratings)
    demo.computingUser("55")
    print("recommendations for user ID:", 55)
    demo.result()

main()

