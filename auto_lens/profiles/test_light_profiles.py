from __future__ import division, print_function

import pytest
from auto_lens.profiles import light_profiles
from auto_lens.profiles import geometry_profiles
import math
import numpy as np

@pytest.fixture(name='circular')
def circular_sersic():
    return light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6,
                                           sersic_index=4.0)


@pytest.fixture(name='elliptical')
def elliptical_sersic():
    return light_profiles.EllipticalSersic(axis_ratio=0.5, phi=0.0, intensity=1.0, effective_radius=0.6,
                                           sersic_index=4.0)


@pytest.fixture(name='vertical')
def vertical_sersic():
    return light_profiles.EllipticalSersic(axis_ratio=0.5, phi=90.0, intensity=1.0, effective_radius=0.6,
                                           sersic_index=4.0)

class TestConstructors(object):

    def test__setup_sersic(self):
        
        sersic = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6,
                                                 sersic_index=4.0)
        
        assert sersic.x_cen == 0.0
        assert sersic.y_cen == 0.0
        assert sersic.axis_ratio == 1.0
        assert sersic.phi == 0.0
        assert sersic.intensity == 1.0
        assert sersic.effective_radius == 0.6
        assert sersic.sersic_index == 4.0
        assert sersic.sersic_constant == pytest.approx(7.66925, 1e-3)
        assert sersic.elliptical_effective_radius == 0.6

    def test__setup_exponential(self):
        
        exponential = light_profiles.EllipticalExponential(axis_ratio=0.5, phi=0.0, intensity=1.0, effective_radius=0.6)
        
        assert exponential.x_cen == 0.0
        assert exponential.y_cen == 0.0
        assert exponential.axis_ratio == 0.5
        assert exponential.phi == 0.0
        assert exponential.intensity == 1.0
        assert exponential.effective_radius == 0.6
        assert exponential.sersic_index == 1.0
        assert exponential.sersic_constant == pytest.approx(1.678378, 1e-3)
        assert exponential.elliptical_effective_radius == 0.6 / math.sqrt(0.5)

    def test__setup_dev_vaucouleurs(self):
        
        dev_vaucouleurs = light_profiles.EllipticalDevVaucouleurs(axis_ratio=0.6, phi=10.0, intensity=2.0, effective_radius=0.9,
                                                                  centre=(0.0, 0.1))
        
        assert dev_vaucouleurs.x_cen == 0.0
        assert dev_vaucouleurs.y_cen == 0.1
        assert dev_vaucouleurs.axis_ratio == 0.6
        assert dev_vaucouleurs.phi == 10.0
        assert dev_vaucouleurs.intensity == 2.0
        assert dev_vaucouleurs.effective_radius == 0.9
        assert dev_vaucouleurs.sersic_index == 4.0
        assert dev_vaucouleurs.sersic_constant == pytest.approx(7.66925, 1e-3)
        assert dev_vaucouleurs.elliptical_effective_radius == 0.9 / math.sqrt(0.6)

    def test__setup_core_sersic(self):
        
        cored_sersic = light_profiles.EllipticalCoreSersic(axis_ratio=0.5, phi=0.0, intensity=1.0,
                                                           effective_radius=5.0, sersic_index=4.0, radius_break=0.01,
                                                           intensity_break=0.1, gamma=1.0, alpha=1.0)

        assert cored_sersic.x_cen == 0.0
        assert cored_sersic.y_cen == 0.0
        assert cored_sersic.axis_ratio == 0.5
        assert cored_sersic.phi == 0.0
        assert cored_sersic.intensity == 1.0
        assert cored_sersic.effective_radius == 5.0
        assert cored_sersic.sersic_index == 4.0
        assert cored_sersic.sersic_constant == pytest.approx(7.66925, 1e-3)
        assert cored_sersic.radius_break == 0.01
        assert cored_sersic.intensity_break == 0.1
        assert cored_sersic.gamma == 1.0
        assert cored_sersic.alpha == 1.0
        assert cored_sersic.elliptical_effective_radius == 5.0 / math.sqrt(0.5)

    def test_component_numbers_four_profiles(self):

        # TODO : Perform Counting reset better

        from itertools import count

        light_profiles.EllipticalLightProfile._ids = count()

        sersic_0 = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6,
                                                 sersic_index=4.0)

        sersic_1 = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6,
                                                 sersic_index=4.0)

        sersic_2 = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6,
                                                 sersic_index=4.0)

        sersic_3 = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6,
                                                 sersic_index=4.0)

        assert sersic_0.component_number == 0
        assert sersic_1.component_number == 1
        assert sersic_2.component_number == 2
        assert sersic_3.component_number == 3



