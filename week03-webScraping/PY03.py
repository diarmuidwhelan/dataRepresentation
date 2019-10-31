from bs4 import BeautifulSoup 
 
with open("C:/Users/Diarmuid/Documents/GMIT_DATA_ANALYTICS/Data_Representation/Labs/Lab-02.html") as fp:     
    soup = BeautifulSoup(fp,'html.parser') 
print(soup.prettify()) 
