from jinja2 import Environment, FileSystemLoader, select_autoescape
import pandas as pd
import numpy as np
import os

# Filenames
courseTemplateFilename = "templates/course_template.html"
indexTemplateFilename = "templates/index_template.html"
dataFilename = "data/phy_courses.csv"
instructorDataFilename = "data/phy_instructors.csv"
# addResourcesFilename = "addresources.csv"
indexFilename = "index.html"

# Import data

def preprocessing(csv_file):
    df = pd.read_csv(csv_file, delimiter=",", header=0)  #reads the .csv file and uses 1st row as header
    df.replace(np.nan, "", regex=True, inplace=True) # replace all null values with blank
    return df

courses = preprocessing(dataFilename)
instData = preprocessing(dataFilename)

courses.rename(columns = {'id':'courseid'}, inplace = True)  # renamed column 'id' to 'courseid'
courses_master_df = pd.merge(courses,instData,how='inner',on='courseid')   # merging the two dataframes based on column 'courseid'
courses = courses_master_df.to_dict('records')   # converted merged dataframe to a dictionary that is list-like ('records')


# Jinja Setup
env = Environment(loader=FileSystemLoader(os.path.abspath(".")), autoescape=select_autoescape(["html"]))
courseTemplate = env.get_template(courseTemplateFilename)
indexTemplate = env.get_template(indexTemplateFilename)

# Start working
for course in courses:
    # print("course:", course)
    # print()
    course["coursehtml"] = courseTemplate.render(course=course)
    # print("courseinfo:", course["courseinfo"])

output = indexTemplate.render(courses=courses)

with open(indexFilename, "w") as outfile:
    outfile.write(output)

print("Tasked Completed Successfully!")
