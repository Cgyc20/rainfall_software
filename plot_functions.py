import netCDF4
from netCDF4 import Dataset, num2date
import pandas as pd
from geopy.distance import geodesic
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


class data_manipulation():

    def __init__(self,data_path):
        #We want to initialise the data itself and also the dictionary
        #Containing the lon/lat values and also the dates

        try:
            data = netCDF4.Dataset(data_path)
            self.data = data
            time_val = self.data.variables['time']
            dates = num2date(time_val[:], units=time_val.units, calendar=time_val.calendar)

            dates_convert = [f"{date.year}-{date.month:02d}" for date in dates]

    
            metadata = {'lon' : data.variables['longitude'][:],
                    'lat' :  data.variables['latitude'][:],
                    'dates':dates,
                    'month':dates_convert}
            self.metadata= metadata
        
            #THis involves working out the area of the box ( using Geosedic class)
            coords_1 = (metadata['lat'][0],metadata['lon'][0])
            coords_2 = (metadata['lat'][0],metadata['lon'][-1])
            coords_3 = (metadata['lat'][-1],metadata['lon'][-1])
            coords_4 = (metadata['lat'][-1],metadata['lon'][0])

            self.area = geodesic(coords_1, coords_2).kilometers * geodesic(coords_1, coords_4).kilometers 
            #We can also make a dataframe of total rainfall over entire area
            total_rainfall = pd.DataFrame({'rf_mm': data['tp'][:,:,:].sum(axis=(1,2)) * 1000,'date': metadata['month']})

            total_rainfall['mm_km2'] = total_rainfall['rf_mm']/self.area
            total_rainfall['month_number'] = [date.month for date in metadata['dates']]


            month_dictionary = {1:'January', #Mapping the months to the labels
                    2:'February',
                    3:'March',
                    4:'April',
                    5:'May',
                    6:'June',
                    7:'July',
                    8:'August',
                    9:'September',
                    10:'October',
                    11:'November',
                    12:'December'}

            total_rainfall['month'] = total_rainfall['month_number'].map(month_dictionary)

            self.total_rainfall = total_rainfall #Define this within the class itself
        except Exception as e:
            print(f"An error occurred while loading data: {e}")


        

    def rain_plot(self,index):


        rainfall = self.data.variables['tp'] # get the variable
        rainfall_data = rainfall[index,:,:] # get the data
        plt.title(self.metadata['dates'][index])
        plt.imshow(rainfall_data)
        plt.show()
    
        print("The rainfall data in this region for date:",self.metadata['dates'][index])

    def geo_plot(self):
        
    # Define the latitude and longitude range for your area
        lat_min, lat_max = self.metadata['lat'][0],self.metadata['lat'][-1]
        lon_min, lon_max = self.metadata['lon'][0], self.metadata['lon'][-1]

        # Create a plot
        fig = plt.figure(figsize=(10, 6))
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

        # Add map features
        ax.add_feature(cfeature.COASTLINE)
        ax.add_feature(cfeature.BORDERS, linestyle=':')

        # Plot the area box
        ax.plot([lon_min, lon_max, lon_max, lon_min, lon_min],
                [lat_min, lat_min, lat_max, lat_max, lat_min],
                color='red', linewidth=2, transform=ccrs.PlateCarree())

        # Set the extent of the map
        ax.set_extent([lon_min-20, lon_max+20, lat_min-20, lat_max+20])

        # Add gridlines
        ax.gridlines(draw_labels=True, linestyle='--')

        plt.show()



    


        
    
        

