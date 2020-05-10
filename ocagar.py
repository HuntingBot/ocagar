import golly as g

# Parameters
xmax = 7
ymax = 7
soup_count = 4096
min_period = 5
max_period = 100
density = 37
exclude = []

# Initialization
rule = g.getrule()
g.setalgo("HashLife")
g.setbase(8)
g.setstep(5)
g.select([-1024, -1024, 2048, 2048])
result_count = [0] * max_period
chaotic_count = 0
hipe_count = 0
g.autoupdate(True)
known = []

for symmetry in ['T', 'C', 'S', 'K']:
	if symmetry == 'S':
		g.setrule(rule + ":" + symmetry + str(xmax))
	else:
		g.setrule(rule + ":" + symmetry + str(xmax) + "," + str(ymax))
	for i in range(soup_count):
		g.randfill(density)
		g.step()
		hashlist = []
		# TODO: Filter reptitions with population sequences

		# Detect period
		for j in range(0, max_period):
			g.run(1)
			if g.hash(g.getselrect()) in hashlist:
				# Periodic
				if (j >= min_period) and not (min(hashlist) in known) and not j in exclude:
					result_count[j] += 1
					g.save("p_" + str(j) + "_" + str(result_count[j]) + ".rle", "rle")
					known.append(min(hashlist))
				break
			hashlist.append(g.hash(g.getselrect()))
		else:
			# Aperiodic
			if int(g.getpop()) / (xmax * ymax) > 0.4:
				# Density > 40%
				chaotic_count += 1
				g.save("z_CHAOTIC_" + str(chaotic_count) + ".rle", "rle")
			else:
				# Density < 40%
				hipe_count += 1
				g.save("z_HIGHPERIOD_" + str(hipe_count) + ".rle", "rle")
