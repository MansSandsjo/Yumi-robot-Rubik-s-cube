#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np

class Combine:

    def sides(self, sides):
        """Join all the sides together into one single string.

        :param sides: dictionary with all the sides
        :returns: string
        """
        
        # rubiksCubeNumb = np.array([], dtype=int)
       
        combined = ''
        for face in 'FUBRLD':
            combined += ''.join(sides[face])
        
        return combined

combine = Combine()
    
   