class TestProfiles(object):
    class TestSersic:

        def test__intensity_at_radius__correct_value(self):
            sersic = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=1.0, effective_radius=0.6,
                                                     sersic_index=4.0)

            intensity = sersic.intensity_at_radius(radius=1.0)
            assert intensity == pytest.approx(0.351797, 1e-3)

        def test__intensity_at_radius_2__correct_value(self):
            sersic = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=2.0)
            intensity = sersic.intensity_at_radius(
                radius=1.5)  # 3.0 * exp(-3.67206544592 * (1,5/2.0) ** (1.0 / 2.0)) - 1) = 0.351797
            assert intensity == pytest.approx(4.90657319276, 1e-3)

        def test__intensity_at_coordinates__different_axis_ratio(self):
            sersic = light_profiles.EllipticalSersic(axis_ratio=0.5, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=2.0)

            intensity = sersic.intensity_at_coordinates(coordinates=np.array([0.0, 1.0]))

            assert intensity == pytest.approx(5.38066670129, 1e-3)

        def test__intensity_at_coordinates__different_rotate_phi_90_same_result(self):
            sersic = light_profiles.EllipticalSersic(axis_ratio=0.5, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=2.0)

            intensity_1 = sersic.intensity_at_coordinates(coordinates=np.array([0.0, 1.0]))

            sersic = light_profiles.EllipticalSersic(axis_ratio=0.5, phi=90.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=2.0)

            intensity_2 = sersic.intensity_at_coordinates(coordinates=np.array([1.0, 0.0]))

            assert intensity_1 == intensity_2

    class TestExponential:

        def test__intensity_at_radius__correct_value(self):
            exponential = light_profiles.EllipticalExponential(axis_ratio=1.0, phi=0.0, intensity=1.0,
                                                               effective_radius=0.6)

            intensity = exponential.intensity_at_radius(radius=1.0)
            assert intensity == pytest.approx(0.3266, 1e-3)

        def test__intensity_at_radius_2__correct_value(self):
            exponential = light_profiles.EllipticalExponential(axis_ratio=1.0, phi=0.0, intensity=3.0,
                                                               effective_radius=2.0)
            intensity = exponential.intensity_at_radius(radius=1.5)
            assert intensity == pytest.approx(4.5640, 1e-3)

        def test__intensity_at_coordinates_1(self):
            exponential = light_profiles.EllipticalExponential(axis_ratio=0.5, phi=0.0, intensity=3.0,
                                                               effective_radius=2.0)

            intensity = exponential.intensity_at_coordinates(coordinates=np.array([0.0, 1.0]))

            assert intensity == pytest.approx(4.9047, 1e-3)

        def test__intensity_at_coordinates_2(self):
            exponential = light_profiles.EllipticalExponential(axis_ratio=0.5, phi=90.0, intensity=2.0,
                                                               effective_radius=3.0)

            intensity = exponential.intensity_at_coordinates(coordinates=np.array([1.0, 0.0]))

            assert intensity == pytest.approx(4.8566, 1e-3)

        def test__double_intensity_doubles_intensity_value(self):
            exponential = light_profiles.EllipticalExponential(axis_ratio=0.5, phi=90.0, intensity=4.0,
                                                               effective_radius=3.0)

            intensity = exponential.intensity_at_coordinates(coordinates=np.array([1.0, 0.0]))

            assert intensity == pytest.approx(2.0 * 4.8566, 1e-3)

        def test__intensity_at_coordinates__different_rotate_phi_90_same_result(self):
            exponential = light_profiles.EllipticalExponential(axis_ratio=0.5, phi=0.0, intensity=3.0,
                                                               effective_radius=2.0)

            intensity_1 = exponential.intensity_at_coordinates(coordinates=np.array([0.0, 1.0]))

            exponential = light_profiles.EllipticalExponential(axis_ratio=0.5, phi=90.0, intensity=3.0,
                                                               effective_radius=2.0)

            intensity_2 = exponential.intensity_at_coordinates(coordinates=np.array([1.0, 0.0]))

            assert intensity_1 == intensity_2

    class TestDevVaucouleurs:

        def test__intensity_at_radius__correct_value(self):
            dev_vaucouleurs = light_profiles.EllipticalDevVaucouleurs(axis_ratio=1.0, phi=0.0, intensity=1.0,
                                                                      effective_radius=0.6)

            intensity = dev_vaucouleurs.intensity_at_radius(radius=1.0)
            assert intensity == pytest.approx(0.3518, 1e-3)

        def test__intensity_at_radius_2__correct_value(self):
            dev_vaucouleurs = light_profiles.EllipticalDevVaucouleurs(axis_ratio=1.0, phi=0.0, intensity=3.0,
                                                                      effective_radius=2.0)
            intensity = dev_vaucouleurs.intensity_at_radius(radius=1.5)
            assert intensity == pytest.approx(5.1081, 1e-3)

        def test__intensity_at_coordinates_1(self):
            dev_vaucouleurs = light_profiles.EllipticalDevVaucouleurs(axis_ratio=0.5, phi=0.0, intensity=3.0,
                                                                      effective_radius=2.0)

            intensity = dev_vaucouleurs.intensity_at_coordinates(coordinates=np.array([0.0, 1.0]))

            assert intensity == pytest.approx(5.6697, 1e-3)

        def test__intensity_at_coordinates_2(self):
            dev_vaucouleurs = light_profiles.EllipticalDevVaucouleurs(axis_ratio=0.5, phi=90.0, intensity=2.0,
                                                                      effective_radius=3.0)

            intensity = dev_vaucouleurs.intensity_at_coordinates(coordinates=np.array([1.0, 0.0]))

            assert intensity == pytest.approx(7.4455, 1e-3)

        def test__double_intensity_doubles_intensity_value(self):
            dev_vaucouleurs = light_profiles.EllipticalDevVaucouleurs(axis_ratio=0.5, phi=90.0, intensity=4.0,
                                                                      effective_radius=3.0)

            intensity = dev_vaucouleurs.intensity_at_coordinates(coordinates=np.array([1.0, 0.0]))

            assert intensity == pytest.approx(2.0 * 7.4455, 1e-3)

        def test__intensity_at_coordinates__different_rotate_phi_90_same_result(self):
            dev_vaucouleurs = light_profiles.EllipticalDevVaucouleurs(axis_ratio=0.5, phi=0.0, intensity=3.0,
                                                                      effective_radius=2.0)

            intensity_1 = dev_vaucouleurs.intensity_at_coordinates(coordinates=np.array([0.0, 1.0]))

            dev_vaucouleurs = light_profiles.EllipticalDevVaucouleurs(axis_ratio=0.5, phi=90.0, intensity=3.0,
                                                                      effective_radius=2.0)

            intensity_2 = dev_vaucouleurs.intensity_at_coordinates(coordinates=np.array([1.0, 0.0]))

            assert intensity_1 == intensity_2

    class TestCoreSersic(object):

        def test__intensity_at_radius__correct_value(self):
            core_sersic = light_profiles.EllipticalCoreSersic(axis_ratio=0.5, phi=0.0, intensity=1.0,
                                                              effective_radius=5.0, sersic_index=4.0,
                                                              radius_break=0.01,
                                                              intensity_break=0.1, gamma=1.0, alpha=1.0)

            assert core_sersic.intensity_at_radius(0.01) == 0.1


