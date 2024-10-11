# %%
#Gujarati language bad words filtered before adding the data to csv file
gujarati_bad_words = [
    "આઇએનડી", "ભાંગ", "ડફર", "ટપક", "કડવું", "ભંયક", "બાગલ", "જુડા", "ફિટક", "કચરો", 
    "છોકરો", "ગંદો", "ગધેડો", "કુતુ", "ઝાંટા", "છિદ્ર", "ફૂફૂ", "કસાબ", "ફટકો", "ઝાટક", 
    "તુકલ", "ગંડકી", "સાળા", "બેપંઝી", "લૂંટો", "ઓછા", "ભીતર", "ઢોલક", "પાગલ", "તખત", 
    "જાળી", "ચામડી", "ઘાટક", "લિઠડ", "ઓટક", "ઝાલ", "બુછડી", "નકામી", "લફડા", "ખોટું", 
    "દેવડા", "ઢીપો", "સીખડો", "ચોટકી", "છાઈ", "રાંદ", "બેઠક", "ખોર", "મોરિયો", "હડક", 
    "ઘોંટી", "ગુંડર", "ચીપો", "નાદાન", "ફતુર", "કૂપ", "તડકો", "ખણક", "અગમ", "કાંકર", 
    "સુપર", "સામું", "ડંખો", "ઝંપો", "ધટકો", "ફિટકાર", "કાઢ", "પગલું", "ઝટકો", "ઢુલક", 
    "સાંભલ", "નભાઈ", "ઘુંટ", "અવલોક", "બાંધવો", "ધારો", "ઝાંઝ", "ઢોક", "દબંગ", "ઢપક", 
    "છૂંફા", "કાપડ", "ચોટું", "ખાટક", "લોટક", "ગજક", "ગડડ", "ઝરક", "કાંકરા", "નમરા", 
    "ઓળખ", "સોડો", "અઠિયું", "ભોડક", "કમલો", "ધમાલ", "ઢગલ"
]


# %%
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import numpy as np

# Set up the WebDriver (Make sure you have ChromeDriver installed and in your PATH)

# URL of the page
# url = "https://www.gujaratilexicon.com/gujarati-blogs/gujarati-language/international-language-day-and-ratilal-chandaria/"
# url="https://www.gujaratilexicon.com/gujarati-blogs/gujarati-language/tips-to-improve-handwriting-in-gujarati-language/"
# url="https://www.gujaratilexicon.com/gujarati-blogs/gujarati-language/importance-of-punctuation-marks-in-gujarati-language/"
# url="https://www.gujaratilexicon.com/gujarati-blogs/events-across-gujarat/about-matrubhasha-abhiyan-and-its-activities/"
# Load the webpage
def fun(url,i):
    driver = webdriver.Chrome()

    driver.get(url)

    # Allow some time for the page to fully load
    time.sleep(3)

    # Initialize empty lists to hold the data
    titles = []
    dates = []
    paragraphs_data = []

    try:
        # Extract the title (assuming it's in an <h1> tag)
        title_element = driver.find_element(By.TAG_NAME, 'h1')
        title = title_element.text
        titles.append(title)

        # Extract the date (assuming it's in a <time> or <span> tag, depending on the structure)
        try:
            date_element = driver.find_element(By.TAG_NAME, 'time')  # Change to appropriate tag if needed
            date = date_element.text
        except:
            date_element = driver.find_element(By.CLASS_NAME, 'info.pb-3.border-bottom')  # Or an appropriate class for date
            date = date_element.text
        dates.append(date)

        # Extract the main content (assuming it's inside a div with the given class)
        content_div = driver.find_element(By.CLASS_NAME, 'info.pb-3.border-bottom')
        paragraphs = content_div.find_elements(By.TAG_NAME, 'p')

        # Loop through and append each paragraph's text to the list
        for p in paragraphs:
            paragraphs_data.append(p.text)

    finally:
        # Close the driver after scraping
        driver.quit()

    # Create a DataFrame with multiple columns
    df = pd.DataFrame({
        "Title": titles * len(paragraphs_data),  # Repeat the title for each paragraph
        "Date": dates * len(paragraphs_data),    # Repeat the date for each paragraph
        "Paragraph": paragraphs_data             # Paragraphs as separate rows
    })

    # Display the DataFrame
    # print(df)

    # Save the DataFrame to a CSV file (optional)
    df.to_csv(f"extracted_blog_data{i}.csv", index=False)


