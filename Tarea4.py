#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np #se importan las librerias a utlizar en el script
import pandas as pd


# # 1. 
# Creación del dataframe

# In[2]:


data=pd.read_csv("exoplanets.csv",low_memory=False) #se importa el archivo que contiene los datos de los exoplanetas
a=pd.DataFrame([data["NAME"],data["TEFF"],data["MASS"],data["A"],
               data["DENSITY"],data["R"],data["STAR"],data["MSTAR"],data["RSTAR"]
               ,data["BINARY"]])       #se crea un DF con los datos 
DF=pd.DataFrame.transpose(a) #se ordenan los datos por columnas


# # 2.
# Descarte los sistemas binarios BINARY==0.

# In[3]:


DF=DF.dropna(subset=["BINARY"]) #se eliminan las entradas NaN

for i in range(3263):
    if DF['BINARY'][i]==1:
        DF=DF.drop(index=i)  #se borran las entradas BINARY==1 que son los sistemas binarios 
        
DF=DF.reset_index()
DF = DF.drop(['index'], axis=1) #Borramos las columnas innecesarias
DF


# # 3.
# La masa de esos planetas esta expresada en masas de jupiter, cree otra
# columna que se llame MASSE en unidades de masa de la tierra.

# In[4]:


DF.insert(9,"MASSE",DF["MASS"]*317.8) #se crea la columna MASSE en unidades de masa de la tierra
DF


# # 4.
# Similarmente el radio de los planetas está expresada en términos del
# radio de Júpiter, cree otra columna llamada RE, con los radios expresados
# en radios terrestres.

# In[5]:


DF.insert(10,"RE",DF["R"]*11.2)#se crea la columna RE con el radio del planeta en unidades de radios terrestres 
DF


# # 5.
# Teniendo en cuenta que la luminosidad de una estrella se puede calcular como $L=4\pi R^2\sigma T_{eff}^4$, donde $R$ es el radio de la estrella, $\sigma$ la constante
# de Stefan-Boltzmann (Recuerde usar las unidades correctas). Cree otra columna llámela LUM y llénela con las luminosidades de las estrellas.

# In[6]:


DF.insert(11,"LUM",(4*np.pi*DF["RSTAR"]**2*(5.6704e-8*6.697e8**2)*DF["TEFF"]**4)/3.828e26)#se crea la columna con la información sobre la luminosidad de cada estrella en unidades solares
DF


# # 6.
# Calcule los limites de la zona de habitabilidad y asigne a estos las
# columnas ri y ro.
# 
# $$ r_i=[r_{is}-a_{i}(T_{eff}-T_s)-b_i(T_{eff}-T_s)^2]\sqrt{L} $$
# 
# $$ r_o=[r_{os}-a_{o}(T_{eff}-T_s)-b_o(T_{eff}-T_s)^2]\sqrt{L} $$
# 
# $L$ es la luminosidad estelar en unidades solares, $T_{eff}$ es la temperatura efectiva estelar en kelvin, $T_s=5780$ temperatura efectiva del sol, $a_i=2.7619e^{-5}$, $b_i=3.8095e^{-9}$, $a_o=1.3786e^{-4}$, $b_o=1.4286e^{-9}$, $r_{is}=0.72$ y $r_{os}=1.77$. 

# In[7]:


DF.insert(12,"ri",(0.72-2.7619e-5*(DF["TEFF"]-5780)-3.8095e-9*(DF["TEFF"]-5780)**2)*DF["LUM"]**0.5) #se crean las columnas ri y ro que son los limites superior e inferior para la zona de habitabilidad
DF.insert(13,"ro",(1.77-1.3786e-4*(DF["TEFF"]-5780)-1.4286e-9*(DF["TEFF"]-5780)**2)*DF["LUM"]**0.5)
DF


# # 7.
# Selección de planetas con alta probabilidad de ser rocosos.

# In[8]:


Den = DF.query("DENSITY>=5") #se filtra la columna DENSITY para seleccionar los planetas rocosos
Den


# In[9]:


Den.insert(14,"HDZ",((2*Den["A"]-Den["ro"]-Den["ri"])/(Den["ro"]-Den["ri"])).astype(float)) #se crea la columna HDZ con la ecuación para estimar la zona de habitabilidad
Den                                                                                          #se convierten los valores en flotantes


# # 8.
# Filtro que seleccione los planetas dentro de la zona de habitabilidad. Muestre los resultados en una tabla.

# In[10]:


Habitables=Den.query("HDZ>=-1 and HDZ<=1") #se pone la condicion sobre la columna HDZ para filtrar los planetas habitables
Habitables


# # 9.
# Gráficas.

# In[17]:


Habitables.plot(kind="scatter",x= "MSTAR" ,y="A", title="Masa de la estrella Vs Distancia del planeta a su estrella")
#Por algún motivo al añadir el argumento kind="scatter" me saca el error ValueError: scatter requires x column to be numeric


# In[16]:


import matplotlib.pyplot as plt  #se grafica usando matplotlib debido al error usando la graficación de pandas
Mass=np.array(Habitables["MSTAR"].astype(float))
A=np.array(Habitables["A"].astype(float))

plt.scatter(Mass,A)
plt.xlabel("MASS")
plt.ylabel("A")
plt.title("Masa de la estrella Vs Distancia del planeta a su estrella")
plt.show()


# In[13]:


Habitables.plot(kind='hist',x="MASS",y="A",title="Distribución orbital de los planetas") #se grafican las columnas del DF como histogramas


# In[14]:


Habitables.plot(x="DENSITY",y="MSTAR",title="Densidad Vs Masa de la estrella")#se grafica como kind='line' por defecto


# In[15]:


Habitables.plot(x="A",y="TEFF",title="Distancia a la estrella Vs Temperatura efectiva")


# In[ ]:




