import netCDF4
from netCDF4 import Dataset, num2date
import pandas as pd
from geopy.distance import geodesic
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import numpy as np


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
            coords_4 = (metadata['lat'][-1],metadata['lon'][0])

            self.area = geodesic(coords_1, coords_2).meters * geodesic(coords_1, coords_4).meters

            self.area_per_grid = self.area/(len(metadata['lon'])*len(metadata['lat']))

            self.total_kg = (data['tp'][:,:,:]*self.area_per_grid)*1000
            
            self.kg_m2 = self.total_kg.sum(axis = (1,2))/self.area
        except Exception as e:
            print(f"An error occurred while loading data: {e}")

    def GenerateTable(self):

        print("Generates Two datasets: Total rainfall over timeframe, Averaged by Month")
        total_rainfall = pd.DataFrame({'kg_m2': self.kg_m2,'date': self.metadata['month']})
        total_rainfall['month_number'] = [date.month for date in self.metadata['dates']]
        """total_rainfall = pd.DataFrame({'rf_mm': data['tp'][:,:,:].sum(axis=(1,2)) * 1000,'date': metadata['month']})
        total_rainfall['mm_km2'] = total_rainfall['rf_mm']/self.area
        
        total_rainfall['mass_per_m2'] = self.mass_per_m2"""
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
        monthly_mean_mass = total_rainfall.groupby('month_number')['kg_m2'].mean() 

        # Create a DataFrame from the resulting Series with specified column names
        monthly_mean_mass = pd.DataFrame({
            'Month_number': monthly_mean_mass.index,
            'Monthly_Mass_Rainfall': monthly_mean_mass.values,
            'month' : monthly_mean_mass.index.map(month_dictionary)
        })

        return total_rainfall, monthly_mean_mass 
        




    def rain_plot(self,index):


        rainfall = self.data.variables['tp'] # get the variable
        rainfall_data = rainfall[index,:,:] # get the data
        lon = self.metadata['lon'] # get the longitude data
        lat = self.metadata['lat'] # get the latitude data

        plt.figure()
        plt.title(self.metadata['dates'][index])

        # Create a meshgrid for the coordinates
        lon_grid, lat_grid = np.meshgrid(lon, lat)

        # Plot the data using the coordinates
        plt.pcolormesh(lon_grid, lat_grid, rainfall_data)

        # Create the colorbar and set its label
        cbar = plt.colorbar()
        # Make label larger font
        cbar.ax.tick_params(labelsize=10)
        cbar.set_label('Meters of Rainfall')

        # Add axis labels
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')

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
        


    def average_rainfall_per_grid(self):
        """
        Calculate the average rainfall per grid point over the total time and plot it as a contour plot.
        
        Parameters:
        data_manager (data_manipulation): An instance of the data_manipulation class containing the rainfall data.
        """

        # Get the rainfall data
        rainfall_data = self.data.variables['tp'][:]

        # Calculate the average rainfall per grid point over the total time
        self.average_rainfall = np.mean(rainfall_data, axis=0)

        # Get longitude and latitude
        lon = self.metadata['lon']
        lat = self.metadata['lat']

        # Create a contour plot
        plt.figure(figsize=(10, 6))
        plt.contourf(lon, lat, self.average_rainfall, cmap='Blues')
        plt.colorbar(label='Average Rainfall (mm)')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Average Rainfall per Grid Point')
        plt.show()




        


            
        
            

