import numpy as np
import xarray as xr
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import cartopy.crs as crs
import cartopy.feature as cfeature
import os
import io

class Fall3D:
    def __init__(self,path,fname):
        self.path  = path
        self.fname = fname
        self.ds    = None

        # Properties
        self._key      = "tephra_col_mass"
        self._minval   = 0.0
        self._maxval   = 1.0
        self._step     = 0.1
        self._log      = False
        self._auto     = False

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self,value):
        self._key = value

    @property
    def minval(self):
        return self._minval

    @minval.setter
    def minval(self,value):
        self._minval = value

    @property
    def maxval(self):
        return self._maxval

    @maxval.setter
    def maxval(self,value):
        self._maxval = value

    @property
    def step(self):
        return self._step

    @step.setter
    def step(self,value):
        self._step = value

    @property
    def log(self):
        return self._log

    @log.setter
    def log(self,value):
        self._log = value

    @property
    def auto(self):
        return self._auto

    @auto.setter
    def auto(self,value):
        self._auto = value

    def load(self):
        """Open an xarray dataset from a file, returning False if the file doesn't exist."""
        ###
        ### Read file
        ###
        if not self.ds is None:
            return True

        filepath = os.path.join(self.path,self.fname)
        if not os.path.isfile(filepath):
            # If the file doesn't exist, return False
            return False
        
        try:
            # Try to open the dataset
            self.ds = xr.open_dataset(filepath)
            return True
        except FileNotFoundError:
            # Return False if file not found or any issue occurs
            return False
        except Exception as e:
            # Handle any other exceptions that might occur
            print(f"An error occurred: {e}")
            return False

    def get_times(self):
        nt = self.ds.sizes['time']
        return [it for it in range(nt)]

    def get_vars(self):
        dims = ('time','lat','lon')
        vars = [s for s,v in self.ds.data_vars.items() if dims==v.dims]
        return vars

    def plot(self,it):
        key = self.key
        ###
        ### Generate map
        ###
        proj = crs.PlateCarree()
        fig, ax = plt.subplots( subplot_kw={'projection': proj} )
        ###
        ### Add map features
        ###
        BORDERS = cfeature.NaturalEarthFeature(
                scale     = '10m',
                category  = 'cultural',
                name      = 'admin_0_countries',
                edgecolor = 'gray',
                facecolor = 'none'
                )
        LAND = cfeature.NaturalEarthFeature(
                'physical', 'land', '10m',
                edgecolor = 'none',
                facecolor = 'lightgrey',
                alpha     = 0.8
                )
        
        ax.add_feature(LAND,zorder=0)
        ax.add_feature(BORDERS, linewidth=0.4)
        ###
        ### Add grid lines
        ###
        gl = ax.gridlines(
            crs         = crs.PlateCarree(),
            draw_labels = True,
            linewidth   = 0.5,
            color       = 'gray',
            alpha       = 0.5,
            linestyle   = '--')
        gl.top_labels    = False
        gl.right_labels  = False
        gl.xlabel_style  = {'fontsize': 7}
        gl.ylabel_style  = {'fontsize': 7,
                            'rotation': 90}
        ###
        ### Plot contours
        ###
        ds = self.ds
        cmap = plt.cm.RdYlBu_r
        time_fmt = ds.isel(time=it)['time'].dt.strftime("%d/%m/%Y %H:%M").item()
        ax.set_title(time_fmt, loc='right')

        if self.auto:
            fc = ax.contourf(
                ds.lon,ds.lat,ds.isel(time=it)[key],
                cmap      = cmap,
                transform = crs.PlateCarree())
        else:
            levels = np.arange(0.0,self.maxval+self.step,self.step)
            print('0:',self.maxval)
            print('1:',levels)
            if self.minval > 0:
                levels = [l for l in levels if l>self.minval]
                levels.insert(0,self.minval)
            print('2:',levels)
            fc = ax.contourf(
                ds.lon,ds.lat,ds.isel(time=it)[key],
                levels    = levels,
                norm      = BoundaryNorm(levels,cmap.N),
                cmap      = cmap,
                extend    = 'max',
                transform = crs.PlateCarree())
    
        ###
        ### Generate colorbar
        ###
        label = ds[key].long_name
        cbar=fig.colorbar(fc,
            orientation = 'vertical',
            label       = label,
            )
    
        ###
        ### Output plot
        ###
        #fname = f"map_{it:03d}.png"
        #filepath = os.path.join('app/static/',fname)
        #plt.savefig(filepath,dpi=300,bbox_inches='tight')

        # Save the figure to a bytes buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)

        return buf

if __name__ == "__main__":
    path = "/home/lmingari/fall3d/flask/default"
    fname = "config.res.nc"
    obj = Fall3D(path,fname)
    obj.load()
#    print(obj.ds)
    print(obj.get_vars())
    print(obj.get_times())
    
    obj.plot(it=5)

###
### Parameters
###

#vlon, vlat      = 15.0, 37.75

###
### Set mininmum level
###

###
### Add vent location
###
#ax.plot(vlon,vlat,color='red',marker='^')
