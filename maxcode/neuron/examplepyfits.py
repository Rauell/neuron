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

qso_dataFile = 'GTR-ADM-QSO-master-sweeps_yannymatch.fit'

for qso_dataFile in qso_dataFiles:
	print "Cleaning star file."
	good_objids_qso = clean_file_qso(dataFile)
	print "Finished cleaning files at:"
	print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print "Making table for stars."
	objids = np.array([])
	coadd_ra = np.array([])
	coadd_dec = np.array([])
	coadd_u = np.array([])
	coadd_g = np.array([])
	coadd_r = np.array([])
	coadd_i = np.array([])
	coadd_z = np.array([])
	zspec = np.array([])
	auPar = np.array([])
	agPar = np.array([])
	A = np.array([])
	gamma = np.array([])
	sigma = np.array([])
	tau = np.array([])
	psfMag_u, psfMagErr_u, mjd_u = [], [], []
	psfMag_g, psfMagErr_g, mjd_g = [], [], []
	psfMag_r, psfMagErr_r, mjd_r = [], [], []
	psfMag_i, psfMagErr_i, mjd_i = [], [], []
	psfMag_z, psfMagErr_z, mjd_z = [], [], []
	data = pyfits.open(qso_dataFile)[1].data
	searchIDs = list(set(data.objid))
	for k, sid in enumerate(qso_objids_point):
		print sid
		x = data[data.objid == long(sid)]
		psfMagList_u, psfMagErrList_u, mjdList_u = [], [], []
		psfMagList_g, psfMagErrList_g, mjdList_g = [], [], []
		psfMagList_r, psfMagErrList_r, mjdList_r = [], [], []
		psfMagList_i, psfMagErrList_i, mjdList_i = [], [], []
		psfMagList_z, psfMagErrList_z, mjdList_z = [], [], []
		for j in xrange(len(x)):
			if j == 0:
				objids = np.append(objids, str(x.objid[j]))
				coadd_ra = np.append(coadd_ra, x.coadd_ra[j])
				coadd_dec = np.append(coadd_dec, x.coadd_dec[j])
				coadd_u = np.append(coadd_u, x.coadd_u[j])
				coadd_g = np.append(coadd_g, x.coadd_g[j])
				coadd_r = np.append(coadd_r, x.coadd_r[j])
				coadd_i = np.append(coadd_i, x.coadd_i[j])
				coadd_z = np.append(coadd_z, x.coadd_z[j])
				zspec = np.append(zspec, x.zQSO[j])
				sigma = np.append(sigma, x.sigma[j])
				tau = np.append(tau, x.tau[j])
				auPar = np.append(auPar, x.aupar[j])
				agPar = np.append(agPar, x.agpar[j])
			psfMagList_u.append(x.u[j])
			psfMagList_g.append(x.g[j])
			psfMagList_r.append(x.r[j])
			psfMagList_i.append(x.i[j])
			psfMagList_z.append(x.z[j])
			psfMagErrList_u.append(x.psfMagErr_u[j])
			psfMagErrList_g.append(x.psfMagErr_g[j])
			psfMagErrList_r.append(x.psfMagErr_r[j])
			psfMagErrList_i.append(x.psfMagErr_i[j])
			psfMagErrList_z.append(x.psfMagErr_z[j])
			mjdList_u.append(x.mjd_u[j])
			mjdList_g.append(x.mjd_g[j])
			mjdList_r.append(x.mjd_r[j])
			mjdList_i.append(x.mjd_i[j])
			mjdList_z.append(x.mjd_z[j])
			if j == (len(x)-1):
				psfMag = rec.fromarrays([psfMagList_u, psfMagList_g, psfMagList_r, psfMagList_i, psfMagList_z],		names = ','.join(SDSS_FILTERS))
				psfMagErr = rec.fromarrays([psfMagErrList_u, psfMagErrList_g, psfMagErrList_r, psfMagErrList_i, psfMagErrList_z], names = ','.join(SDSS_FILTERS))
				mjd = rec.fromarrays([mjdList_u, mjdList_g, mjdList_r, mjdList_i, mjdList_z], names = ','.join(SDSS_FILTERS))
				A_fit, gamma_fit = calculate_variability_parameters(mjd, psfMag, psfMagErr)
				A = np.append(A, A_fit)
				gamma = np.append(gamma, gamma_fit)
		psfMag_u.append(psfMagList_u)
		psfMag_g.append(psfMagList_g)
		psfMag_r.append(psfMagList_r)
		psfMag_i.append(psfMagList_i)
		psfMag_z.append(psfMagList_z)
		psfMagErr_u.append(psfMagErrList_u)
		psfMagErr_g.append(psfMagErrList_g)
		psfMagErr_r.append(psfMagErrList_r)
		psfMagErr_i.append(psfMagErrList_i)
		psfMagErr_z.append(psfMagErrList_z)
		mjd_u.append(mjdList_u)
		mjd_g.append(mjdList_g)
		mjd_r.append(mjdList_r)
		mjd_i.append(mjdList_i)
		mjd_z.append(mjdList_z)
	print len(objids), len(coadd_ra), len(coadd_dec), len(coadd_u), len(coadd_g), len(coadd_r), len(coadd_i), len(coadd_z), len(zspec), len(auPar), len(agPar), len(A), len(gamma), len(sigma), len(tau), len(psfMag_u), len(psfMag_g), len(psfMag_r), len(psfMag_i), len(psfMag_z), len(psfMagErr_u), len(psfMagErr_g), len(psfMagErr_r), len(psfMagErr_i), len(psfMagErr_z), len(mjd_u), len(mjd_g), len(mjd_r), len(mjd_i), len(mjd_z)
	objid = pyfits.Column(name='objid', format='A19', array=objids)
	coadd_ra = pyfits.Column(name='coadd_ra', format='D', array=coadd_ra)
	coadd_dec = pyfits.Column(name='coadd_dec', format='D', array=coadd_dec)
	coadd_u = pyfits.Column(name='coadd_u', format='D', array=coadd_u)
	coadd_g = pyfits.Column(name='coadd_g', format='D', array=coadd_g)
	coadd_r = pyfits.Column(name='coadd_r', format='D', array=coadd_r)
	coadd_i = pyfits.Column(name='coadd_i', format='D', array=coadd_i)
	coadd_z = pyfits.Column(name='coadd_z', format='D', array=coadd_z)
	zspec = pyfits.Column(name='zspec', format='D', array=zspec)
	psfMag_u = pyfits.Column(name='psfMag_u', format='PD()', array=psfMag_u)
	psfMag_g = pyfits.Column(name='psfMag_g', format='PD()', array=psfMag_g)
	psfMag_r = pyfits.Column(name='psfMag_r', format='PD()', array=psfMag_r)
	psfMag_i = pyfits.Column(name='psfMag_i', format='PD()', array=psfMag_i)
	psfMag_z = pyfits.Column(name='psfMag_z', format='PD()', array=psfMag_z)
	psfMagErr_u = pyfits.Column(name='psfMagErr_u', format='PD()', array=psfMagErr_u)
	psfMagErr_g = pyfits.Column(name='psfMagErr_g', format='PD()', array=psfMagErr_g)
	psfMagErr_r = pyfits.Column(name='psfMagErr_r', format='PD()', array=psfMagErr_r)
	psfMagErr_i = pyfits.Column(name='psfMagErr_i', format='PD()', array=psfMagErr_i)
	psfMagErr_z = pyfits.Column(name='psfMagErr_z', format='PD()', array=psfMagErr_z)
	mjd_u = pyfits.Column(name='mjd_u', format='PD()', array=mjd_u)
	mjd_g = pyfits.Column(name='mjd_g', format='PD()', array=mjd_g)
	mjd_r = pyfits.Column(name='mjd_r', format='PD()', array=mjd_r)
	mjd_i = pyfits.Column(name='mjd_i', format='PD()', array=mjd_i)
	mjd_z = pyfits.Column(name='mjd_z', format='PD()', array=mjd_z)
	auPar = pyfits.Column(name='auPar', format='D', array=auPar)
	agPar = pyfits.Column(name='agPar', format='D', array=agPar)
	A = pyfits.Column(name='A', format='D', array=A)
	gamma = pyfits.Column(name='gamma', format='D', array=gamma)
	tau = pyfits.Column(name='tau', format='D', array=tau)
	sigma = pyfits.Column(name='sigma', format='D', array=sigma)
	table_hdu = pyfits.new_table([objid, coadd_ra, coadd_dec, coadd_u, coadd_g, coadd_r, coadd_i, coadd_z, zspec, auPar, agPar, A, gamma, tau, sigma, psfMag_u, psfMag_g, psfMag_r, psfMag_i, psfMag_z, psfMagErr_u, psfMagErr_g, psfMagErr_r, psfMagErr_i, psfMagErr_z, mjd_u, mjd_g, mjd_r, mjd_i, mjd_z])
	phdu = pyfits.PrimaryHDU()
	hdulist = pyfits.HDUList([phdu, table_hdu])
	hdulist.writeto(qso_dataFile + '_cleaned.fit')
	print "Finished making table for stars at:"
	print datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print "Ended: %s." % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
