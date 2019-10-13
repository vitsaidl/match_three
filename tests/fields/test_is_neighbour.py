import pytest
from match_three import Fields, PointContainer

class FakeGameWindow():
    def create_oval(*args, **kwargs):
        pass

@pytest.fixture
def create_helper_object():
    fake_game_window = FakeGameWindow()
    first_point = PointContainer(1, 1)
    second_point = PointContainer(100, 100)
    return fake_game_window, first_point, second_point

def test_fields_are_east_neighbours(create_helper_object):
    fake_game_window, first_point, second_point = \
    create_helper_object
    first_field = Fields(
        fake_game_window,
        0, 0,
        first_point,
        second_point)
    second_field = Fields(
        fake_game_window,
        1, 0,
        first_point,
        second_point)
    asserted_value = True
    real_value = first_field.is_neighbour(second_field)
    assert asserted_value == real_value

def test_fields_are_west_neighbours(create_helper_object):
    fake_game_window, first_point, second_point = \
    create_helper_object
    first_field = Fields(
        fake_game_window,
        5, 6,
        first_point,
        second_point)
    second_field = Fields(
        fake_game_window,
        4, 6,
        first_point,
        second_point)
    asserted_value = True
    real_value = first_field.is_neighbour(second_field)
    assert asserted_value == real_value

def test_fields_are_north_neighbours(create_helper_object):
    fake_game_window, first_point, second_point = \
    create_helper_object
    first_field = Fields(
        fake_game_window,
        5, 6,
        first_point,
        second_point)
    second_field = Fields(
        fake_game_window,
        5, 7,
        first_point,
        second_point)
    asserted_value = True
    real_value = first_field.is_neighbour(second_field)
    assert asserted_value == real_value

def test_fields_are_south_neighbours(create_helper_object):
    fake_game_window, first_point, second_point = \
    create_helper_object
    first_field = Fields(
        fake_game_window,
        5, 6,
        first_point,
        second_point)
    second_field = Fields(
        fake_game_window,
        5, 5,
        first_point,
        second_point)
    asserted_value = True
    real_value = first_field.is_neighbour(second_field)
    assert asserted_value == real_value

def test_fields_are_the_same_field(create_helper_object):
    fake_game_window, first_point, second_point = \
    create_helper_object
    first_field = Fields(
        fake_game_window,
        0, 0,
        first_point,
        second_point)
    second_field = Fields(
        fake_game_window,
        0, 0,
        first_point,
        second_point)
    asserted_value = False
    real_value = first_field.is_neighbour(second_field)
    assert asserted_value == real_value

def test_fields_are_not_neighbours(create_helper_object):
    fake_game_window, first_point, second_point = \
    create_helper_object
    first_field = Fields(
        fake_game_window,
        0, 0,
        first_point,
        second_point)
    second_field = Fields(
        fake_game_window,
        5, 0,
        first_point,
        second_point)
    asserted_value = False
    real_value = first_field.is_neighbour(second_field)
    assert asserted_value == real_value
    