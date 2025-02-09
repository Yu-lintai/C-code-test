#include <stdio.h>
int getRemainder(int num1, int num2, int* res);
int main()
{
    int a = 10;
    int b = 5;
    int c = 0;
    
    int flag = getRemainder( a, b, &c);
    
    if (!flag)
    {
        printf("该函数的余数为：%d\n", c);
    }
    
}


int getRemainder(int num1, int num2, int* res)
{
    if (num2 == 0)
    {
        return 1;
    }
    
    *res = num1 % num2;
    return 0;
}