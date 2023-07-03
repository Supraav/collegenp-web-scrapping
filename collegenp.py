import json
import requests
from bs4 import BeautifulSoup as bs
import requests
import json
import time
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright

HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
output_file='final.json'

#loading json file
with open('uni_collegelinks.json', 'r') as file:
    json_data = file.read()

links = json.loads(json_data)
data = {}

while True:
    # Looping through links of JSON
    for link in links:
        print("getting into link",link)
        result = requests.get(link, headers=HEADER)
        content = result.text
        soup = bs(content, "lxml")
        time.sleep(2)
        # Title (holds the title of college name, address, est date, and type of org)
        title = soup.find('div', class_='colz-name')

        # College name
        try:
            name=title.h1.get_text().strip()
            data['college_name'] = name
        except:
            pass

        #organizationtype(uni or college or school)
        try:
            if "university" in name.lower():
                data["organizationtype"]='UNIVERSITY'
            elif "college" in name.lower():
                data["organizationtype"]='COLLEGE'
            elif "school" in name.lower():
                data["organizationtype"]='SCHOOL'
            else:
                data["organizationtype"]='INDUSTRY'
        except:
            pass

        # Address start
        Address={'country':'Nepal'}

        #streetline address
        try:
            address = title.find_all('p')[0].text.strip()
            Address['street_line_address'] = address
        except:
            pass

        # District
        try:
            Address['district'] = address.split(",")[-1].strip()
        except:
            pass
        data['address']=address
        #Address end

        # Est date
        try:
            data['est_date'] = title.find_all('p')[1].text.replace('Estd. ', '').strip()
        except:
            pass

        # Ownership (type of org: private/public)
        try:
            data['type_of_org'] = title.find_all('p')[2].text.strip()
        except:
            pass


        # URL
        try:
            data['website'] = link
        except:
            pass

        # College logo
        try:
            college_logo = soup.find_all('div', class_='colz-logo')[0]['style']
            start_index = college_logo.index("('") + 2
            end_index = college_logo.index("')")
            data['logo'] = college_logo[start_index:end_index]
        except:
            pass

        # Contact, email, and phone
        try:
            contact_details = soup.find('div', class_='col-md-4 col-sm-6 col-xs-12')
            phone = []
            for li_element in contact_details.find_all('li'):
                span_element = li_element.find('span')
                # Phone
                if span_element and 'fa-phone' in span_element.get('class', []):
                    phone_number = li_element.get_text(strip=True)
                    phone.append(phone_number)
                # Email
                elif span_element and 'fa-globe' in span_element.get('class', []):
                    data['email'] = li_element.get_text(strip=True)
            data['phone'] = phone
        except:
            pass
        

        # Affiliations
        affiliations = []
        try:
            aff = soup.find('div', class_='section-content mt-3', id='affiliations')
            for item in aff.find_all('li'):
                affiliation = item.get_text(strip=True)
                affiliations.append(affiliation)
            data['affiliations'] = affiliations
        except:
            pass


        #courses
        data['course']=[]
        #finding the course links
        course_links=[]
        try:
            course_list=soup.find('div',class_='section-content mt-3',id='course-list')
            aaa=course_list.find('div',class_='tab-pane fade active show',id='all_courses')
            for li_element in aaa.find_all('li'):
                course_names=li_element.find('a')['href']
                course_links.append(course_names)
        except:
            pass
        #all course_links extracted from college div

        #looping for all courselinks
        try:
            for course_link in course_links:
                program={}
                course_result = requests.get(course_link, headers=HEADER)
                course_soup = bs(course_result.text, "lxml")
                time.sleep(1.5)

                #course-name
                course_name=course_soup.find('div',class_='clearfix')
                program['name']=course_name.find('h1').text

                #course-details
                course_div=course_soup.select_one('.clearfix.course-facts')
                inner_divs= course_div.find_all('div',class_='col-md-3 col-6 col-sm-3')

                for h5 in inner_divs:
                    h5_text=h5.find('h5').text
                    h4_text=h5.find("h4").text
                    if h5_text=='Course Level':
                        program['degree']=h4_text.replace(' Degree','')
                    elif h5_text=='Study Mode':
                        program['Study_mode']=h4_text
                    else:
                        program[h5_text]=h4_text

                # program[h5_text] = h5.find("h4").text
                # print(h5_text,": ", h5.find("h4").text)
                # print("course :",program,"***********")    
                # print('*************************************************')     
                data['course'].append(program)
        except:
            pass

        #saving into json
        try:
            results = []
            with open(output_file, 'r') as file:
                results = json.load(file)
            
            with open(output_file,'w') as file:
                results.append(data)
                json.dump(results, file, indent=3)
        except Exception as e:
            print("Error opening file,",e)
            results=[]
            with open(output_file, 'w') as file:
                results.append(data)
                json.dump(results, file, indent=3)
                
        print("finished scrapping url:",link)
        print('JSON data saved to', output_file)
        print('/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/*/* /n/n')

    # print(data)


        

