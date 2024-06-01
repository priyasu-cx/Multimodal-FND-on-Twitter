# importing required packages for this section
import re
import whois
import urllib
import urllib.request
from datetime import datetime
import requests
from urllib.parse import urlsplit, urlparse
import ipaddress
from datetime import datetime, timedelta


# 1.Domain of the URL (Domain)
def getDomain(url):
    domain = urlparse(url).netloc
    if re.match(r"^www.", domain):
        domain = domain.replace("www.", "")
    return domain


# 2.Checks for IP address in URL (Have_IP)
def havingIP(url):
    domain = urlparse(url).netloc
    # print("Domain:",domain)
    try:
        ipaddress.ip_address(domain)
        ip = 1
    except:
        ip = 0
    # print("Have IP:",ip)
    return ip


# 3.Checks the presence of @ in URL (Have_At)
def haveAtSign(url):
    if "@" in url:
        at = 1
    else:
        at = 0
    return at


# 4.Finding the length of URL and categorizing (URL_Length)
def getLength(url):
    if len(url) < 54:
        length = 0
    else:
        length = 1
    return length


# 5.Gives number of '/' in URL (URL_Depth)
def getDepth(url):
    s = urlparse(url).path.split("/")
    depth = 0
    for j in range(len(s)):
        if len(s[j]) != 0:
            depth = depth + 1
    return depth


# 6.Checking for redirection '//' in the url (Redirection)
def redirection(url):
    pos = url.rfind("//")
    if pos > 6:
        if pos > 7:
            return 1
        else:
            return 0
    else:
        return 0


# 7.Existence of “HTTPS” Token in the Domain Part of the URL (https_Domain)
def httpDomain(url):
    domain = urlparse(url).netloc
    if "https" in domain:
        return 1
    else:
        return 0


# listing shortening services
shortening_services = (
    r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|"
    r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|"
    r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|"
    r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|"
    r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|"
    r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|"
    r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|"
    r"tr\.im|link\.zip\.net"
)


# 8. Checking for Shortening Services in URL (Tiny_URL)
def tinyURL(url):
    match = re.search(shortening_services, url)
    if match:
        return 1
    else:
        return 0


# 9.Checking for Prefix or Suffix Separated by (-) in the Domain (Prefix/Suffix)
def prefixSuffix(url):
    if "-" in urlparse(url).netloc:
        return 1  # phishing
    else:
        return 0  # legitimate


# 11.DNS Record availability (DNS_Record)
# obtained in the featureExtraction function itself


# 12.Web traffic (Web_Traffic)
def web_traffic(url):
    try:
        # Filling the whitespaces in the URL if any
        url = urllib.parse.quote(url)

        # {"domain":"oracle.com","rank":77}
        res = requests.get("https://api.visitrank.com/ranks/" + url)
        rank = res.json()["rank"]
        # print("Rank:",rank)

    except TypeError:
        return 1
    if rank > 100000 | rank == 0:
        return 1
    else:
        return 0


# 13.Survival time of domain: The difference between termination time and creation time (Domain_Age)
def domainAge(domain):
    try:
        # Query WHOIS information for the domain
        domain_info = whois.whois(domain)

        # Extract the creation and expiration dates
        creation_date = domain_info.creation_date
        expiration_date = domain_info.expiration_date

        # Handle cases where creation_date or expiration_date are lists
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        if isinstance(expiration_date, list):
            expiration_date = expiration_date[0]

        # Check if both dates are available
        if creation_date and expiration_date:
            # Calculate the domain age
            domain_age = expiration_date - creation_date

            # Check if the domain age is less than 12 months (365 days)
            if domain_age < timedelta(days=365):
                return 1  # Phishing
            else:
                return 0  # Legitimate
        else:
            print("Creation date or expiration date is missing.")
            return 1  # Error in fetching necessary dates
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1  # Error in fetching WHOIS information


# 14.End time of domain: The difference between termination time and current time (Domain_End)
def domainEnd(domain):
    try:
        # Query WHOIS information for the domain
        domain_info = whois.whois(domain)

        # Extract the expiration date
        expiration_date = domain_info.expiration_date

        if isinstance(expiration_date, list):
            expiration_date = expiration_date[
                0
            ]  # Handle cases where expiration_date is a list

        # Calculate the remaining time until expiration
        current_date = datetime.now()
        remaining_time = expiration_date - current_date

        # Check if the remaining time is less than 6 months (180 days)
        if remaining_time < timedelta(days=180):
            return 1  # Phishing
        else:
            return 0  # Legitimate
    except Exception as e:
        print(f"An error occurred: {e}")
        return 1  # Error in fetching WHOIS information


# 15. IFrame Redirection (iFrame)
def iframe(response):
    if response == "":
        return 1
    else:
        if re.findall(r"[<iframe>|<frameBorder>]", response.text):
            return 0
        else:
            return 1


# 16.Checks the effect of mouse over on status bar (Mouse_Over)
def mouseOver(response):
    if response == "":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return 1
        else:
            return 0


# 17.Checks the status of the right click attribute (Right_Click)
def rightClick(response):
    if response == "":
        return 1
    else:
        try:
            if response.status_code == 200:
                page_source = response.text

                # Search for the specific event pattern in the page source
                if "event.button==2" in page_source or "oncontextmenu" in page_source:
                    return 1  # Phishing
                else:
                    return 0  # Legitimate
            else:
                print(
                    f"Failed to retrieve the webpage. Status code: {response.status_code}"
                )
                return 1  # Error in fetching webpage
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return 1  # Error in fetching webpage


# 18.Checks the number of forwardings (Web_Forwards)
def forwarding(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1


def get_domain_from_url(url):
    split_url = urlsplit(url)
    domain = split_url.netloc
    # print(domain)
    return domain


# URL Feature Extraction
# Function to extract features
def featureExtraction(url):

    features = []

    # features.append(url)  # 1
    # Address bar based features (10)
    # features.append(getDomain(url))  # 2
    features.append(havingIP(url))  # 3
    features.append(haveAtSign(url))  # 4
    features.append(getLength(url))  # 5
    features.append(getDepth(url))  # 6
    features.append(redirection(url))  # 7
    features.append(httpDomain(url))  # 8
    features.append(tinyURL(url))  # 9
    features.append(prefixSuffix(url))  # 10

    # Domain based features (4)
    dns = 0
    try:
        domain_name = whois.whois(urlparse(url).netloc)
        # Check if the response contains null values
        if all(value is None for value in domain_name.values()):
            dns = 1
    except:
        dns = 1

    # print("DNS", dns)

    features.append(dns)  # 11

    domain = get_domain_from_url(url)

    # print("Domain:", domain)

    features.append(web_traffic(domain))  # 12
    features.append(1 if dns == 1 else domainAge(domain))  # 13
    features.append(1 if dns == 1 else domainEnd(domain))  # 14

    # print(url)

    # HTML & Javascript based features (4)
    try:
        response = requests.get(url, timeout=10)  # Set a timeout (in seconds)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
    except requests.Timeout:
        print(f"Timeout occurred while making the request to {url}")
        response = ""
    except:
        response = ""

    features.append(iframe(response))  # 15
    features.append(mouseOver(response))  # 16
    features.append(rightClick(response))  # 17
    features.append(forwarding(response))  # 18
    # features.append(label)  # 19

    return features


# Test the function
# url = "https://www.google.com"

# print(featureExtraction(url))
