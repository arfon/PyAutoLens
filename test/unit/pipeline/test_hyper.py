import numpy as np
import pytest
from astropy import cosmology as cosmo

from autofit.mapper import model
from autofit.mapper import model_mapper as mm
from autolens.data.array import grids
from autolens.data.array import mask as msk
from autolens.model import galaxy as g
from autolens.model.profiles import light_profiles as lp
from autolens.model.profiles import mass_profiles as mp
from autolens.pipeline import phase as ph
from test.unit.mock.mock_imaging import MockBorders


class MockData:
    def __init__(self, grid_stack, padded_grid_stack, border):
        self.grid_stack = grid_stack
        self.padded_grid_stack = padded_grid_stack
        self.border = border


@pytest.fixture(name="lens_data")
def make_lens_data():
    mask = msk.Mask(np.array([[True, True, True, True],
                              [True, False, False, True],
                              [True, True, True, True]]), pixel_scale=6.0)

    grid_stack = grids.GridStack.grid_stack_from_mask_sub_grid_size_and_psf_shape(mask=mask, sub_grid_size=2,
                                                                                  psf_shape=(3, 3))
    mask = msk.Mask(np.array([[True, False]]), pixel_scale=3.0)
    padded_grid_stack = grids.GridStack.padded_grid_stack_from_mask_sub_grid_size_and_psf_shape(mask, 2, (3, 3))
    border = MockBorders()

    return MockData(grid_stack, padded_grid_stack, border)


@pytest.fixture(name="lens_galaxy")
def make_lens_galaxy():
    return g.Galaxy(mass=mp.EllipticalCoredPowerLaw(), redshift=1.0)


@pytest.fixture(name="source_galaxy")
def make_source_galaxy():
    return g.Galaxy(light=lp.EllipticalLightProfile(), redshift=2.0)


@pytest.fixture(name="lens_galaxies")
def make_lens_galaxies(lens_galaxy):
    lens_galaxies = model.ModelInstance()
    lens_galaxies.lens = lens_galaxy
    return lens_galaxies


@pytest.fixture(name="lens_result")
def make_lens_result(lens_galaxies, lens_data):
    instance = model.ModelInstance()
    instance.lens_galaxies = lens_galaxies

    return ph.LensPlanePhase.Result(instance, 1.0, mm.ModelMapper(), None,
                                    ph.LensPlanePhase.Analysis(lens_data=lens_data, cosmology=cosmo.Planck15,
                                                               positions_threshold=1.0), None)


@pytest.fixture(name="lens_source_result")
def make_lens_source_result(source_galaxy, lens_galaxy, lens_data):
    source_galaxies = model.ModelInstance()
    lens_galaxies = model.ModelInstance()
    source_galaxies.source = source_galaxy
    lens_galaxies.lens = lens_galaxy

    instance = model.ModelInstance()
    instance.source_galaxies = source_galaxies
    instance.lens_galaxies = lens_galaxies

    return ph.LensSourcePlanePhase.Result(instance, 1.0, mm.ModelMapper(), None,
                                          ph.LensSourcePlanePhase.Analysis(lens_data=lens_data,
                                                                           cosmology=cosmo.Planck15,
                                                                           positions_threshold=1.0), None)


@pytest.fixture(name="multi_plane_result")
def make_multi_plane_result(lens_galaxy, source_galaxy, lens_data):
    instance = model.ModelInstance()
    galaxies = model.ModelInstance()
    galaxies.lens = lens_galaxy
    galaxies.source = source_galaxy
    instance.galaxies = galaxies

    return ph.MultiPlanePhase.Result(instance, 1.0, mm.ModelMapper(), None,
                                     ph.MultiPlanePhase.Analysis(lens_data=lens_data,
                                                                 cosmology=cosmo.Planck15,
                                                                 positions_threshold=1.0), None)


class TestImagePassing(object):
    def test_lens_galaxy_dict(self, lens_result, lens_galaxy):
        assert lens_result.name_galaxy_tuples == [("lens", lens_galaxy)]

    def test_lens_source_galaxy_dict(self, lens_source_result, lens_galaxy, source_galaxy):
        assert lens_source_result.name_galaxy_tuples == [("lens", lens_galaxy), ("source", source_galaxy)]

    def test_multi_plane_galaxy_dict(self, multi_plane_result, lens_galaxy, source_galaxy):
        assert multi_plane_result.name_galaxy_tuples == [("lens", lens_galaxy), ("source", source_galaxy)]

    def test_lens_image_dict(self, lens_result):
        image_dict = lens_result.image_dict
        assert isinstance(image_dict["lens"], np.ndarray)

    def test_lens_source_image_dict(self, lens_source_result):
        image_dict = lens_source_result.image_dict
        assert isinstance(image_dict["lens"], np.ndarray)
        assert isinstance(image_dict["source"], np.ndarray)

    def test_multi_plane_image_dict(self, multi_plane_result):
        image_dict = multi_plane_result.image_dict
        assert isinstance(image_dict["lens"], np.ndarray)
        assert isinstance(image_dict["source"], np.ndarray)
