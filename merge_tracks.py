import numpy as np, argparse, scipy.interpolate
parser = argparse.ArgumentParser()
parser.add_argument("ifiles",nargs="+")
parser.add_argument("ofile")
parser.add_argument("--dt", type=float, default=1)
args = parser.parse_args()

# Load all input files
idata = [np.loadtxt(ifile).T for ifile in args.ifiles]
# Find union time range
t1 = min([d[0, 0] for d in idata])
t2 = max([d[0,-1] for d in idata])

# Build output time steps
t = np.arange(t1,t2,args.dt)

# Interpolate each time series
odata = [[t]]
for d in idata:
	ip = scipy.interpolate.interp1d(d[0],d[1:],bounds_error=False,fill_value=(d[1:,0],d[1:,-1]))
	od = ip(t)
	odata.append(od)
odata = np.concatenate(odata,0)

np.savetxt(args.ofile, odata.T, fmt="%8.0f" + " %11.6f %11.6f %6.1f"*(len(idata)))
