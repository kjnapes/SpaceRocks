from astropy.table import Table
import pandas as pd
import numpy as np
from astropy.time import Time
import copy

import dateutil

class Convenience:

    def __len__(self):
        '''
        This method allows you to use the len() function on a SpaceRocks object.
        '''
        return len(self.name)


    def __getitem__(self, idx):
        '''
        This method allows you to index a SpaceRocks object.
        '''
        p = copy.copy(self)
        for attr in self.__dict__.keys():
            setattr(p, attr, getattr(self, attr)[idx])

        return p


    def detect_timescale(self, timevalue, timescale):
        if isinstance(timevalue[0], str):
            dates = [dateutil.parser.parse(d, fuzzy_with_tokens=True)[0] for d in timevalue]
            return Time(dates, format='datetime', scale=timescale)
        elif np.all(timevalue > 100000):
            return Time(timevalue, format='jd', scale=timescale)
        else:
            return Time(timevalue, format='mjd', scale=timescale)

    def detect_coords(self, kwargs):

        kep = ['a', 'e', 'inc', 'node', 'arg', 'm', 'f', 'varpi', 't_peri']
        xyz = ['x', 'y', 'z', 'vx', 'vy', 'vz']
        abg = ['alpha', 'beta', 'gamma', 'dalpha', 'dbeta', 'dgamma']

        input_coords = list(kwargs.keys())

        if np.in1d(input_coords, kep).sum() == 6:
            coords = 'kep'

        elif np.in1d(input_coords, xyz).sum() == 6:
            coords = 'xyz'

        elif np.in1d(input_coords, abg).sum() == 6:
            coords = 'abg'

        else:
            raise ValueError('Invalid input coordinates. Please see the documentation for accepted input.')

        return coords



    def astropy_table(self):
        '''
        Write the rocks to an astropy table. This can handle units, though
        it is generally less elegant than pandas.
        '''
        return Table(self.__dict__)


    def pandas_df(self):
        '''
        Write the rocks to a pandas dataframe. Pandas can't handle astropy
        units (yet), so if you want to keep units intact you'll have to use
        an Astropy Table. to_pandas()
        '''
        return self.astropy_table().to_pandas()
