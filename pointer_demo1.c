#include <stdio.h>

void getMAXandMIN();

int main()
{
    int arr[] = {0,2,5,4,3,5,3,12,63,-1,-9,24 };
    int len = (sizeof(arr) / sizeof(int));
    printf("该数组的长度为：%d\n",len);
    int Max, MIN = arr[0];
    getMAXandMIN(arr, len, &Max, &MIN);

    printf("该数组最大值为：%d\n该数组最小值为：%d\n ", Max, MIN); 
    return 0 ;
}

void getMAXandMIN(int arr[], int len, int* MAX, int* MIN)
{
    *MAX = arr[0];
    *MIN = arr[0];
    for ( int i = 1; i < len; i++)
    {
        if (arr[i] > *MAX)
        {
            *MAX = arr[i]; 
    
        }
        if (arr[i] < *MIN)
        {
            *MIN = arr[i]; 
    
        }
    }
}