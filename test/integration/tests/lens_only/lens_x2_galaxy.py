import os
from pathlib import Path

from autofit.core import non_linear as nl
from autolens.imaging import mask as msk
from autolens.model.galaxy import galaxy, galaxy_model as gm
from autolens.pipeline import phase as ph
from autolens.pipeline import pipeline as pl
from autolens.model.profiles import light_profiles as lp
from test.integration import tools

home = str(Path.home())
dirpath = os.path.dirname(os.path.realpath(__file__))
dirpath = os.path.dirname(dirpath)
output_path = '{}/../output/lens_only'.format(dirpath)


def pipeline():
    pipeline_name = "lens_x2_galaxy"
    data_name = '/lens_x2_galaxy'

    tools.reset_paths(data_name, pipeline_name, output_path)

    sersic_0 = lp.EllipticalSersic(centre=(-1.0, -1.0), axis_ratio=0.8, phi=0.0, intensity=1.0,
                                   effective_radius=1.3, sersic_index=3.0)

    sersic_1 = lp.EllipticalSersic(centre=(1.0, 1.0), axis_ratio=0.8, phi=0.0, intensity=1.0,
                                   effective_radius=1.3, sersic_index=3.0)

    lens_galaxy_0 = galaxy.Galaxy(light_profile=sersic_0)
    lens_galaxy_1 = galaxy.Galaxy(light_profile=sersic_1)

    tools.simulate_integration_image(data_name=data_name, pixel_scale=0.2, lens_galaxies=[lens_galaxy_0, lens_galaxy_1],
                                     source_galaxies=[], target_signal_to_noise=50.0)

    pipeline = make_pipeline(pipeline_name=pipeline_name)
    image = tools.load_image(data_name=data_name, pixel_scale=0.2)

    results = pipeline.run(image=image)
    for result in results:
        print(result)


def make_pipeline(pipeline_name):
    class LensPlanex2GalPhase(ph.LensPlanePhase):

        def pass_priors(self, previous_results):
            self.lens_galaxies[0].sersic.centre_0 = -1.0
            self.lens_galaxies[0].sersic.centre_1 = -1.0
            self.lens_galaxies[1].sersic.centre_0 = 1.0
            self.lens_galaxies[1].sersic.centre_1 = 1.0

    def modify_mask_function(img):
        return msk.Mask.circular(shape=img.shape, pixel_scale=img.pixel_scale, radius_mask_arcsec=5.)

    phase1 = LensPlanex2GalPhase(lens_galaxies=[gm.GalaxyModel(sersic=lp.EllipticalSersic),
                                                gm.GalaxyModel(sersic=lp.EllipticalSersic)],
                                 mask_function=modify_mask_function, optimizer_class=nl.MultiNest,
                                 phase_name="{}/phase1".format(pipeline_name))

    phase1.optimizer.n_live_points = 40
    phase1.optimizer.sampling_efficiency = 0.8

    return pl.PipelineImaging(pipeline_name, phase1)


if __name__ == "__main__":
    pipeline()