class TestLuminosityIntegral(object):

    class TestWithinCircle(object):

        def test__spherical_exponential__compare_to_analytic(self):

            import math
            import scipy.special

            sersic = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=1.0)

            integral_radius = 5.5

            # Use gamma functioon for analytic computation of the intensity within a radius=0.5

            x = sersic.sersic_constant * (integral_radius / sersic.effective_radius) ** (1.0 / sersic.sersic_index)

            intensity_analytic = sersic.intensity * sersic.effective_radius ** 2 * 2 * math.pi * sersic.sersic_index * \
                                 (math.e ** sersic.sersic_constant / (
                                 sersic.sersic_constant ** (2 * sersic.sersic_index))) * \
                                 scipy.special.gamma(2 * sersic.sersic_index) * scipy.special.gammainc(
                2 * sersic.sersic_index, x)

            intensity_integral = sersic.luminosity_within_circle(radius=integral_radius)

            assert intensity_analytic == pytest.approx(intensity_integral, 1e-3)

        def test__spherical_sersic_index_2__compare_to_analytic(self):

            import math
            import scipy.special

            sersic = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=2.0)

            integral_radius = 0.5

            # Use gamma functioon for analytic computation of the intensity within a radius=0.5

            x = sersic.sersic_constant * ((integral_radius / sersic.effective_radius) ** (1.0 / sersic.sersic_index))

            intensity_analytic = sersic.intensity * sersic.effective_radius ** 2 * 2 * math.pi * sersic.sersic_index * \
                                 ((math.e ** sersic.sersic_constant) / (
                                 sersic.sersic_constant ** (2 * sersic.sersic_index))) * \
                                 scipy.special.gamma(2 * sersic.sersic_index) * scipy.special.gammainc(
                2 * sersic.sersic_index, x)

            intensity_integral = sersic.luminosity_within_circle(radius=0.5)

            assert intensity_analytic == pytest.approx(intensity_integral, 1e-3)

        def test__spherical_dev_vaucouleurs__compare_to_analytic(self):

            import math
            import scipy.special

            sersic = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=4.0)

            integral_radius = 0.5

            # Use gamma functioon for analytic computation of the intensity within a radius=0.5

            x = sersic.sersic_constant * ((integral_radius / sersic.effective_radius) ** (1.0 / sersic.sersic_index))

            intensity_analytic = sersic.intensity * sersic.effective_radius ** 2 * 2 * math.pi * sersic.sersic_index * \
                                 ((math.e ** sersic.sersic_constant) / (
                                 sersic.sersic_constant ** (2 * sersic.sersic_index))) * \
                                 scipy.special.gamma(2 * sersic.sersic_index) * scipy.special.gammainc(
                2 * sersic.sersic_index, x)

            intensity_integral = sersic.luminosity_within_circle(radius=0.5)

            assert intensity_analytic == pytest.approx(intensity_integral, 1e-3)

        def test__spherical_exponential__compare_to_grid(self):

            sersic = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=1.0)

            import numpy as np

            integral_radius = 1.0
            luminosity_tot = 0.0

            xs = np.linspace(-1.5, 1.5, 40)
            ys = np.linspace(-1.5, 1.5, 40)

            edge = xs[1] - xs[0]
            area = edge ** 2

            for x in xs:
                for y in ys:

                    eta = math.sqrt(x ** 2 + y ** 2)

                    if eta < integral_radius:
                        luminosity_tot += sersic.intensity_at_radius(eta) * area

            intensity_integral = sersic.luminosity_within_circle(radius=integral_radius)

            assert luminosity_tot == pytest.approx(intensity_integral, 0.02)

        def test__spherical_sersic_2__compare_to_grid(self):

            sersic = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=2.0)

            import numpy as np

            integral_radius = 1.0
            luminosity_tot = 0.0

            xs = np.linspace(-1.5, 1.5, 40)
            ys = np.linspace(-1.5, 1.5, 40)

            edge = xs[1] - xs[0]
            area = edge ** 2

            for x in xs:
                for y in ys:

                    eta = math.sqrt(x ** 2 + y ** 2)
                    if eta < integral_radius:
                        luminosity_tot += sersic.intensity_at_radius(eta) * area

            intensity_integral = sersic.luminosity_within_circle(radius=integral_radius)

            assert luminosity_tot == pytest.approx(intensity_integral, 0.02)

        def test__spherical_dev_vaucauleurs__compare_to_grid(self):

            sersic = light_profiles.EllipticalSersic(axis_ratio=1.0, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=4.0)

            import numpy as np

            integral_radius = 1.0
            luminosity_tot = 0.0

            xs = np.linspace(-1.5, 1.5, 40)
            ys = np.linspace(-1.5, 1.5, 40)

            edge = xs[1] - xs[0]
            area = edge ** 2

            for x in xs:
                for y in ys:

                    eta = math.sqrt(x ** 2 + y ** 2)
                    if eta < integral_radius:
                        luminosity_tot += sersic.intensity_at_radius(eta) * area

            intensity_integral = sersic.luminosity_within_circle(radius=integral_radius)

            assert luminosity_tot == pytest.approx(intensity_integral, 0.02)

        def test__elliptical_exponential__compare_to_grid(self):

            sersic = light_profiles.EllipticalSersic(axis_ratio=0.5, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=1.0)

            integral_radius = 0.5
            luminosity_tot = 0.0

            xs = np.linspace(-1.0, 1.0, 40)
            ys = np.linspace(-1.0, 1.0, 40)

            edge = xs[1] - xs[0]
            area = edge ** 2

            for x in xs:
                for y in ys:

                    eta = math.sqrt(x ** 2 + y ** 2)
                    if eta < integral_radius:
                        luminosity_tot += sersic.intensity_at_radius(eta) * area

            intensity_integral = sersic.luminosity_within_circle(radius=integral_radius)

            assert luminosity_tot == pytest.approx(intensity_integral, 0.02)

        def test__elliptical_sersic_2__compare_to_grid(self):

            sersic = light_profiles.EllipticalSersic(axis_ratio=0.3, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=2.0)

            integral_radius = 0.5
            luminosity_tot = 0.0

            xs = np.linspace(-1.8, 1.8, 50)
            ys = np.linspace(-1.8, 1.8, 50)

            edge = xs[1] - xs[0]
            area = edge ** 2

            for x in xs:
                for y in ys:

                    eta = math.sqrt(x ** 2 + y ** 2)
                    if eta < integral_radius:
                        luminosity_tot += sersic.intensity_at_radius(eta) * area

            intensity_integral = sersic.luminosity_within_circle(radius=integral_radius)

            assert luminosity_tot == pytest.approx(intensity_integral, 0.02)

    class TestWithinEllipse(object):

        def test__elliptical_exponential__compare_to_grid(self):

            sersic = light_profiles.EllipticalSersic(axis_ratio=0.5, phi=0.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=1.0)

            integral_radius = 0.5
            luminosity_tot = 0.0

            xs = np.linspace(-1.0, 1.0, 40)
            ys = np.linspace(-1.0, 1.0, 40)

            edge = xs[1] - xs[0]
            area = edge ** 2

            for x in xs:
                for y in ys:

                    eta = sersic.coordinates_to_elliptical_radius((x, y))

                    if eta < integral_radius:
                        luminosity_tot += sersic.intensity_at_radius(eta) * area

            intensity_integral = sersic.luminosity_within_ellipse(major_axis=integral_radius)

            assert luminosity_tot == pytest.approx(intensity_integral, 0.02)

        def test__elliptical_sersic_2__compare_to_grid(self):

            sersic = light_profiles.EllipticalSersic(axis_ratio=0.5, phi=90.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=2.0)

            integral_radius = 0.5
            luminosity_tot = 0.0

            xs = np.linspace(-1.8, 1.8, 80)
            ys = np.linspace(-1.8, 1.8, 80)

            edge = xs[1] - xs[0]
            area = edge ** 2

            for x in xs:
                for y in ys:

                    eta = sersic.coordinates_to_elliptical_radius((x, y))

                    if eta < integral_radius:
                        luminosity_tot += sersic.intensity_at_radius(eta) * area

            intensity_integral = sersic.luminosity_within_ellipse(major_axis=integral_radius)

            assert luminosity_tot == pytest.approx(intensity_integral, 0.02)

        def test__elliptical_dev_vaucauleurs__compare_to_grid(self):

            sersic = light_profiles.EllipticalSersic(axis_ratio=0.7, phi=30.0, intensity=3.0, effective_radius=2.0,
                                                     sersic_index=4.0)

            integral_radius = 0.5
            luminosity_tot = 0.0

            xs = np.linspace(-1.5, 1.5, 50)
            ys = np.linspace(-1.5, 1.5, 50)

            edge = xs[1] - xs[0]
            area = edge ** 2

            for x in xs:
                for y in ys:

                    eta = sersic.coordinates_to_elliptical_radius((x, y))

                    if eta < integral_radius:
                        luminosity_tot += sersic.intensity_at_radius(eta) * area

            intensity_integral = sersic.luminosity_within_ellipse(major_axis=integral_radius)

            assert luminosity_tot == pytest.approx(intensity_integral, 0.01)


