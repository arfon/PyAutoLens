
class HyperImage(object):

    def __init__(self, background_sky_scale=0.0, background_noise_scale=0.0):
        """Class for scaling the noise of different components in an image_coords, primarily the different galaxies (e.g. the \
        lens, source).

        Parameters
        -----------
        background_sky_scale : float
            The value by which the background scale is scaled (electrons per second).
        background_noise_scale : float
            The value by which the background noise is increased (electrons per second).
        """
        self.background_sky_scale = background_sky_scale
        self.background_noise_scale = background_noise_scale

    def compute_sky_scaled_image(self, image):
        """Compute a new image_coords with the background sky level scaled. This can simply multiple by a constant factor \
        (assuming a uniform background sky) because the image_coords is in units electrons per second.

        Parameters
        -----------
        image : ndarray
            The image_coords before scaling (electrons per second).
        """
        return image + self.background_sky_scale

    def compute_scaled_noise(self, noise, background_noise):
        """Compute a scaled noise map from the baseline noise map. This scales each galaxy component individually \
        using their galaxy contribution map and sums their scaled noise maps with the baseline and background noise maps.

        Parameters
        -----------
        noise : ndarray
            The noise before scaling (electrons per second)..
        background_noise : ndarray
            The background noise values (electrons per second)..
        """
        return noise + (self.background_noise_scale * background_noise)
