from django.shortcuts import render
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from dreamweavers.forms import UniversityRecommendationForm
import os
# Load the dataset
df = pd.read_csv('college.csv')
# print(df.head())
# print(f"Original DataFrame: \n{df.head()}")
# print(df.dtypes)

# df = pd.read_csv(os.path.join(os.path.dirname(__file__), 'college.csv'))

# Combine relevant features
df['Combined'] = df['City'] + ' ' + df['Subjects'] + ' ' + df['Country']

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(df['Combined'])

# Function to recommend universities based on user input
# def recommend_universities(user_city, user_cost, user_subjects, user_ielts_score, user_country):
#     user_input_combined = user_city + ' ' + user_subjects + ' ' + user_country
#     user_vector = vectorizer.transform([user_input_combined])
#     cosine_sim = cosine_similarity(user_vector, tfidf_matrix)
#     df['Similarity'] = cosine_sim[0]
#     df_filtered = df[(df['City'].str.contains(user_city, case=False)) & 
#                      (df['Country'].str.contains(user_country, case=False)) &
#                      (df['Cost'] <= user_cost) & 
#                      (df['IELTS Score'] <= user_ielts_score)]
#     recommended_universities = df_filtered.sort_values(by='Similarity', ascending=False)
#     return recommended_universities[['University', 'Cost', 'City', 'Country', 'IELTS Score']]
def recommend_universities(user_city, user_cost, user_subjects, user_ielts_score, user_country):
    user_input_combined = user_city + ' ' + user_subjects + ' ' + user_country
    user_vector = vectorizer.transform([user_input_combined])
    cosine_sim = cosine_similarity(user_vector, tfidf_matrix)
    df['Similarity'] = cosine_sim[0]
    
    print(f"User Input Combined: {user_input_combined}")
    print(f"Cosine Similarity: {cosine_sim[0]}")
    
    df_filtered = df[
        (df['City'].str.contains(user_city, case=False)) &
        (df['Country'].str.contains(user_country, case=False)) &
        (df['Cost'] <= user_cost) &
        (df['IELTS Score'] <= user_ielts_score)
    ]
    
    print("Filtered DataFrame:")
    print(df_filtered)
    
    recommended_universities = df_filtered.sort_values(by='Similarity', ascending=False)
    
    print("Sorted Recommendations:")
    print(recommended_universities)
    
    return recommended_universities[['University', 'Cost', 'City', 'Country', 'IELTS Score']]


# def recommend_universities(user_city, user_cost, user_subjects, user_ielts_score, user_country):
#     user_input_combined = user_city + ' ' + user_subjects + ' ' + user_country
#     user_vector = vectorizer.transform([user_input_combined])
#     cosine_sim = cosine_similarity(user_vector, tfidf_matrix)
#     df['Similarity'] = cosine_sim[0]

#     # Apply filters based on user input
#     df_filtered = df[(df['City'].str.contains(user_city, case=False, na=False)) & 
#                  (df['Country'].str.contains(user_country, case=False, na=False)) &
#                  (df['Cost'] <= user_cost) & 
#                  (df['IELTS Score'] <= user_ielts_score)]
    
#     # Log the filtered DataFrame
#     print(f"Filtered DataFrame: \n{df_filtered}")
#     print("Filtered DataFrame:")
#     print(df_filtered)

#     recommended_universities = df_filtered.sort_values(by='Similarity', ascending=False)
    
#     # Log the sorted recommendations
#     print(f"Sorted Recommendations: \n{recommended_universities}")
    
#     return recommended_universities[['University', 'Cost', 'City', 'Country', 'IELTS Score']]



def university_recommendation_view(request):
    if request.method == 'POST':
        form = UniversityRecommendationForm(request.POST)
        if form.is_valid():
            user_city = form.cleaned_data['city']
            user_country = form.cleaned_data['country']
            user_cost = form.cleaned_data['cost']
            user_subjects = form.cleaned_data['subjects']
            user_ielts_score = form.cleaned_data['ielts']

            # Log the form data
            print(f"Form Data: city={user_city}, country={user_country}, cost={user_cost}, subjects={user_subjects}, ielts={user_ielts_score}")
            
            # Call the recommendation function
            recommendations_df = recommend_universities(user_city, user_cost, user_subjects, user_ielts_score, user_country)

            # Log the recommendation DataFrame
            print(f"Recommendations DataFrame: \n{recommendations_df}")
            
            recommendations_df.rename(columns={'IELTS Score': 'IELTS'}, inplace=True)
            # Convert DataFrame to a list of dictionaries
            recommendations = recommendations_df.to_dict(orient='records')
            
            # Log the recommendations
            print(f"Recommendations: {recommendations}")
            
            return render(request, 'unirecomend.html', {'recommendations': recommendations})
        else:
            # Log form errors if any
            print(f"Form Errors: {form.errors}")
    else:
        form = UniversityRecommendationForm()
    
    return render(request, 'unirecomend.html', {'form': form})

