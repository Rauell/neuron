import numpy as np
import math
import scipy
import pyfits
import sys
import datetime
import scipy.optimize
import smtplib
import string
import numpy.core.records as rec
import matplotlib.pyplot as plt
import asciitable
import stripe82dcr as s82d
from krige import krige1d

def clean_file_qso(dataFile):
	print "\t Beginning to clean file: " + dataFile
	data = pyfits.open(dataFile)[1].data
	indices = np.array(range(len(data)))
	searchIDs = list(set(data.objid))
	
	print "Number of objids: %i. Number of indices: %i" % (len(searchIDs), len(indices))
	speczgood = ((data.ZBEST[:,0]>0)|(data.ZBEST[:,7]>0)|(data.ZBEST[:,2]>0)|(data.ZBEST[:,3]>0)|(data.ZBEST[:,4]>0)|(data.ZBEST[:,5]>0)|(data.ZBEST[:,6]>0)|(data.ZBEST[:,8]>0)|(data.ZBEST[:,11]>0)|(data.ZBEST[:,12]>0)|(data.ZBEST[:,13]>0))
	fluxgood = ((data.PSFFLUX_CLEAN[:,0]!=-9999.0)&(data.PSFFLUX_CLEAN[:,1]!=-9999.0)&(data.PSFFLUX_CLEAN[:,2]!=-9999.0)&(data.PSFFLUX_CLEAN[:,3]!=-9999.0)&(data.PSFFLUX_CLEAN[:,4]!=-9999.0))
	data2 = data[speczgood&fluxgood]
	
	indices = np.array(range(len(data2)))
	searchIDs = list(set(data2.objid))
	
	print "Number of objids with good zs: %i. Number of indices with good zs: %i" % (len(searchIDs), len(indices))
	
	bad_objids = []
	good_objids = []
	psfMagAll_cleaned = []
	psfMag_u = []
	psfMag_g = []
	psfMag_r = []
	psfMag_i = []
	psfMag_z = []
	
	count = 0.
	
	for sid in searchIDs:
		count += 1.
		bad_object = False
		
		x = data2[data2.objid == sid]
		
		if DEBUG == True:
			print x
	
		psfMagList = []

		for i in xrange(len(x)):
			if i == 0:
				try:
					coadd_u=x.coadd_u[i]
				except ValueError:
					coadd_u=np.nan
				try:
					coadd_g=x.coadd_g[i]
				except ValueError:
					coadd_g=np.nan
				try:
					coadd_r=x.coadd_r[i]
				except ValueError:
					coadd_r=np.nan
				try:
					coadd_i=x.coadd_i[i]
				except ValueError:
					coadd_i=np.nan
				try:
					coadd_z=x.coadd_z[i]
				except ValueError:
					coadd_z=np.nan
			psfMag_u.append(x.u[i])
			psfMag_g.append(x.g[i])
			psfMag_r.append(x.r[i])
			psfMag_i.append(x.i[i])
			psfMag_z.append(x.z[i])
			psfMag = np.array([x.u[i], x.g[i], x.r[i], x.i[i], x.z[i]]) 
			psfMagList.append(psfMag.tolist())
			
		psfMag = rec.fromrecords(psfMagList, names = ','.join(SDSS_FILTERS))
		if (min(psfMag.u) > coadd_u) or (max(psfMag.u) < coadd_u) or (coadd_u > 27.0):
			if (x.objid[i] in bad_objids) == False:
				bad_objids.append(x.objid[i])
			bad_object = True
		if (min(psfMag.g) > coadd_g) or (max(psfMag.g) < coadd_g) or (coadd_g > 25.0):
			if (x.objid[i] in bad_objids) == False:
				bad_objids.append(x.objid[i])
			bad_object = True
		if (min(psfMag.r) > coadd_r) or (max(psfMag.r) < coadd_r) or (coadd_r > 23.0):
			if (x.objid[i] in bad_objids) == False:
				bad_objids.append(x.objid[i])
			bad_object = True
		if (min(psfMag.i) > coadd_i) or (max(psfMag.i) < coadd_i) or (coadd_i > 22.0):
			if (x.objid[i] in bad_objids) == False:
				bad_objids.append(x.objid[i])
			bad_object = True
		if (min(psfMag.z) > coadd_z) or (max(psfMag.z) < coadd_z) or (coadd_z > 22.0):
			if (x.objid[i] in bad_objids) == False:
				bad_objids.append(x.objid[i])
			bad_object = True
		if bad_object == False:
			good_objids.append(str(x.objid[i]))
	print "Number of good objects: %d. Number of bad objects: %d" %(len(good_objids), len(bad_objids))
	print "\t Done cleaning file."
	return good_objids
