# -*- coding: utf-8 -*-
"""
.. module:: convert_SLS.py
   :platform: Unix
   :synopsis: Convert SLS TOMCAT TIFF files in data exchange.

Example on how to use the `xtomo_raw`_ module to read SLS TOMCAT TIFF raw tomographic data and save them as Data Exchange

:Author:
  `Francesco De Carlo <mailto: decarlof@gmail.com>`_

:Organization:
  Argonne National Laboratory, Argonne, IL 60439 USA

:Version: 2014.08.15

.. _xtomo_raw: dataexchange.xtomo.xtomo_importer.html
"""

# Data Exchange: https://github.com/data-exchange/data-exchange
import xtomo_importer as xtomo_imp 
import xtomo_exporter as xtomo_exp

import re

def main():

    tray = 'tray03'
    sample = 'Sam18'
    sample_name = 'Glypto_crem_5'


    hdf5_file_name = '/local/carmen/lorentz/stu/' + tray + '/hdf5/' + sample + '.h5'
    file_name = '/local/carmen/lorentz/stu/' + tray + '/' + sample + '/raw/' + sample_name + '_.h5'
    log_file = '/local/carmen/lorentz/stu/tray03/exp.log'

    source_name="Advanced Photon Source"
    source_mode="top-up"
    #source_datetime=None
    beamline="2-BM"
    #energy=None
    #current=None
    #actual_pixel_size=None
    experimenter_name="Stuart R Stock"
    experimenter_affiliation="Northwestern University Feinberg School of Medicine" 
    experimenter_email="s-stock@northwestern.edu"
    instrument_comment="Francesco De Carlo at decarlo@aps.anl.gov"  

    #Read SLS log file data
    file = open(log_file, 'r')
    for line in file:
        linelist=line.split()
        if len(linelist)>1:
            if (linelist[0]=="Number" and linelist[2]=="darks"):
                number_of_darks = int(linelist[4])
            elif (linelist[0]=="Number" and linelist[2]=="flats"):
                number_of_flats = int(linelist[4])
            elif (linelist[0]=="Number" and linelist[2]=="projections"):
                number_of_projections = int(linelist[4])
            elif (linelist[0]=="Rot" and linelist[2]=="min"):
                rotation_min = float(linelist[6])
            elif (linelist[0]=="Rot" and linelist[2]=="max"):
                rotation_max = float(linelist[6])
            elif (linelist[0]=="Angular" and linelist[1]=="step"):
                angular_step = float(linelist[4])
    file.close()

    white_start = 1
    white_end = 2
    projections_start = 2
    projections_end = projections_start + (int)((rotation_max -  rotation_min) / angular_step) + 1
    dark_start = projections_end + 1 
    dark_end = dark_start + number_of_darks
    projections_angle_end = 180 + angular_step
    
    print "DARK", dark_start, dark_end
    print "WHITE", white_start, white_end
    print projections_start, projections_end
    print projections_angle_end

    print file_name
    print log_file
    
    # Read raw data
    read = xtomo_imp.Import()
    data, white, dark, theta = read.xtomo_raw(file_name,
                                                       projections_start = projections_start,
                                                       projections_end = projections_end,
                                                       projections_angle_end = projections_angle_end,
                                                       projections_digits=5,
                                                       white_start = white_start,
                                                       white_end = white_end,
                                                       dark_start = dark_start,
                                                       dark_end = dark_end,
                                                       data_type = 'hdf5',
                                                       log='INFO'
                                                       )
    # Save data as dataExchange
    write = xtomo_exp.Export()
    write.xtomo_exchange(data = data,
                          data_white = white,
                          data_dark = dark,
                          theta = theta,
                          hdf5_file_name = hdf5_file_name,
                          source_name=source_name,
                          source_mode=source_mode, 
                          beamline = beamline,
                          experimenter_name=experimenter_name, 
                          experimenter_affiliation=experimenter_affiliation, 
                          experimenter_email=experimenter_email, 
                          instrument_comment=instrument_comment,  
                          sample_name = sample_name,
                          data_exchange_type = 'tomography_raw_projections'
                          )

if __name__ == "__main__":
    main()


