import os
import streamlit as st
from together import Together
import requests

# Import icons library
import streamlit.components.v1 as components

# Set Streamlit app width
app_width = 800

# Set Together API key as an environment variable
os.environ["TOGETHER_API_KEY"] = "4ee9783589ac9ed46de547ab8180a0b4db4e9acafbb79c138df5238fc1331793"

# Initialize Together AI client
together_client = Together()

# Function to generate recipe using Together AI
def text_to_recipe(query):
    response = together_client.chat.completions.create(
        model="databricks/dbrx-instruct",
        messages=[{"role": "user", "content": query}],
    )
    return response.choices[0].message.content

# Function to search for related YouTube videos
def search_youtube_videos(query, max_results=10):
    # Replace "YOUR_YOUTUBE_API_KEY" with your actual YouTube Data API key
    youtube_api_key = "AIzaSyDujfV7oij8VwbQVpnsmfhu0zvdOiOphDA"
    
    # Construct the API request URL using the recipe name as the query
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&maxResults={max_results}&key={youtube_api_key}"
    
    # Send the API request
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        data = response.json()
        # Check if there are any search results
        if data['items']:
            # Extract video details
            videos = []
            for item in data['items']:
                video_id = item['id']['videoId']
                video_title = item['snippet']['title']
                videos.append({"id": video_id, "title": video_title})
            return videos
        else:
            return None
    else:
        return None


def main():
    # Initialize recipe variables
    recipe_name = ""
    recipe_instructions = ""

    st.set_page_config(layout="wide")
    st.title("Recipe Generator")

    # Set background color to black
    st.markdown(
        """
        <style>
        body {
            background-color: black !important;
            color: white !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Dietary Preferences
    st.sidebar.header("Dietary Preferences")
    dietary_preferences_placeholder = "Enter your dietary preferences (e.g., vegetarian, gluten-free)"
    dietary_preferences = st.sidebar.text_area("Enter your dietary preferences", height=100, placeholder=dietary_preferences_placeholder)

    # Dietary Restrictions
    st.sidebar.header("Dietary Restrictions")
    dietary_restrictions_placeholder = "Enter your dietary restrictions (e.g., no dairy, nut-free)"
    dietary_restrictions = st.sidebar.text_area("Enter your dietary restrictions", height=100, placeholder=dietary_restrictions_placeholder)


    # Select Meal Type
    st.sidebar.header("Select Meal Type")
    meal_type = st.sidebar.selectbox("Select meal type", options=["Breakfast", "Lunch", "Dinner"])

    # Include Ingredients option
    st.sidebar.header("Include Ingredients")
    include_ingredients = st.sidebar.radio("Include ingredients?", options=["Yes", "No"], index=0, key="include_ingredients")

    # Cooking Time Slider
    st.sidebar.header("Cooking Time")
    cooking_time = st.sidebar.slider("Select cooking time (minutes)", min_value=1, max_value=200, value=30)

    # Cooking Style
    st.sidebar.header("Cooking Style")
    cooking_styles = st.sidebar.multiselect("Select cooking style (up to 7)", options=["Grilling", "Roasting", "Boiling", "Sauteing", "Baking", "Steaming", "Frying"])

    # Number of Servings
    st.sidebar.header("Number of Servings")
    servings = st.sidebar.number_input("Enter number of servings", min_value=1, step=1)

    # Generate Recipe Button
    if st.sidebar.button("Generate Recipe"):
        # Generate the recipe based on the entered query
        query = f"{dietary_preferences} {dietary_restrictions} {meal_type}"
        recipe = text_to_recipe(query)

        # Extract recipe name and instructions
        lines = recipe.split('\n')
        recipe_name = lines[0]
        recipe_instructions = '\n'.join(lines[1:])

    # Display the generated recipe name
    if recipe_name:
        st.header("Generated Recipe")
        st.subheader("Recipe Name:")
        st.write(recipe_name)

    # Display the generated recipe instructions
    if recipe_instructions:
        st.subheader("Instructions & Ingredients:")
        st.write(recipe_instructions)

    # Search for related YouTube videos using the recipe name
    if recipe_name:
        videos = search_youtube_videos(recipe_name)
        if videos:
            st.sidebar.header("YouTube Videos")
            for video in videos:
                # Add border around the video
                st.sidebar.markdown(
                    f"""
                    <div style="border: 1px solid #333; padding: 5px; margin-bottom: 10px;">
                        <iframe class="youtube-video" width="400" height="225" src="https://www.youtube.com/embed/{video['id']}" frameborder="0" allowfullscreen></iframe>
                        <p style="font-size: 14px; font-weight: bold;">{video['title']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    # Apply CSS to ensure the thumbnail stays within the border
    st.markdown(
        """
        <style>
        .youtube-video {
            max-width: 100%;
            height: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
