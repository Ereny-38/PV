#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np


# In[2]:


import pandas as pd


# In[3]:


import matplotlib.pyplot as plt


# In[4]:


import pvlib


# In[5]:


from pvlib.pvsystem import PVSystem


# In[6]:


from pvlib.location import Location


# In[7]:


from pvlib.modelchain import ModelChain


# In[8]:


from pvlib.temperature import TEMPERATURE_MODEL_PARAMETERS


# In[9]:


temperature_model_parameters = TEMPERATURE_MODEL_PARAMETERS['sapm']['open_rack_glass_glass']


# In[10]:


sandia_modules = pvlib.pvsystem.retrieve_sam('SandiaMod')


# In[11]:


cec_inverters = pvlib.pvsystem.retrieve_sam('cecinverter')


# In[12]:


sandia_module = sandia_modules['Canadian_Solar_CS5P_220M___2009_']


# In[13]:


sandia_module


# In[14]:


cec_inverter = cec_inverters['ABB__MICRO_0_25_I_OUTD_US_208__208V_']


# In[15]:


location = Location(latitude=52, longitude=13, name='Berlin',tz='Europe/Berlin')


# In[16]:


print(location)


# In[17]:


system = PVSystem(surface_tilt=20, surface_azimuth=200,
  module_parameters=sandia_module,inverter_parameters=cec_inverter,temperature_model_parameters=temperature_model_parameters,modules_per_string = 70,strings_per_inverter = 3)


# In[18]:


mc = ModelChain(system, location)


# In[19]:


print(mc)


# In[20]:


weather =pd.read_csv (r'F:\TU BERLIN\3rd semester\Thesis\Termin 4-Schmid\Schmid email\irradiation-refined.csv',header=None,names=['timestamp','ghi','dni','dhi'],index_col=0,parse_dates=True)


# In[21]:


weather


# In[22]:


mc.run_model(weather);


# In[23]:


mc.cell_temperature
mc.cell_temperature.plot()
plt.xlabel("Time(Sec)")
plt.ylabel("Temp(C)")


# In[24]:


mc.dc.plot()
plt.xlabel("Time(Sec)")
plt.ylabel("P_DC(W)")


# In[25]:


mc.dc.loc['2010-1-22':'2010-2-1'].plot()


# In[26]:


mc.dc.describe()


# In[27]:


mc.dc['p_mp'].sum()


# In[36]:


mc.ac.plot()
plt.xlabel("Time(Sec)")
plt.ylabel("P_AC(W)")


# In[29]:


weather['ghi'].plot()
plt.xlabel("Time(Sec)")
plt.ylabel("Irradiance(Wh/m2)")


# In[30]:


Energy=weather['ghi']*.13*10


# In[31]:


Energy.plot()
plt.xlabel("Time(Sec)")
plt.ylabel("Energy(Wh)")


# In[32]:


#Alternatively, we could have specified single diode or PVWatts related information in the PVSystem
#pvwatts_system = PVSystem(module_parameters={'pdc0': 240, 'gamma_pdc': -0.004},inverter_parameters={'pdc0': 240},temperature_model_parameters=temperature_model_parameters)
#ModelChain still needs us to specify aoi_model and spectral_model keyword arguments 
#because the system.module_parameters dictionary does not contain enough information to determine which of those models to choose.
#mc = ModelChain(pvwatts_system, location,aoi_model='physical', spectral_model='no_loss')

