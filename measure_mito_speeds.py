import numpy
import csv
import utility


def calculate_speed(centroids, time_interval, calibration):
	displacement_vectors = centroids[1:] - centroids[:-1]
	return numpy.sqrt(numpy.sum(displacement_vectors**2,axis = 1))/time_interval*calibration


def calculate_velocities(centroids, time_interval, calibration, normal = numpy.asarray([0,-1,0])):
	displacement_vectors = centroids[1:] - centroids[:-1]
	distances = numpy.sqrt(numpy.sum(displacement_vectors**2,axis = 1))
	dot_products = (normal * displacement_vectors).sum(axis=1)
	return numpy.sign(dot_products)*distances*calibration/time_interval

def calculate_normal(centroids):
	displacement_vector = centroids[1] - centroids[0]
	distance = numpy.sqrt(numpy.sum(displacement_vector**2))
	return [displacement_vector[0]/distance,displacement_vector[1]/distance,displacement_vector[2]/distance]

#parameters, paths
time_interval = 6.27 #seconds
xy_size = 0.109 #pixel size, microns
z_size = 1.5 #z step, microns
znum = 27 #number of z slices
norm_centroids = numpy.asarray([[3.3,22.8,0],[15.5,13.5,0]])
normal = calculate_normal(norm_centroids)

parent_dir = '/Users/erin/Desktop/team/Demi/data/'
track_file = parent_dir+'red_mitos.csv'
out_file = parent_dir+'red_speeds_raw.csv'


#load tracks
rows, header = utility.read_csv_file(track_file)
R = numpy.asarray(rows)
R = numpy.asarray(R,dtype = 'float')

#get T and Z from original slice numbers
slices = R[:,1]
T,Z = numpy.divmod(slices,znum)

#get centroids
centroids = numpy.zeros((len(slices),3))
centroids[:,0] = R[:,2]*xy_size #x coordinate
centroids[:,1] = R[:,3]*xy_size #y coordinate
centroids[:,2] = Z*z_size #z coordinate

#measure speeds and velocities
speeds = calculate_speed(centroids,time_interval,1)
speeds_2D = calculate_speed(centroids[:,:2],time_interval,1)
vs = calculate_velocities(centroids,time_interval,1,normal = normal)

#save results

header_out = ['track','original_slice','T_frame','X_pixel','Y_pixel','Z_slice','T_s','X_microns','Y_microns','Z_microns','speed','velocity','speed_2D']
OUT = numpy.zeros((len(slices),13))
OUT[:,0] = R[:,0]
OUT[:,1] = slices
OUT[:,2] = T
OUT[:,3] = R[:,2]
OUT[:,4] = R[:,3]
OUT[:,5] = Z
OUT[:,6] = T*time_interval
OUT[:,7:10] = centroids
OUT[1:,10] = speeds
OUT[1:,11] = vs
OUT[1:,12] = speeds_2D

utility.write_csv(OUT,header_out,out_file)



