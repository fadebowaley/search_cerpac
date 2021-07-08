from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pprint import pprint
from urllib.parse import urljoin
import webbrowser
# from api import get_all_forms, get_form_details, session
#iniatialise an http session

session = HTMLSession()
url = "http://knowyourimmigrationstatus.ng/FormStatusDetails.aspx"
# url = "http://knowyourimmigrationstatus.ng/KnowStatusCerpac.aspx" 
# url =" http://knowyourimmigrationstatus.ng/KnowFormStatus.aspx"
# url = "https://www.wikipedia.org/"

# url = "https://www.google.com/"


def get_all_forms(url):
    res = session.get(url)
    # res.html.render
    soup = BeautifulSoup(res.html.html, "html.parser")
    form = soup.find_all('form', id_="form1")
    # return soup.find_all('form')
    return soup.find_all('form')

def get_form_details(form):
    details = {}
    action = form.attrs.get("action").lower()
    # print(action)
    method = form.attrs.get("method", "get").lower()
    inputs = []
    for input_tag in form.find_all("input"):        
        input_type = input_tag.attrs.get("type", "text").lower()
        input_name = input_tag.attrs.get("name")
        input_value = input_tag.attrs.get("value", "")
        inputs.append({"type": input_type, "name": input_name, "value": input_value})
    details["actions"]  = action
    details["method"] = method
    details["inputs"] = inputs
    return details
        


forms = get_all_forms(url)
for i , form in enumerate(forms, start=1):
    form_details = get_form_details(form)
    print("="*50, f"form #{i}", "="*50)  
    print(form_details)   
        


# get the first form
first_form = get_all_forms(url)[0]
# extract all form details
form_details = get_form_details(first_form)
pprint(form_details)

# the data body we want to submit
data = {}
for input_tag in form_details["inputs"]:
    # if input_tag["type"] == "hidden" :
        # if it's hidden, use the default value
        data[input_tag["name"]] = input_tag["value"]
        
    # elif input_tag["type"] != "submit" :
        # all others except submit, prompt the user to set it
        value = input(f"Enter the value of the field '{input_tag['name']}' (type: {input_tag['type']}): ")
        data[input_tag["name"]] = value
        
action = form.attrs.get("action").lower()

# url = "http://knowyourimmigrationstatus.ng/KnowStatusCerpac.aspx" 
# url = "http://knowyourimmigrationstatus.ng/KnowFormStatus.aspx"
# url = "https://www.wikipedia.org/"
# url = "https://www.google.com/"

# join the url with the action (form request URL)
url = urljoin(url, action)
# url = urljoin(url, form_details["action"])
print(url)

if form_details["method"] == "post":
    res = session.post(url, data=data)
elif form_details["method"] == "get":
    res = session.get(url, params=data)

# the below code is only for replacing relative URLs to absolute ones
soup = BeautifulSoup(res.content, "html.parser")
for link in soup.find_all("link"):
    try:
        link.attrs["href"] = urljoin(url, link.attrs["href"])
    except:
        pass
for script in soup.find_all("script"):
    try:
        script.attrs["src"] = urljoin(url, script.attrs["src"])
    except:
        pass
for img in soup.find_all("img"):
    try:
        img.attrs["src"] = urljoin(url, img.attrs["src"])
    except:
        pass
for a in soup.find_all("a"):
    try:
        a.attrs["href"] = urljoin(url, a.attrs["href"])
    except:
        pass

open("page.html", "w",  encoding='utf-8').write(str(soup))
# open the page on the default browser
webbrowser.open("page.html")    