class TestCoordinates(object):
    def test__coordinates_to_eccentric_radius(self, elliptical):
        assert elliptical.coordinates_to_eccentric_radius((1, 1)) == pytest.approx(
            elliptical.coordinates_to_eccentric_radius(
                (-1, -1)), 1e-10)

    def test__intensity_at_coordinates(self, elliptical):
        assert elliptical.intensity_at_coordinates((1, 1)) == pytest.approx(
            elliptical.intensity_at_coordinates((-1, -1)), 1e-10)


class TestArray(object):
    def test__simple_assumptions(self, circular):
        array = geometry_profiles.array_function(circular.intensity_at_coordinates)(x_min=0, x_max=101, y_min=0, y_max=101,
                                                                                    pixel_scale=1)
        assert array.shape == (101, 101)
        assert array[51][51] > array[51][52]
        assert array[51][51] > array[52][51]
        assert all(map(lambda i: i > 0, array[0]))

        array = geometry_profiles.array_function(circular.intensity_at_coordinates)(x_min=0, x_max=100, y_min=0, y_max=100,
                                                                                    pixel_scale=0.5)
        assert array.shape == (200, 200)

    def test__ellipticity(self, circular, elliptical, vertical):
        array = geometry_profiles.array_function(circular.intensity_at_coordinates)(x_min=0, x_max=101, y_min=0, y_max=101,
                                                                                    pixel_scale=1)
        assert array[60][0] == array[0][60]

        array = geometry_profiles.array_function(elliptical.intensity_at_coordinates)(x_min=0, x_max=100, y_min=0, y_max=100,
                                                                                      pixel_scale=1)

        assert array[60][51] > array[51][60]

        array = geometry_profiles.array_function(vertical.intensity_at_coordinates)(x_min=0, x_max=100, y_min=0, y_max=100,
                                                                                    pixel_scale=1)
        assert array[60][51] < array[51][60]

    # noinspection PyTypeChecker
    def test__flat_array(self, circular):
        array = geometry_profiles.array_function(circular.intensity_at_coordinates)(x_min=0, x_max=100, y_min=0, y_max=100,
                                                                                    pixel_scale=1)
        flat_array = geometry_profiles.array_function(circular.intensity_at_coordinates)(x_min=0, x_max=100, y_min=0, y_max=100,
                                                                                         pixel_scale=1).flatten()

        assert all(array[0] == flat_array[:100])
        assert all(array[1] == flat_array[100:200])

    def test_symmetric_profile(self, circular):
        circular.centre = (50, 50)
        array = geometry_profiles.array_function(circular.intensity_at_coordinates)(x_min=0, x_max=100, y_min=0, y_max=100,
                                                                                    pixel_scale=1.0)

        assert array[50][50] > array[50][51]
        assert array[50][50] > array[49][50]
        assert array[49][50] == array[50][51]
        assert array[50][51] == array[50][49]
        assert array[50][49] == array[51][50]

        array = geometry_profiles.array_function(circular.intensity_at_coordinates)(x_min=0, x_max=100, y_min=0, y_max=100,
                                                                                    pixel_scale=0.5)

        assert array[100][100] > array[100][101]
        assert array[100][100] > array[99][100]
        assert array[99][100] == array[100][101]
        assert array[100][101] == array[100][99]
        assert array[100][99] == array[101][100]

    def test_origin_symmetric_profile(self, circular):
        array = geometry_profiles.array_function(circular.intensity_at_coordinates)()

        assert circular.intensity_at_coordinates((-5, 0)) < circular.intensity_at_coordinates((0, 0))
        assert circular.intensity_at_coordinates((5, 0)) < circular.intensity_at_coordinates((0, 0))
        assert circular.intensity_at_coordinates((0, -5)) < circular.intensity_at_coordinates((0, 0))
        assert circular.intensity_at_coordinates((0, 5)) < circular.intensity_at_coordinates((0, 0))
        assert circular.intensity_at_coordinates((5, 5)) < circular.intensity_at_coordinates((0, 0))
        assert circular.intensity_at_coordinates((-5, -5)) < circular.intensity_at_coordinates((0, 0))

        assert array.shape == (100, 100)

        assert array[50][50] > array[50][51]
        assert array[50][50] > array[49][50]
        assert array[49][50] == pytest.approx(array[50][51], 1e-10)
        assert array[50][51] == pytest.approx(array[50][49], 1e-10)
        assert array[50][49] == pytest.approx(array[51][50], 1e-10)


class TestTransform(object):
    def test_exceptions(self, elliptical):
        with pytest.raises(geometry_profiles.CoordinatesException):
            elliptical.transform_to_reference_frame(geometry_profiles.TransformedCoordinates((0, 0)))

        with pytest.raises(geometry_profiles.CoordinatesException):
            elliptical.transform_from_reference_frame((0, 0))
