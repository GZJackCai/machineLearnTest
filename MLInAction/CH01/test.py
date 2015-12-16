#author Jack
from numpy import *

if __name__ == '__main__':
    #print(random.rand(4,4))
    #矩阵
    randMat=mat(random.rand(4,4))
    #print(randMat)
    #实现了矩阵求逆的运算
    invRandMat=randMat.I
    #print(invRandMat)
    #矩阵和逆矩阵相乘(单位矩阵)
    myEye=randMat*invRandMat
    #print(myEye)
    #处理计算机的结果误差
    print(myEye-eye(4))
