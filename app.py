# ===== Step 1: Import Libraries =====
import streamlit as st                 # Streamlit for interactive web apps
import pandas as pd                    # For data manipulation
import matplotlib.pyplot as plt        # For plotting
import seaborn as sns                  # Enhanced plotting with Seaborn
from wordcloud import WordCloud        # To generate a word cloud visualization

# ===== Step 2: Load Cleaned Dataset =====
# Load the cleaned CORD-19 dataset from CSV
df = pd.read_csv("metadata_cleaned.csv")

# ===== Step 3: App Title and Description =====
st.title("CORD-19 Data Explorer")      # Main app title
st.write("""
Interactive exploration of COVID-19 research papers.
Filter by publication year or journal and visualize trends.
""")                                   # App description

# ===== Step 4: Interactive Year Slider =====
# Slider widget for selecting a range of publication years
year_range = st.slider(
    "Select publication year range",   # Label for slider
    int(df['year'].min()),             # Minimum year
    int(df['year'].max()),             # Maximum year
    (int(df['year'].min()), int(df['year'].max()))  # Default range
)

# Filter dataset based on selected year range
filtered_df = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]

# ===== Step 5: Display Sample of Filtered Data =====
st.subheader("Sample Papers")  # Section title
# Display first 10 rows of filtered data
st.dataframe(filtered_df[['title','abstract','authors','journal','year']].head(10))

# ===== Step 6: Plot Papers Published Per Year =====
st.subheader("Papers Published Per Year")  # Section title

# Count papers per year
papers_per_year = filtered_df['year'].value_counts().sort_index()

# Create a matplotlib figure for the bar chart
fig, ax = plt.subplots(figsize=(8,4))
# Draw bar plot with seaborn
sns.barplot(x=papers_per_year.index, y=papers_per_year.values, color='skyblue', ax=ax)
ax.set_xlabel("Year")                # X-axis label
ax.set_ylabel("Number of Papers")    # Y-axis label
ax.set_title("COVID-19 Papers Per Year")  # Plot title
# Display plot in Streamlit
st.pyplot(fig)

# ===== Step 7: Top 10 Journals =====
st.subheader("Top 10 Journals")  # Section title

# Count top 10 journals
top_journals = filtered_df['journal'].value_counts().head(10)

# Create figure for horizontal bar chart
fig2, ax2 = plt.subplots(figsize=(8,4))
sns.barplot(x=top_journals.values, y=top_journals.index, palette="viridis", ax=ax2)
ax2.set_xlabel("Number of Papers")
ax2.set_ylabel("Journal")
ax2.set_title("Top Journals Publishing COVID-19 Papers")
st.pyplot(fig2)  # Display chart in Streamlit

# ===== Step 8: Word Cloud of Paper Titles =====
st.subheader("Word Cloud of Paper Titles")  # Section title

# Combine all titles in filtered dataset
all_titles = " ".join(filtered_df['title'].dropna().astype(str))
# Generate word cloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)

# Create matplotlib figure for word cloud
fig3, ax3 = plt.subplots(figsize=(12,6))
ax3.imshow(wordcloud, interpolation='bilinear')  # Display image
ax3.axis('off')  # Remove axes
st.pyplot(fig3)  # Render in Streamlit

# ===== Step 9: Optional - Filter by Journal Dropdown =====
st.subheader("Filter by Journal")  # Section title

# Dropdown widget to select a journal
journal_list = filtered_df['journal'].dropna().unique()
selected_journal = st.selectbox("Select a journal", journal_list)

# Filter dataset for selected journal
journal_papers = filtered_df[filtered_df['journal'] == selected_journal]
# Display first 10 papers for selected journal
st.write(f"Papers from {selected_journal}:")
st.dataframe(journal_papers[['title','abstract','authors','year']].head(10))
