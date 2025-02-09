#include <stdio.h>
int main()
{   
    printf("请输入你需要的数组长度");
    int n = scanf("%d", &n);
    int *arr = (int*)malloc(n * sizeof(int));

    for (int i = 0; i < n; i++)
    {
        printf("请输入数组内第%d个元素", i+1);
        scanf("%d", &arr[i])
        printf("数组里面的元素为：%d\n", arr[i]);

        int sum = sum + arr[i];
    }
    



    return 0;
}