import simul_run
import output
import time
st = time.time()

# inputs: extract or load


# running
# simul_run.run(save=True)

# outputs
# output.write_results()
# output.plot_results()
output.change_trajectories()

print("ran in %.2f seconds" % (time.time()-st))
