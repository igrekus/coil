from euclid3 import LineSegment2, Point2
from pyexpect import expect

from cncode.move_commands import get_intersects


# 1st quarter
def test_center_point_vertical_begin_acute_angle_right_first_q():
    begin = LineSegment2(Point2(0, 0), Point2(0, 5))
    end = LineSegment2(Point2(0, 5), Point2(7, 0))
    diameter = 2

    int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)
    expect(int4.x).to_equal(2)
    expect(int4.y).almost_equal(1.11, 0.01)


def test_center_point_vertical_begin_right_angle_right_first_q():
    begin = LineSegment2(Point2(0, 0), Point2(0, 5))
    end = LineSegment2(Point2(0, 5), Point2(5, 5))
    diameter = 2

    int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)
    expect(int4.x).to_equal(2)
    expect(int4.y).to_equal(3)


def test_center_point_vertical_begin_obtuse_angle_right_first_q():
    begin = LineSegment2(Point2(0, 0), Point2(0, 5))
    end = LineSegment2(Point2(0, 5), Point2(2, 7))
    diameter = 2

    int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)
    expect(int4.x).to_equal(2)
    expect(int4.y).almost_equal(4.17, 0.01)


def test_center_point_arbitrary_begin_acute_angle_right_first_q():
    begin = LineSegment2(Point2(0, 0), Point2(1, 5))
    end = LineSegment2(Point2(1, 5), Point2(4, 2))
    diameter = 2

    int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)
    expect(int4.x).almost_equal(2.22, 0.01)
    expect(int4.y).almost_equal(0.94, 0.01)


def test_center_point_arbitrary_begin_right_angle_right_first_q():
    begin = LineSegment2(Point2(0, 0), Point2(1, 5))
    end = LineSegment2(Point2(1, 5), Point2(5, 5))
    diameter = 2

    int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)
    expect(int4.x).almost_equal(2.63, 0.01)
    expect(int4.y).almost_equal(3, 0.01)


def test_center_point_arbitrary_begin_obtuse_angle_right_first_q():
    begin = LineSegment2(Point2(0, 0), Point2(1, 5))
    end = LineSegment2(Point2(1, 5), Point2(5, 7))
    diameter = 2

    int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)
    expect(int4.x).almost_equal(2.76, 0.01)
    expect(int4.y).almost_equal(3.64, 0.01)


# 2nd quarter
# int2
def test_center_point_horizontal_begin_acute_angle_right_second_q():
    begin = LineSegment2(Point2(0, 0), Point2(-5, 0))
    end = LineSegment2(Point2(-5, 0), Point2(-1, 5))
    diameter = 2

    int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)

    expect(int2.x).almost_equal(-0.83, 0.01)
    expect(int2.y).almost_equal(2.0, 0.01)


# int2
def test_center_point_horizontal_begin_right_angle_right_second_q():
    begin = LineSegment2(Point2(0, 0), Point2(-5, 0))
    end = LineSegment2(Point2(-5, 0), Point2(-5, 5))
    diameter = 2

    int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)

    expect(int2.x).to_equal(-3)
    expect(int2.y).to_equal(2)


#2 int1
def test_center_point_horizontal_begin_obtuse_angle_right_second_q():
    begin = LineSegment2(Point2(0, 0), Point2(-5, 0))
    end = LineSegment2(Point2(-5, 0), Point2(-7, 5))
    diameter = 2

    int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)

    print('\n')
    print(int1)
    print(int2)
    print(int3)
    print(int4)

    expect(int1.x).almost_equal(-3.64, 0.01)
    expect(int1.y).almost_equal(2.0, 0.01)

# https://www.youtube.com/watch?v=yoDDvOId_vY

# def test_center_point_arbitrary_begin_acute_angle_right_first_q():
#     begin = LineSegment2(Point2(0, 0), Point2(1, 5))
#     end = LineSegment2(Point2(1, 5), Point2(4, 2))
#     diameter = 2
#
#     int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)
#     expect(int4.x).almost_equal(2.22, 0.01)
#     expect(int4.y).almost_equal(0.94, 0.01)
#
#
# def test_center_point_arbitrary_begin_right_angle_right_first_q():
#     begin = LineSegment2(Point2(0, 0), Point2(1, 5))
#     end = LineSegment2(Point2(1, 5), Point2(5, 5))
#     diameter = 2
#
#     int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)
#     expect(int4.x).almost_equal(2.63, 0.01)
#     expect(int4.y).almost_equal(3, 0.01)
#
#
# def test_center_point_arbitrary_begin_obtuse_angle_right_first_q():
#     begin = LineSegment2(Point2(0, 0), Point2(1, 5))
#     end = LineSegment2(Point2(1, 5), Point2(5, 7))
#     diameter = 2
#
#     int1, int2, int3, int4 = get_intersects(begin, end, diameter=diameter)
#     expect(int4.x).almost_equal(2.76, 0.01)
#     expect(int4.y).almost_equal(3.64, 0.01)
#
#
#
