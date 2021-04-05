class Matrix:
    def __init__(self, values):
        self.values = values
        self.col = len(values[0])
        self.row = len(values)

    def __repr__(self):
        return f'<Matrix.values values="{self.values}">'

    def __matmul__(self, other):
        """
        A = [[1, 2],  [3, 4]]
        B = [[11, 12], [13, 14]]

        [[1 * 11 + 2 * 13,   1 * 12 + 2 * 14],
        [3 * 11 + 4 * 13,   3 * 12 + 4 * 14]]


        A @ B =

        A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]
        A[1][0] * B[0][0] + A[1][1] + B[1][1], A[1][0] * B[0][1] + A[1][1] * B[1][1]


        """
        if self.col != other.row:
            raise ValueError(
                "Numbers rows first matrix != number columns second matrix"
            )

        result = [[0 for row in range(other.col)] for col in range(self.row)]

        for i in range(self.row):
            for j in range(other.col):
                for k in range(self.col):
                    res = self.values[i][k] * other.values[k][j]
                    result[i][j] += res

        return Matrix(result)

    __rmatmul__ = __matmul__

    def __imatmul__(self, other):
        self.values = self.__matmul__(other).values
        return self
