import requests


# Function to send calls to searchcode.com API
def sendAPICall(query):
    url = "https://searchcode.com/api/codesearch_I/?"
    for i in range(len(query)):
        url = url + "&" + query[i]
    try:
        response = requests.get(url)
        return response.json()

    except requests.exceptions.RequestException as e:
        print(e)
        return None


# Function to automatically populate the query request to pass to the API
def createQuery(params):
    query = []
    for i in params:
        query.append(i)


"""
Query parameters: [q: search term
Filter by file extension ext:EXTENTION E.g. "gsub ext:erb"
Filter by language lang:LANGUAGE E.g. "import lang:python"
Filter by repository repo:REPONAME E.g. "float Q_rsqrt repo:quake"
Filter by user/repository repo:USERNAME/REPONAME E.g. "batf repo:boyter/batf"
p: result page starting at 0 through to 49
callback: callback function (JSONP only)
per_page: number of results wanted per page max 100
lan: allows filtering to languages supplied by return types. Supply multiple to filter to multiple languages.
src: allows filtering to sources supplied by return types. Supply multiple to filter to multiple sources.
loc: filter to sources with greater lines of code then supplied int. Valid values 0 to 10000.
loc2: filter to sources with less lines of code then supplied int. Valid values 0 to 10000.]
"""
query = ["q=nh2seven", "p=0", "per_page=100"]
result = sendAPICall(query)
if result:
    print(result)
else:
    print("An error occurred.")
