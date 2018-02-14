import prior
import pytest
from profiles import geometry_profiles, light_profiles, mass_profiles

import os
data_path = "{}/".format(os.path.dirname(os.path.realpath(__file__)))

@pytest.fixture(name='uniform_simple')
def make_uniform_simple():
    return prior.UniformPrior(lower_limit=0., upper_limit=1.)


@pytest.fixture(name='uniform_half')
def make_uniform_half():
    return prior.UniformPrior(lower_limit=0.5, upper_limit=1.)


class TestUniformPrior(object):
    def test__simple_assumptions(self, uniform_simple):
        assert uniform_simple.value_for(0.) == 0.
        assert uniform_simple.value_for(1.) == 1.
        assert uniform_simple.value_for(0.5) == 0.5

    def test__non_zero_lower_limit(self, uniform_half):
        assert uniform_half.value_for(0.) == 0.5
        assert uniform_half.value_for(1.) == 1.
        assert uniform_half.value_for(0.5) == 0.75


class MockClass(object):
    def __init__(self, one, two):
        self.one = one
        self.two = two


class MockConfig(prior.Config):
    def __init__(self, d=None):
        super(MockConfig, self).__init__("")
        if d is not None:
            self.d = d
        else:
            self.d = {}

    def get_for_nearest_ancestor(self, cls, attribute_name):
        return self.get(None, cls.__name__, attribute_name)

    def get(self, _, class_name, var_name):
        try:
            return self.d[class_name][var_name]
        except KeyError:
            return ["u", 0, 1]


class MockProfile(object):
    def __init__(self, intensity, centre=(0, 0)):
        self.intensity = intensity
        self.centre = centre


class TestClassMappingCollection(object):
    def test__argument_extraction(self):
        collection = prior.ClassMap(MockConfig())
        collection.add_class("mock_class", MockClass)
        assert 1 == len(collection.prior_models)

        assert len(collection.priors_ordered_by_id) == 2

    def test_config_limits(self):
        collection = prior.ClassMap(MockConfig({"MockClass": {"one": ["u", 1., 2.]}}))

        collection.add_class("mock_class", MockClass)

        assert collection.mock_class.one.lower_limit == 1.
        assert collection.mock_class.one.upper_limit == 2.

    def test_config_prior_type(self):
        collection = prior.ClassMap(MockConfig({"MockClass": {"one": ["g", 1., 2.]}}))

        collection.add_class("mock_class", MockClass)

        assert isinstance(collection.mock_class.one, prior.GaussianPrior)

        assert collection.mock_class.one.mean == 1.
        assert collection.mock_class.one.sigma == 2.

    def test_attribution(self):
        collection = prior.ClassMap(MockConfig())

        collection.add_class("mock_class", MockClass)

        assert hasattr(collection, "mock_class")
        assert hasattr(collection.mock_class, "one")

    def test_tuple_arg(self):
        collection = prior.ClassMap(MockConfig())

        collection.add_class("mock_profile", MockProfile)

        assert 3 == len(collection.priors_ordered_by_id)


class TestReconstruction(object):
    def test_simple_reconstruction(self):
        collection = prior.ClassMap(MockConfig())

        collection.add_class("mock_class", MockClass)

        reconstruction = collection.reconstruction_for_vector([1., 1.])

        assert isinstance(reconstruction.mock_class, MockClass)
        assert reconstruction.mock_class.one == 1.
        assert reconstruction.mock_class.two == 1.

    def test_two_object_reconstruction(self):
        collection = prior.ClassMap(MockConfig())

        collection.add_class("mock_class_1", MockClass)
        collection.add_class("mock_class_2", MockClass)

        reconstruction = collection.reconstruction_for_vector([1., 0., 0., 1.])

        assert isinstance(reconstruction.mock_class_1, MockClass)
        assert isinstance(reconstruction.mock_class_2, MockClass)

        assert reconstruction.mock_class_1.one == 1.
        assert reconstruction.mock_class_1.two == 0.

        assert reconstruction.mock_class_2.one == 0.
        assert reconstruction.mock_class_2.two == 1.

    def test_swapped_prior_construction(self):
        collection = prior.ClassMap(MockConfig())

        collection.add_class("mock_class_1", MockClass)
        collection.add_class("mock_class_2", MockClass)

        collection.mock_class_2.one = collection.mock_class_1.one

        reconstruction = collection.reconstruction_for_vector([1., 0., 0.])

        assert isinstance(reconstruction.mock_class_1, MockClass)
        assert isinstance(reconstruction.mock_class_2, MockClass)

        assert reconstruction.mock_class_1.one == 1.
        assert reconstruction.mock_class_1.two == 0.

        assert reconstruction.mock_class_2.one == 1.
        assert reconstruction.mock_class_2.two == 0.

    def test_prior_replacement(self):
        collection = prior.ClassMap(MockConfig())

        collection.add_class("mock_class", MockClass)

        collection.mock_class.one = prior.UniformPrior(100, 200)

        reconstruction = collection.reconstruction_for_vector([0., 0.])

        assert reconstruction.mock_class.one == 100.

    def test_tuple_arg(self):
        collection = prior.ClassMap(MockConfig())

        collection.add_class("mock_profile", MockProfile)

        reconstruction = collection.reconstruction_for_vector([0., 1., 0.])

        assert reconstruction.mock_profile.intensity == 0.
        assert reconstruction.mock_profile.centre == (1., 0.)

    def test_modify_tuple(self):
        collection = prior.ClassMap(MockConfig())

        collection.add_class("mock_profile", MockProfile)

        collection.mock_profile.centre.centre_0 = prior.UniformPrior(1., 10.)

        reconstruction = collection.reconstruction_for_vector([1., 1., 1.])

        assert reconstruction.mock_profile.centre == (10., 1.)

    def test_match_tuple(self):
        collection = prior.ClassMap(MockConfig())

        collection.add_class("mock_profile", MockProfile)

        collection.mock_profile.centre.centre_1 = collection.mock_profile.centre.centre_0

        reconstruction = collection.reconstruction_for_vector([0., 1.])

        assert reconstruction.mock_profile.centre == (1., 1.)


