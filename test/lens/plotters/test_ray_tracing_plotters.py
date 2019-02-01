from autolens.data.array import grids
from autolens.lens import ray_tracing
from autolens.lens.plotters import ray_tracing_plotters
from autolens.model.galaxy import galaxy as g
from autolens.model.profiles import light_profiles as lp, mass_profiles as mp
from test.fixtures import *


@pytest.fixture(name='ray_tracing_plotter_path')
def make_ray_tracing_plotter_setup():
    return "{}/../../test_files/plotting/ray_tracing/".format(os.path.dirname(os.path.realpath(__file__)))


@pytest.fixture(name='galaxy_light')
def make_galaxy_light():
    return g.Galaxy(light=lp.EllipticalSersic(intensity=1.0))


@pytest.fixture(name='galaxy_mass')
def make_galaxy_mass():
    return g.Galaxy(mass=mp.SphericalIsothermal(einstein_radius=1.0))


@pytest.fixture(name='grid_stack')
def make_grid_stack():
    return grids.GridStack.from_shape_pixel_scale_and_sub_grid_size(shape=(100, 100), pixel_scale=0.05, sub_grid_size=2)


@pytest.fixture(name='tracer')
def make_tracer(galaxy_light, galaxy_mass, grid_stack):
    return ray_tracing.TracerImageSourcePlanes(lens_galaxies=[galaxy_mass, galaxy_light],
                                               source_galaxies=[galaxy_light],
                                               image_plane_grid_stack=grid_stack)


def test__tracer_sub_plot_output_dependent_on_config(tracer, ray_tracing_plotter_path, plot_patch):
    ray_tracing_plotters.plot_ray_tracing_subplot(tracer=tracer, output_path=ray_tracing_plotter_path,
                                                  output_format='png')

    assert ray_tracing_plotter_path + 'tracer.png' in plot_patch.paths


def test__tracer_individuals__dependent_on_config(tracer, ray_tracing_plotter_path, plot_patch):
    ray_tracing_plotters.plot_ray_tracing_individual(tracer=tracer, output_path=ray_tracing_plotter_path,
                                                     output_format='png')

    assert ray_tracing_plotter_path + 'tracer_image_plane_image.png' in plot_patch.paths

    assert ray_tracing_plotter_path + 'tracer_source_plane.png' in plot_patch.paths

    assert ray_tracing_plotter_path + 'tracer_surface_density.png' not in plot_patch.paths

    assert ray_tracing_plotter_path + 'tracer_potential.png' in plot_patch.paths

    assert ray_tracing_plotter_path + 'tracer_deflections_y.png' not in plot_patch.paths
    assert ray_tracing_plotter_path + 'tracer_deflections_x.png' not in plot_patch.paths


def test__image_plane_image_is_output(tracer, ray_tracing_plotter_path, plot_patch):
    ray_tracing_plotters.plot_image_plane_image(tracer=tracer, output_path=ray_tracing_plotter_path,
                                                output_format='png')
    assert ray_tracing_plotter_path + 'tracer_image_plane_image.png' in plot_patch.paths


def test__surface_density_is_output(tracer, ray_tracing_plotter_path, plot_patch):
    ray_tracing_plotters.plot_surface_density(tracer=tracer, output_path=ray_tracing_plotter_path, output_format='png')
    assert ray_tracing_plotter_path + 'tracer_surface_density.png' in plot_patch.paths


def test__potential_is_output(tracer, ray_tracing_plotter_path, plot_patch):
    ray_tracing_plotters.plot_potential(tracer=tracer, output_path=ray_tracing_plotter_path, output_format='png')
    assert ray_tracing_plotter_path + 'tracer_potential.png' in plot_patch.paths


def test__deflections_y_is_output(tracer, ray_tracing_plotter_path, plot_patch):
    ray_tracing_plotters.plot_deflections_y(tracer=tracer, output_path=ray_tracing_plotter_path, output_format='png')
    assert ray_tracing_plotter_path + 'tracer_deflections_y.png' in plot_patch.paths


def test__deflections_x_is_output(tracer, ray_tracing_plotter_path, plot_patch):
    ray_tracing_plotters.plot_deflections_x(tracer=tracer, output_path=ray_tracing_plotter_path, output_format='png')
    assert ray_tracing_plotter_path + 'tracer_deflections_x.png' in plot_patch.paths
