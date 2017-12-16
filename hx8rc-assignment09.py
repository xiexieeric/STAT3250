##
## File: hx8rc-assignment09.py
## Topic: Assignment 9
## Name: Eric Xie
## Section time: 3:30-4:45
## Grading Group: 6
##

import pandas as pd
import numpy as np
import re

reviews = pd.read_csv('reviews.txt',
                      sep='\t',
                      header=None,
                      names=['Reviewer', 'Movie', 'Rating', 'Date'])

## 1.
# Group reviews by reviewer and count entries by any column to get reviews per reviewer
review_counts = reviews.groupby('Reviewer')['Movie'].count().sort_values(ascending=False)
# Isolate reviews written by the top 5 reviewers
reviews_top5 = reviews[reviews['Reviewer'].isin(review_counts.index[:5])]
# Calculate parameters for the CI formula for the avg rating of reviews by top 5 reviewers
x_bar = reviews_top5['Rating'].mean()
s = reviews_top5['Rating'].std(ddof=1)
n = len(reviews_top5['Rating'])
ci = [x_bar - 1.96 * s / np.sqrt(n), x_bar + 1.96 * s / np.sqrt(n)] # CI formula
print(ci)
# Find the complement set of reviews to get the remaining reviews
reviews_not_top5 = reviews[~(reviews['Reviewer'].isin(review_counts.index[:5]))]
# Calculate mean rating of those reviews
print('Average rating of remaining reviews:', reviews_not_top5['Rating'].mean())

'''
1.
[2.9048586350882037, 2.9975803893020401]
Average rating of remaining reviews: 3.5484703356591387
The average rating of the remaining reviews is not within a 95% CI for the average rating given
by the top 5 reviewers. 
'''

## 2.
# Read in genres.txt as dataframe
movies = pd.read_csv('genres.txt', sep='|', header=None, names=['Movie', 'Title', 'Rel_Date', 'Vid_Date', 'Url',
                                                                'unknown', 'Action', 'Adventure', 'Animation',
                                                                'Childrens', 'Comedy', 'Crime', 'Documentary',
                                                                'Drama', 'Fantasy', 'FilmNoir', 'Horror', 'Musical',
                                                                'Mystery', 'Romance', 'SciFi', 'Thriller', 'War',
                                                                'Western'])
# Group reviews by Movie ID and count by any column to get 10 most reviewed movies
movie_counts = reviews.groupby('Movie')['Reviewer'].count().sort_values(ascending=False)[:10]
# Create a df that contains Movie ID and it's associated number of reviews for the top 10 movies
movies_top10 = pd.DataFrame({'Movie': movie_counts.index, 'Count': movie_counts})
# Create a df that contains movie id in the same column as movie title
movie_titles = pd.DataFrame({'Movie': movies['Movie'], 'Title': movies['Title']})
# Merge the titles df with the top 10 movies df on Movie ID
movies_with_count = pd.merge(movies_top10, movie_titles)
movies_with_count = movies_with_count[['Title', 'Count']] # Reorder the columns to suit answer format
print(movies_with_count.to_string(index=False)) # Print without the index column

'''
2.
             Star Wars (1977)    583
               Contact (1997)    509
                 Fargo (1996)    508
    Return of the Jedi (1983)    507
             Liar Liar (1997)    485
  English Patient, The (1996)    481
                Scream (1996)    478
             Toy Story (1995)    452
         Air Force One (1997)    431
Independence Day (ID4) (1996)    429
'''

## 3.
# Create a df with only the movie IDs of each reviews, and merge that with genres.txt
# such that each review contains its genre information
with_genres = pd.merge(pd.DataFrame({'Movie': reviews['Movie']}), movies, on='Movie')
# Drop unnecessary columns from merged df
with_genres = with_genres.drop(['Movie','unknown','Vid_Date'], axis=1)
# Sum the genre columns for all reviews, ignoring non-numeric volumes, and sort
genres_count = with_genres.sum(numeric_only=True).sort_values(ascending=False)
print('highest:', genres_count.idxmax()) # Prints the genre with highest sum
print('lowest:', genres_count.idxmin()) # Prints genre with lowest sum

'''
3.
highest: Drama
lowest: Documentary
'''

## 4.
genres = movies.iloc[:,-18:].sum(axis=1) # Isolate only genres columns from genres.txt and sum horizontally
movies["Num_Genres"] = genres # Add the genres count for each movie back into the genres.txt df
# Merge genres.txt with the genres count into reviews.txt, so that each review knows how many genres it represents
with_genres = pd.merge(pd.DataFrame({'Movie': reviews['Movie']}), movies, on='Movie')
multi_genre = len(with_genres[with_genres['Num_Genres'] > 1]) # Isolate reviews with more than 1 genre
print(multi_genre*100/len(with_genres)) # Percentage formula

