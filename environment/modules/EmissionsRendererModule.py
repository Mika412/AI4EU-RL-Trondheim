from abc import abstractmethod
from .BaseModule import BaseModule
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.colors import ListedColormap
from environment.modules.EmissionsModule import EmissionType
from mpl_toolkits.axes_grid1 import make_axes_locatable
import math 

class EmissionColors:
	good = np.array([0, 153/255, 102/255, 1])
	moderate = np.array([255/255, 153/255, 51/255, 1])
	unhealthy_special = np.array([255/255, 222/255, 51/255, 1])
	unhealthy = np.array([204/255, 0, 51/255, 1])
	vunhealthy = np.array([102/255, 0, 153/255, 1])
	hazardous = np.array([126/255, 0, 35/255, 1])


class EmissionsRendererModule(BaseModule):
        def __init__(self, emissions, emission_types = [], save_to_file=False):
                super().__init__()

                self.emissions = emissions
                self.emission_types = emission_types

                self.max_values = {"CO":1000,"CO2":10000, "NOx": 400, "HC": 10, "PMx": 1}
                
                plt.ion()
                
                self.axs = []
                self.imgs = []
                self.cbars = []
                
                self.fig = plt.figure()
		
                num_rows = max(int(round(math.sqrt(len(self.emission_types)))), 1)
                num_cols = int(ceil(len(self.emission_types)/num_rows))


                """ Create new emission plots"""
                for i, emission_type in enumerate(emission_types):
                        ax = subplot(num_rows, num_cols, i+1)
                        ax.set_title(str(emission_type))
                        ax.get_xaxis().set_visible(False)
                        ax.get_yaxis().set_visible(False)
                        
                        cmap = self.get_emissions_colormap(emission_type)
                        im = ax.imshow(np.flip(emissions.get_emissions_type_matrix(emission_type),0), cmap=cmap, vmin=0, vmax=self.max_values[str(emission_type)])
                        divider = make_axes_locatable(ax)
                        cax = divider.append_axes("right", size="5%", pad=0.05)
                        cbar = self.fig.colorbar(im, cax=cax)
                        cbar.set_clim(vmin=0,vmax=self.max_values[str(emission_type)])
                        cbar.draw_all()
                        
                        self.axs.append(ax)
                        self.imgs.append(im)
                        
                        
                plt.show(block=False)
                
        def get_emissions_colormap(self, emission_type):
                emissions_switcher = {
                        EmissionType.CO: 	self._CO_colorbar,
                        EmissionType.CO2: 	self._CO2_colorbar,
                        EmissionType.NOx: 	self._NOx_colorbar,
                        EmissionType.HC: 	self._HC_colorbar,
                        EmissionType.PMx: 	self._PMx_colorbar
                }
                return emissions_switcher.get(emission_type, lambda: 0)

        @property
        def _CO_colorbar(self):
                viridis = cm.get_cmap('viridis')
                _colors = viridis(np.linspace(0, 1, self.max_values['CO']))

                _colors[:, :]             	= EmissionColors.hazardous
                _colors[:int(20000/24), :]    = EmissionColors.vunhealthy
                _colors[:int(15000/24), :]    = EmissionColors.unhealthy
                _colors[:int(10000/24), :]    = EmissionColors.moderate
                _colors[:int(7500/24), :]    	= EmissionColors.unhealthy_special
                _colors[:int(5000/24), :]    	= EmissionColors.good
                return ListedColormap(_colors)
	
        @property
        def _CO2_colorbar(self):
                viridis = cm.get_cmap('viridis')
                return ListedColormap(viridis.colors)

        @property
        def _NOx_colorbar(self):
                viridis = cm.get_cmap('viridis')
                _colors = viridis(np.linspace(0, 1, self.max_values['NOx']))
                
                # _colors[:, :]             	= EmissionColors.hazardous
                # _colors[:int(40/24), :]    	= EmissionColors.vunhealty
                # _colors[:int(90/24), :]    	= EmissionColors.unhealthy
                # _colors[:int(120/24), :]    = EmissionColors.moderate
                # _colors[:int(230/24), :]    = EmissionColors.unhealthy_special
                # _colors[:int(340/24), :]    = EmissionColors.good
                _colors[:, :]             	= EmissionColors.good
                _colors[50:99, :]    = EmissionColors.unhealthy_special
                _colors[100:149, :]    = EmissionColors.moderate
                _colors[150:199, :]    = EmissionColors.unhealthy
                _colors[200:299, :]    = EmissionColors.vunhealthy
                _colors[300:self.max_values['NOx'], :] = EmissionColors.hazardous
                #import pdb;pdb.set_trace()
                return ListedColormap(_colors)

        @property
        def _HC_colorbar(self):
                viridis = cm.get_cmap('viridis')
                return ListedColormap(viridis.colors)

        @property
        def _PMx_colorbar(self):
                viridis = cm.get_cmap('viridis')
                return ListedColormap(viridis.colors)

        @property
        @abstractmethod
        def variable_name(self):
                return "emissions_renderer"

        @abstractmethod
        def step(self, timestep):
                self.fig.suptitle("Timestep: " + str(timestep))
                for i,emission_type in enumerate(self.emission_types):
                        ax = self.axs[i]
                        #import pdb; pdb.set_trace()
                        #print(self.emissions.get_emissions_type_matrix(emission_type))
                        self.imgs[i].set_data(np.flip(self.emissions.get_emissions_type_matrix(emission_type),0))

                plt.draw()
                plt.pause(1e-3)
	        
        @abstractmethod
        def reset(self):
                pass
        
