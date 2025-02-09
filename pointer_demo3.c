#include <stdio.h>
#include <stdlib.h>
#include <time.h>


typedef struct viewer
{
    char name [100];
    int count;
} vw;


int main()
{
    vw arr[4] = {{"A", 0}, {"B", 0}, {"C", 0}, {"D", 0}};

    srand(time(NULL));
    for ( int i = 0; i < 80; i++)
    {
        int choose = rand() % 4;
        arr[choose].count++;
    }
    
    
    for (int i = 0; i < 4; i++)
    
    {
        vw temp = arr[i];
        printf("需要去的景点是：%s,一共有%d几票赞成\n", temp.name, temp.count);

    }

    int max = arr[0].count;
     
} 