'''
4.
69.938%
'''

## 5.
# Read in reviewers.txt as df
reviewers = pd.read_csv('reviewers.txt', sep='|', header=None, names=['Reviewer', 'Age', 'Gender', 'Job', 'Zip'])
# Add just the reviewer ID and their gender to a new df
gender_by_reviewer = pd.DataFrame({'Reviewer': reviewers['Reviewer'], 'Gender': reviewers['Gender']})
# Merge that df with reviews so that each review entry contains the reviewer's gender
with_gender = pd.merge(reviews, gender_by_reviewer, on='Reviewer')

male_reviews = with_gender[with_gender['Gender'] == 'M'] # Isolate male reviews
# Calculate CI parameters
n_male = len(male_reviews)
x_male = male_reviews['Rating'].mean()
s_male = male_reviews['Rating'].std(ddof=1)
# CI formula
ci_male = [x_male - 1.96 * s_male / np.sqrt(n_male), x_male + 1.96 * s_male / np.sqrt(n_male)]
print('male:', ci_male)

# Repeat CI calculation for female reviews
female_reviews = with_gender[with_gender['Gender'] == 'F']
n_female = len(female_reviews)
x_female = female_reviews['Rating'].mean()
s_female = female_reviews['Rating'].std(ddof=1)
ci_female = [x_female - 1.96 * s_female / np.sqrt(n_female), x_female + 1.96 * s_female / np.sqrt(n_female)]
print('female:', ci_female)

'''
5.
male: [3.5213085280777978, 3.5372694412192667]
female: [3.5172022879993174, 3.5458124750154458]
'''

## 6.
# Read in zipcodes.txt as df, eliminating duplicate entries
zips = pd.read_csv('zipcodes.txt', usecols=[1,4],
                   converters={'Zipcode':str}).drop_duplicates()
zipseries = pd.Series(data=zips['State'].values, index=zips['Zipcode']) # Series mapping zipcode to state
# Define function that returns the region of a zipcode value
def ziptostate(zcode):
    if re.search('[a-zA-Z]', zcode): # If the zipcode contains a letter
        return 'Canada' # It must be Canada
    elif zcode in zipseries: # If the zipcode is in the zipseries
        return zipseries[zcode] # Return the state for that zipcode
    else: # Otherwise the zipcode is invalid
        return "Unknown" # Return unknown
# For each reviewer's zipcode, convert it to the region it represents, and add that as a column to reviewers.txt
reviewers['Location'] = reviewers['Zip'].apply(ziptostate)
# Merge reviews.txt with reviewers.txt, so each review has the reviewer's location
with_locs = pd.merge(reviews, reviewers, on="Reviewer")
# Group by location, and count by a certain column to get reviews per location
by_loc = with_locs.groupby('Location')['Reviewer'].count()
# Filter out the counts for Unknown location, and sort from highest to lowest
by_loc = by_loc[by_loc.index != 'Unknown'].sort_values(ascending=False)
print(by_loc[:10]) # Print top 10 most common reviewer locations

'''
6.
CA    13842
MN     7635
NY     6882
IL     5740
TX     5042
OH     3475
PA     3339
MD     2739
VA     2590
MA     2584
'''

## 7.
# Remove reviews by occupations of "other" and "none"
exclude_jobs = with_locs[(with_locs['Job'] != 'other') & (with_locs['Job'] != 'none')]
# Group by occupation and find the mean rating
mean_ratings = exclude_jobs.groupby('Job')['Rating'].mean()
print('highest:', mean_ratings.idxmax()) # Prints occupation with highest avg rating
print('lowest:', mean_ratings.idxmin()) # Prints occupation with lowest avg rating

'''
7.
highest: lawyer
lowest: healthcare
'''

## 8.
df = pd.merge(reviews, movies, on='Movie') # Merge reviews.txt with genres.txt
# Group by IMDB url to eliminate duplicate movies
num_ratings = df.groupby('Url')['Rating'].count()
# Merge review counts per movie with movies, so each movie knows its review count
movies_count_reviews = pd.merge(movies, pd.DataFrame({'Url': num_ratings.index, 'Count': num_ratings}), on='Url')
movies_count_reviews.drop_duplicates(subset='Url', inplace=True) # Drop duplicate movies by Url
count_max20 = movies_count_reviews[movies_count_reviews['Count'] <= 20] # Isolate movies with 20 or less reviews
total_movies = len(movies_count_reviews) # Find total unique movies
# Group by review count up to 20 reviews, count by any column to find frequency
countby_num_reviews = count_max20.groupby('Count')['Movie'].count()
print(countby_num_reviews*100/total_movies) # Percentage formula

