#!/usr/bin/env python
# coding: utf-8

# ## Impotation des Packages Necessaire 

# In[1]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import boto3


# In[2]:


url= 'https://immobilier-au-senegal.com/list-layout/page/3/'


# In[3]:


#fonction

def upload_file_s3(file_path, bucket_name, object_name=None):
    if object_name is None:
        object_name = file_path

    s3 = boto3.client("s3")
    s3.upload_file(file_path, bucket_name, object_name)

## Recupere le code source de la page a Scapper
c_source=requests.get(url).text


# In[4]:

soup= BeautifulSoup(c_source, 'lxml')
# print(soup.prettify())


# In[5]:


article= soup.find('article', class_="rh_list_card")
print(article.prettify())


# In[6]:


## recuperation du Titre du premier article 
headline= article.h3.a.text
print(headline)


# In[7]:


## recuperation du Commentaire du premier article 
summarry= article.find('div', class_="rh_list_card__details_wrap").p.text
print(summarry)


# In[8]:


## recuperation du Status du premier article 
## Status veut dire si le terrain est en vente , en location ou c un terrain que l'on veut acheter
status= article.find('div', class_="rh_list_card__price").span.text
print(status)


# In[9]:


# ## recuperation du Prix du premier article 
price= article.find('div', class_="rh_list_card__price").p.text
print(price)


# ## Maintenant on va recuperer tous les Articles avec les differents champs ennonce ci-dessous

# In[10]:


csv_file= open('ajout_IAS_scrape.csv', 'w', encoding='utf-8')
csv_writer= csv.writer(csv_file)
csv_writer.writerow(['headline','summarry','status','price'])


# In[11]:


for article in soup.find_all('article', class_="rh_list_card"):
    headline= article.h3.a.text
    print(headline)
    summarry= article.find('div', class_="rh_list_card__details_wrap").p.text
    print(summarry)
    status= article.find('div', class_="rh_list_card__price").span.text
    print(status)
    price= article.find('div', class_="rh_list_card__price").p.text
    print(price)

    print()

    csv_writer.writerow([headline, summarry, status, price])
csv_file.close()

upload_file_s3("data/ajout_IAS_scrape.csv","m2dsia-pomane-mamadou","ajout_IAS_scrape.csv")
# In[ ]:




# In[14]:


# ## Concatener les fichiers Excel
# df1= pd.read_csv('fichier_final.csv')
# df2= pd.read_csv('ajout_IAS_scrape.csv')
# df_concatene = pd.concat([df1, df2], ignore_index=True)


# In[16]:


# df_concatene.to_csv('fichier_final.csv', index=False)


# In[ ]:


### Essayons avec la pagination


