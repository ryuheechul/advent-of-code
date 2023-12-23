"""
read the doc below for `calc_row`
and here are many module level doc tests for it

# sb, se: source.start, source.stop
# tb, te: target.start, target.stop

# sb  se
#         tb  te
>>> calc_row(3, range(10, 20), range(30, 40))
([], [range(30, 40)])

# sb  se
#     tb  te
>>> calc_row(3, range(10, 20), range(20, 30))
([], [range(20, 30)])

#         sb  se
# tb  te
>>> calc_row(3, range(30, 40), range(10, 20))
([], [range(10, 20)])

#     sb  se
# tb  te
>>> calc_row(3, range(20, 30), range(10, 20))
([], [range(10, 20)])

# sb |      | se
#    tb    te
>>> calc_row(3, range(10, 40), range(20, 30))
([range(23, 33)], [])

#    sb    se
# tb |      | te
>>> calc_row(3, range(20, 30), range(10, 40))
([range(23, 33)], [range(10, 20), range(30, 40)])

# sb    se
# tb    te
>>> calc_row(3, range(20, 30), range(20, 30))
([range(23, 33)], [])

# sb  |     se
#     tb     |  te
>>> calc_row(3, range(10, 30), range(20, 40))
([range(23, 33)], [range(30, 40)])

#     sb     |  se
# tb  |     te
>>> calc_row(3, range(20, 40), range(10, 30))
([range(23, 33)], [range(10, 20)])

# sb  |     se
#     tb    te
>>> calc_row(3, range(10, 30), range(20, 30))
([range(23, 33)], [])

# sb     |  se
# tb     te
>>> calc_row(3, range(20, 40), range(20, 30))
([range(23, 33)], [])

# real world cases
>>> calc_row(-32, range(77, 100), range(74, 88))
([range(45, 56)], [range(74, 77)])

>>> calc_row(4, range(64, 77), range(74, 77))
([range(78, 81)], [])

>>> calc_row(1, range(0, 69), range(45, 56))
([range(46, 57)], [])

>>> calc_row(2, range(50, 98), range(55, 68))
([range(57, 70)], [])

>>> calc_row(-4, range(53, 61), range(57, 70))
([range(53, 57)], [range(61, 70)])

>>> calc_row(36, range(45, 64), range(46, 50))
([range(82, 86)], [])

>>> calc_row(36, range(45, 64), range(54, 63))
([range(90, 99)], [])
"""


def calc_row(diff: int, source: range, target: range):
    """
    returns (mapped, unmapped)
    """

    sb, se = source.start, source.stop
    tb, te = target.start, target.stop

    # case 1: no overlap
    # sb  se          o           sb  se
    #        tb  te   r   tb  te
    if se <= tb or te <= sb:
        return [], [target]
    # case 2: target is enveloped within source
    # sb |      | se
    #    tb    te
    elif sb < tb and te < se:
        mapped = range(tb + diff, te + diff)
        return [mapped], []
    # case 3: source is enveloped within target
    #    sb    se
    # tb |      | te
    elif tb <= sb and se <= te:
        mapped = range(sb + diff, se + diff)
        unmapped = []

        unmapped_left = range(tb, sb)
        unmapped_right = range(se, te)

        if tb != sb:
            unmapped.append(unmapped_left)

        if se != te:
            unmapped.append(unmapped_right)

        return [mapped], unmapped
    # case 4:
    # - target.start is equal or bigger than source.start
    # - and target.stop is equal or bigger than source.stop
    # sb  |     se
    #     tb     |  te
    elif sb <= tb and se <= te:
        mapped = range(tb + diff, se + diff)
        unmapped = [] if se == te else [range(se, te)]

        return [mapped], unmapped
    # case 5:
    # - source.start is equal or bigger than target.start
    # - and source.stop is equal or bigger than target.stop
    #     sb     |  se
    # tb  |     te
    elif tb <= sb and te <= se:
        mapped = range(sb + diff, te + diff)
        unmapped = [] if tb == sb else [range(tb, sb)]
        return [mapped], unmapped

    # it shouldn't reach here but in case it does it should be the same as the first case
    return [], [target]


if __name__ == "__main__":
    import doctest

    if doctest.testmod().failed:
        raise Exception("doc test failed")
