import glob
import numpy as np
import astropy.units as u
from astropy.time import Time
import astropy.io.fits as fits
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord

def plot_change_in_velocity(science_files, output_graph):

    observations = []

    # using for loop to read required data in each reduced science image
    for file in science_files:
        with fits.open(file) as hdul:
            header = hdul[0].header
            ra = header.get('RA')  # extract RA
            dec = header.get('DEC')  # extract DEC
            date_obs = header.get('DATE-OBS')  # extract observation date
            observations.append((ra, dec, date_obs))  # make into a list

    # using for loop to obtain coords in degree using ra and dec
    coords = [SkyCoord(ra=obs[0], dec=obs[1], unit=(u.deg, u.deg), frame='icrs') for obs in observations]

    # taking time from the third value in the tuples
    times = [Time(obs[2]) for obs in observations]

    # note: plot will show time in intervals of 15 seconds, 
    # but observation was done every hour for 10 minutes!

    # finding change in velocity over the observation time
    velocities = []
    for i in range(len(coords) - 1):
        # angular separation in degrees
        ang_sep = coords[i].separation(coords[i+1])
        
        # time difference in seconds
        dt = (times[i+1] - times[i]).to(u.s).value
        
        # converting angular separation to velocity 
        velocity = ang_sep.arcsec / dt  # arcsec per second
        velocities.append(velocity)

    # timestamps for observations
    time_vals = times
    
    # converting imestamps to datetime
    times = [Time(t).datetime for t in time_vals]

    # adjusting timestamps for plotting (so it looks better)
    mid_time_vals = [(times[i] + (times[i+1] - times[i]) / 2) for i in range(len(times) - 1)]
    
    # ploting change in velocity
    plt.figure(figsize=(8, 6))
    plt.plot(mid_time_vals, velocities, marker='o', linestyle='-', color='red')
    plt.xlabel("Time (UTC)")
    plt.ylabel("Velocity Difference (arcsec/sec)")
    plt.title("Change In Angular Velocity Over Time")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.savefig(output_graph)
    plt.show()

    # glob was used to sort and read the reduced science images
    # output_graph argument is in place to give the graphs as a png

    return