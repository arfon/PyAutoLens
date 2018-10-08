from autolens.imaging import mask
from autolens.plotting import imaging_plotters

# In this example, we'll create a grid of Cartesian (x,y) coordinates, representing the
# arc second coordinate grid of an observed image.

# In AutoLens, a grid is a set of two-dimensional (x,y) coordinates (in arc-seconds) that are deflected
# and traced by a strong lensing system.

# This coordinate grid is aligned with the image we analyze, thus each coordinate maps to the centre of
# each image-pixel. Lets make a grid using a 100 x 100 pixel image, with a pixel scale (arcsecond-to-pixel
# conversion factor) of 0.05", giving us a a 5" x 5" grid.
image_grids = mask.ImagingGrids.from_shape_and_pixel_scale(shape=(100, 100), pixel_scale=0.05,
                                                                 sub_grid_size=2)

# If we print the grid, we see it consists of a set of arc-second coordinates
# (noting that the difference between each coordinate is the 'pixel_scales' of 0.05" defined above)
print('(x,y) image-pixel 1:')
print(image_grids.image[0])
print('(x,y) image-pixel 2:')
print(image_grids.image[1])
print('(x,y) image-pixel 3:')
print(image_grids.image[2])
print('(x,y) image-pixel 101:')
print(image_grids.image[100])
print('etc.')

# (PyAutoLens actually flattens the NumPy array to 1D to save memory, however it consists of all
# 10000 pixel coordinates on our 2D grid)
print(image_grids.image.shape)

# We can also plot the grid, albeit it's a fairly bland uniform grid of dots.
imaging_plotters.plot_grid(grid=image_grids.image)

# You might be wondering why the image_grids are using the attribute 'image' (e.g. image_grids.image).

# This is because it consists of multiple grids. The 'image' grid is the grid where each (x,y) coordinate is located at
# the centre of each image pixel.

# There is also a sub-grid, which splits each image-pixel into a (sub_grid_size x sub_grid_size) pixel. This is
# used for evaluating light and mass profiles at a higher resolution and thus more accurately.

# We specified a sub_grid_size of 2 above, therefore we expect 4 (2 x 2) times more sub-pixels than image-pixels (still
# flattened to 1D).
print(image_grids.image.shape)
print(image_grids.sub.shape)

# The sub-pixels coordinates can also be printed:
print('(x,y) sub-pixel 1 (of image pixel 1):')
print(image_grids.sub[0])
print('(x,y) sub-pixel 2 (of image pixel 1):')
print(image_grids.sub[1])
print('(x,y) sub-pixel 3 (of image pixel 1):')
print(image_grids.sub[2])
print('(x,y) sub-pixel 4 (of image pixel 1):')
print(image_grids.sub[3])
print('(x,y) sub-pixel 1 (of image pixel 2):')
print(image_grids.sub[3])
print('etc.')

# Congratulations, you've completed your first PyAutoLens tutorial! Before moving on to the next one, experiment with
# PyAutoLens by doing the following:
#
# 1) Change the pixel-scale of the grid - what happens to the Cartesian coordinates?
# 2) Change the resolution of the grid - what happens Cartesian coordinates?
# 3) Change the sub-grid size - what do you note about the pixel-scale of sub pixels?