# %%
#Add links to  below list in order to extract data 
url=["",
     "",
     "",
     "",
       ]

#few remaining links are in below list, while many sublinks were used. 
# All sources home links are added in a separate dictionary along with the size of data extracted
url = ["https://www.gujaratilexicon.com/gujarati-blogs/gujarati-language/international-language-day-and-ratilal-chandaria/","https://www.gujaratilexicon.com/gujarati-blogs/gujarati-language/tips-to-improve-handwriting-in-gujarati-language/"
"https://www.gujaratilexicon.com/gujarati-blogs/gujarati-language/importance-of-punctuation-marks-in-gujarati-language/",
"https://www.gujaratilexicon.com/gujarati-blogs/events-across-gujarat/about-matrubhasha-abhiyan-and-its-activities/"]


i=15
# fun(url[0],i)
for u in url:
    try:
        fun(u,i)
    except:
        continue
    i+=1

# %%
import os
import csv

def text_files_to_csv(folder_path, output_csv):
    # List to store file data
    data = []
    num=1
    # Iterate through all the files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read().strip()  # Read and strip any trailing newlines
                if(content not in gujarati_bad_words):#filter bad words out
                    data.append([f"Serial number {num} :", content])  # Append file name and content as a row
                    num+=1
                else:
                    continue

    # Write data to a CSV file
    with open(output_csv, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['File Name', 'Content'])  # Write the header row
        writer.writerows(data)  # Write all rows

    # print(f"All text files have been successfully converted into '{output_csv}'.")
    # pd.to_

# Example usage

# folder_path = 'E:/NLP/Assignments/Gujarati_Artical_Dataset/Business/BBC business'  # Replace with the folder path
# # output_csv = 'bbc_business.csv'  # Replace with the desired output CSV file name
# folder_path="E:/NLP/Assignments/Gujarati_Artical_Dataset"
# for folder_name in os.listdir(folder_path):
#     for sub_folder_name in os.listdir(f"{folder_path}/{folder_name}"):
#         try:
#             text_files_to_csv(f"{folder_path}/{folder_name}/{sub_folder_name}", f"{sub_folder_name}.csv")
#         except:
#             continue


# text_files_to_csv("E:/NLP/fake and real news data/Gujarati_fake_news","fake_news.csv")
text_files_to_csv("E:/NLP/fake and real news data/Gujarati_real_news","real_news.csv")

# %%


# %% [markdown]
# Creating dataframe with two cols (source link of data, size of data taken from it)

# %%
#size of data is in MBs
dict={"https://www.gujaratilexicon.com":"5",
      "https://gujarati.news18.com/":"1",
      "https://www.newspremi.com/":"1",
      "https://huggingface.co/":"200",
      "https://www.bbc.com/news":"78 ",
      "https://chitralekha.com/":"174",
      "https://gujaratexclusive.in/":"7",
      "https://www.gujaratpost.in/":"105",
      "https://www.gujarattak.in/": "120",
      "https://epaper.gujarattimesusa.com/":"35",
      "https://indianexpress.com/":"235",
      "https://www.kaltak24.com/":"7",
      "https://tv9gujarati.com/live-tv":"20",
      "https://www.magicbricks.com/":"40",
      "https://mantavyanews.com/":"400",
      "https://morbiupdate.com/":"320",
      "https://www.navajivan.in/":"90",
      "https://nbs.net/":"15",
      "https://www.opindia.com/category/international/":"283",
      "https://theeconomicbusiness.com/":"78",
      "https://trishulnews.com/":"231",
      "https://www.westerntimes.co.in/":"107",
      "https://www.kaggle.com/":"118"
      }


