/*
 * This file justs shows the C representation of what we are doing.
 * We are not going to be taking input from the user as it is initialized
 * in the memory, nor are we going to print the contents of the array.
 * We are going to just run the code between begin and end.
 * This code performs insertion sort on the array.
 * 
 * @author Aryan Bansal and Abhirath Adamane
 * @data 25/1/24
 * @version 1.0
 */

#include<stdio.h>

int main()
{
    int ARR_LENGTH = 0; 
    scanf("%d", &ARR_LENGTH);

    int * arr = malloc(ARR_LENGTH * sizeof(int));
    
    //This is just for initializing the array.
    //In the IAS, the memory would be preloaded with the data.
    
    for(int i = 0; i - ARR_LENGTH < 0; i++)
        scanf("%d", arr + i);

    
    //Begin
    
    for(int i = 1; i - ARR_LENGTH < 0;)
    {
        int j = i;

        int currentValue = arr[i];
        
        while(-j < 0 && -arr[j - 1] + currentValue < 0)
        {
            arr[j] = arr[j - 1];
            j--;
        }

        arr[j] = currentValue;
        i++;
    }
    
    //End

    //This is just for printing the result. It won't be there in the IAS.
    //In the IAS, the array would be sorted in the memory.
    
    for(int i = 0; i < ARR_LENGTH; i++)
        printf("%d ", arr[i]);
    printf("\n");

    return 0;
}