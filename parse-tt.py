from bs4 import BeautifulSoup

htmlfile = "SWSCUST Programme Of Study Individual - allyr.html"
outfile = "NCY-TT.html"

weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri"]
courselist = ["4135","4136","3044","3032","4064","4076","4055"]
weeknum = list(range(4,10))
print(weeknum)


with open(htmlfile, 'r') as file:
    html_content = file.read()
    

soup = BeautifulSoup(html_content,"html.parser")


table = soup.find('table', {"border":"1"})
table_body = table.find('tbody')

headercol = []
rows = table_body.find_all('tr')
for row in rows:
    td = [ele for ele in row.find_all('td', {"rowspan":"1"}) if ele]
    for tag in td:
        remove = 1
        for course in courselist:
            if course in tag.get_text():
                remove = 0

        for wd in weekdays:
            if wd in tag.get_text():
                remove = 0

        if remove == 0 and len(weeknum) != 0:
            remove = 1
            children = tag.findChildren("td" , {"align":"right"})
            for weeks in [child.get_text() for child in children if child.get_text()[0].isdigit()]:
                # check each week of class ...
                for wn in weeknum:
                    # with desired week numbers
                    if wn in [int(w) for w in weeks.split(", ") if w.isdigit()]:
                        # non-range week
                        remove = 0
                        break
                    
                    for wrange in [w.split("-") for w in weeks.split(", ") if not w.isdigit()]:
                        # range week
                        if wn >= int(wrange[0]) and wn <= int(wrange[1]):
                            remove = 0
                            break
            
        if remove == 1:
            tag.clear()


with open(outfile, "wb") as f_output:
    f_output.write(soup.prettify("utf-8"))  
            
                