'''
8.
1     8.072289
2     3.915663
3     3.493976
4     3.734940
5     3.012048
6     2.289157
7     2.771084
8     1.686747
9     2.108434
10    1.987952
11    1.204819
12    1.686747
13    1.506024
14    0.843373
15    1.325301
16    1.144578
17    0.602410
18    1.445783
19    1.084337
20    0.722892

** It was noticed that genres.txt unintentionally(?) contains duplicate entries for the same movie, e.g.: Chasing Amy is both
movie 246 and 268, and Kull the Conquerer is both 267 and 680. My code removes those before groupby. 
'''

## 9.
# List of genres
genres_list = ['Action', 'Adventure', 'Animation',
               'Childrens', 'Comedy', 'Crime', 'Documentary',
               'Drama', 'Fantasy', 'FilmNoir', 'Horror', 'Musical',
               'Mystery', 'Romance', 'SciFi', 'Thriller', 'War',
               'Western']
genre_avg = [] # List to store tuples of format (Genre, Avg Rating)
for genre in genres_list: # Iterate through genres
    all_ratings = df['Rating'] * df[genre] # Multiply that genre's col by Ratings
    all_ratings = all_ratings[all_ratings > 0] # Isolate only rows that were positive
    avg = all_ratings.mean() # Calculate average rating
    genre_avg.append((genre, avg)) # Add the genre and its avg to the list
sorted_genres = sorted(genre_avg, key= lambda x:x[1], reverse=True) # Sort the list of tuples by the ratings
print('Highest rating:', sorted_genres[0][0]) # Print highest rated genre
print('Lowest rating:', sorted_genres[-1][0]) # Print lowest rated genre

'''
9.
Highest rating: FilmNoir
Lowest rating: Fantasy
'''

## 10a.
# Find total number of positive reviews by males and females
male_pos = len(male_reviews[male_reviews['Rating'] > 3])
female_pos = len(female_reviews[female_reviews['Rating'] > 3])
# Calculate parameters for proportion of positive reviews by males
n_m = len(male_reviews)
p_m = male_pos/n_m
q_m = 1-p_m
# Calculate parameters for proportion of positive reviews by males
n_f = len(female_reviews)
p_f = female_pos/n_f
q_f = 1-p_f
# CI Formula
ci = [p_f-p_m-1.96*np.sqrt(p_f*q_f/n_f+p_m*q_m/n_m), p_f-p_m+1.96*np.sqrt(p_f*q_f/n_f+p_m*q_m/n_m)]
print(ci)

'''
10a.
[-0.0057658579712690323, 0.0083267378550685271]
Based on the CI, there is a 95% chance that the difference between p_f and p_m is very small,
between 0.57% to 0.83%. Thus there is no statistically significant evidence that females give 
more positive reviews than males. 
'''

## 10b.
with_locs = with_locs[with_locs['Location'] != 'Unknown'] # Filter out reviews with unknown location
canadian_reviews = with_locs[with_locs['Location'] == 'Canada'] # Isolate canadian reviews
american_reviews = with_locs[with_locs['Location'] != 'Canada'] # Isolate american reviews
c_pos = len(canadian_reviews[canadian_reviews['Rating'] > 3]) # Number of canandian positive reviews
a_pos = len(american_reviews[american_reviews['Rating'] > 3]) # Number of american positive reviews
# Calculate parameters for proportion of positive reviews by canadians
n_c = len(canadian_reviews)
p_c = c_pos/n_c
q_c = 1-p_c
# Calculate parameters for proportion of positive reviews by americans
n_a = len(american_reviews)
p_a = a_pos/n_a
q_a = 1-p_a
# CI Formula
ci = [p_c-p_a-1.96*np.sqrt(p_c*q_c/n_c+p_a*q_a/n_a), p_c-p_a+1.96*np.sqrt(p_c*q_c/n_c+p_a*q_a/n_a)]
print(ci)

'''
10b.
[-0.069417374393881695, -0.026050239950439692]
Based on the CI, there is a 95% chance that p_c - p_a is between -2.6% and -6.9%.
This would suggest that Canadians give slightly less positive reviews than Americans, which  
does not support the hypothesis that Canadians are more likely to give positive reviews than Americans
'''