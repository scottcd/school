#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include "atmFunctions.h"


int main()
{
	loadAccounts();
	
	while(1)
	{
		system("clear");
		printf("Welcome to the ATM machine.\n");

		int validation = (int)login();

		if(validation == 0)
		{
			continue;
		}
		printf("Successful user login!\n");
		int menuChoice = 0;
		
		while(menuChoice != 4)
		{
			printf("Please select an option below. (1-4)");
			printf("\n1. View Balance");
			printf("\n2. Deposit" );
			printf("\n3. Withdrawal");
			printf("\n4. Log Out\n\n");

			char buffer[8];
			gets(buffer);
			menuChoice = (int)*buffer - 48;
			
			system("clear");
			char* atmResponse = processSelection(menuChoice);
			printf("\n%s\n\n", atmResponse);
		}
	}

	return 0;
}
