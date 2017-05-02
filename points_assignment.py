from xml.etree import ElementTree

_pointsAssignment = {}  # set()
_factorMax = 0


class PointAssignment:
    def __init__(self, factor, win, loss):
        self.factor = int(factor)
        self.win = int(win)
        self.loss = int(loss)

    def __str__(self):
        return 'Factor {0}: win: {1} pts; loss: {2} pts'.\
            format(self.factor, self.win, self.loss)

    def __repr__(self):
        return '<PointAssignment (factor={0}, win={1}, loss={2})>'.\
            format(self.factor, self.win, self.loss)

    def __eq__(self, other):
        return self.factor == other.factor

    def __hash__(self):
        return hash('{}'.format(self.factor))


# noinspection PyPep8Naming
def getPointsAssignment():
    global _factorMax
    if not _pointsAssignment:
        tree = ElementTree.parse('points_mapping.xml')
        for segment in tree.getroot().findall('segment'):
            factor = int(segment.find('factor').text)
            _factorMax = max(factor, _factorMax)
            _pointsAssignment[factor] = PointAssignment(
                factor,
                segment.find('win').text,
                segment.find('loss').text
            )
    return _pointsAssignment


# noinspection PyPep8Naming
def getPoint(factor):
    if factor in _pointsAssignment:
        return getPointsAssignment()[factor]
    else:
        point = getPointsAssignment()[_factorMax]
        return PointAssignment(factor, point.win, point.loss)
    # return getPointsAssignment().get(factor,
    #                                  getPointsAssignment()[_factorMax])


if __name__ == '__main__':
    points = getPointsAssignment()
    for factor, point in points.items():
        print(factor, ':', str(point))
    for point in getPointsAssignment().values():
        print(point.win, '<-->', point.loss)
    for factor in range(10):
        print(getPoint(factor))
