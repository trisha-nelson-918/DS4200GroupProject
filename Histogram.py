import pandas as pd
import plotly.express as px
from collections import Counter
from itertools import chain


# Load the data
df = pd.read_csv('movies_cleaned1.csv') 
df.head()

# Split genres and keywords into lists
df['genres'] = df['genres'].fillna('').apply(lambda x: x.split(', ') if x else [])
df['keywords'] = df['keywords'].fillna('').apply(lambda x: x.split(', ') if x else [])

# Extract genre count
genre_count = df.explode('genres').groupby('genres').size().reset_index(name='count')

# Extract most common keywords for each genre
def get_most_common_keywords(genre):
    """ 
        Args (str): genre found in list of genres from dataframe
        Outputs (str): string of 5 most commonly used keywords for each genre separated by commas
        
        This function takes in the cleaned csv file to sort through the list of genres sorted for each movie, 
        make a count of how many movies associate to a unique genre, and outputs the most commonly 
        applied keywords within these genres.
        
    """
    
    # Get all keywords associated with the genre
    genre_keywords = df[df['genres'].apply(lambda genres: genre in genres)]['keywords']
    all_keywords = list(chain(*genre_keywords))
    
    # Get top 5 most common keywords
    most_common = Counter(all_keywords).most_common(5)  
    return ', '.join([kw[0] for kw in most_common])

# Apply the function to create a 'common_keywords' column
genre_count['common_keywords'] = genre_count['genres'].apply(get_most_common_keywords)

# Count movies per genre
genre_count = df.explode('genres').groupby('genres').agg(
    count=('genres', 'size'),
    avg_popularity=('popularity', 'mean')
).reset_index()

# Round avg_popularity to two decimal places
genre_count['avg_popularity'] = genre_count['avg_popularity'].round(2)

# Apply function to add most common keywords column
genre_count['common_keywords'] = genre_count['genres'].apply(get_most_common_keywords)

# Create a histogram with hover data
fig = px.bar(
    genre_count, 
    x='genres', 
    y='count', 
    hover_data={'genres': False, 'avg_popularity': True, 'common_keywords': True}, 
    title="Number of Movies Per Genre with Average Popularity",
    labels={'genres': 'Genre', 'count': 'Number of Movies', 'avg_popularity': 'Avg. Popularity'}
)

fig.update_traces(textposition='outside')

fig.show()
