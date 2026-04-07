class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def __add__(self, other):
        result = []

        for i in range(len(self.matrix)):
            row = []
            for j in range(len(self.matrix[0])):
                row.append(self.matrix[i][j] + other.matrix[i][j])
            result.append(row)

        return result


m1 = [[1,2,3],[4,5,6],[7,8,9]]
m2 = [[9,8,7],[6,5,4],[3,2,1]]

mat1 = Matrix(m1)
mat2 = Matrix(m2)

result = mat1.__add__(mat2)

print(result)