class TestRealClasses(object):

    def test_combination(self):
        collection = prior.ClassMap(MockConfig(), source_light_profile=light_profiles.SersicLightProfile,
                                    lens_mass_profile=mass_profiles.CoredEllipticalIsothermalMassProfile,
                                    lens_light_profile=light_profiles.CoreSersicLightProfile)

        reconstruction = collection.reconstruction_for_vector([1 for _ in range(len(collection.priors_ordered_by_id))])

        assert isinstance(reconstruction.source_light_profile, light_profiles.SersicLightProfile)
        assert isinstance(reconstruction.lens_mass_profile, mass_profiles.CoredEllipticalIsothermalMassProfile)
        assert isinstance(reconstruction.lens_light_profile, light_profiles.CoreSersicLightProfile)


class TestConfig(object):
    def test_loading_config(self):
        config = prior.Config(config_folder_path=data_path+"config_test")

        assert ['u', 0, 1] == config.get("geometry_profiles", "Profile", "centre_0")
        assert ['u', 0, 0.5] == config.get("geometry_profiles", "Profile", "centre_1")

    def test_reconstruction(self):
        collection = prior.ClassMap(prior.Config(config_folder_path=data_path+"config_test"), geometry_profile=geometry_profiles.Profile)

        reconstruction = collection.reconstruction_for_vector([1., 1.])

        assert reconstruction.geometry_profile.centre == (1., 0.5)

    def test_inheritance(self):
        collection = prior.ClassMap(prior.Config(config_folder_path=data_path+"config_test"), geometry_profile=geometry_profiles.EllipticalProfile)

        reconstruction = collection.reconstruction_for_vector([1., 1., 1., 1.])

        assert reconstruction.geometry_profile.centre == (1., 0.5)

    def test_true_config(self):
        collection = prior.ClassMap(elliptical_profile_1=geometry_profiles.EllipticalProfile,
                                    elliptical_profile_2=geometry_profiles.EllipticalProfile,
                                    spherical_profile=geometry_profiles.SphericalProfile,
                                    elliptical_light_profile=light_profiles.EllipticalLightProfile,
                                    sersic_light_profile=light_profiles.SersicLightProfile,
                                    exponential_light_profile=light_profiles.ExponentialLightProfile)

        reconstruction = collection.reconstruction_for_vector([1 for _ in range(len(collection.priors_ordered_by_id))])

        assert isinstance(reconstruction.elliptical_profile_1, geometry_profiles.EllipticalProfile)
        assert isinstance(reconstruction.elliptical_profile_2, geometry_profiles.EllipticalProfile)
        assert isinstance(reconstruction.spherical_profile, geometry_profiles.SphericalProfile)

        assert isinstance(reconstruction.elliptical_light_profile, light_profiles.EllipticalLightProfile)
        assert isinstance(reconstruction.sersic_light_profile, light_profiles.SersicLightProfile)
        assert isinstance(reconstruction.exponential_light_profile, light_profiles.ExponentialLightProfile)


class TestUtility(object):
    def test_class_priors_dict(self):
        collection = prior.ClassMap(MockConfig(), mock_class=MockClass)

        assert list(collection.class_priors_dict.keys()) == ["mock_class"]
        assert len(collection.class_priors_dict["mock_class"]) == 2

        collection = prior.ClassMap(MockConfig(), mock_class_1=MockClass, mock_class_2=MockClass)

        collection.mock_class_1.one = collection.mock_class_2.one
        collection.mock_class_1.two = collection.mock_class_2.two

        assert collection.class_priors_dict["mock_class_1"] == collection.class_priors_dict["mock_class_2"]

    def test_value_vector_for_hypercube_vector(self):
        collection = prior.ClassMap(MockConfig(), mock_class=MockClass)

        collection.mock_class.two = prior.UniformPrior(upper_limit=100.)

        assert collection.value_vector_for_hypercube_vector([1., 0.5]) == [1., 50.]
