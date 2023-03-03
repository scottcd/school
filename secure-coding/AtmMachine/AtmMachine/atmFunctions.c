#include "account.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

const int numberOfAccounts = 2;
int loggedIn = -1; // int representing the currently logged in account, -1 if none 

account accountList[2] = {};

void loadAccounts()
{
	account a1 = {"Bobby Bee","user1","pass1",100};
	account a2 = {"Joe Mahma","user2","pass2",100};
	
	accountList[0] = a1;
	accountList[1] = a2;
}

int login() {
	char username [25];
	char password [25];

	printf("Enter your username: ");
	gets(username);
	printf("Enter your password: ");
	gets(password);

	for (int i = 0; i < numberOfAccounts; i++) {
		if (strcmp(accountList[i].username, username) == 0) {
			if (strcmp(accountList[i].password, password) == 0) {
				loggedIn = i;
				return 1;
			}
			else { 
				return 0;
			}
		}
	}
	return 0;
}

void deposit (int val) {
	accountList[loggedIn].balance += val;
	return;
}

// returns -1 if error (out of bounds), 0 otherwise
int withdraw (int val) {
	if (accountList[loggedIn].balance >= val) {
		accountList[loggedIn].balance -= val;
		return 0;
	}
	return -1;
}

int viewBalance()
{
	int currentBal = (int)accountList[loggedIn].balance;
	return currentBal;
}

char* processSelection(int menuChoice)
{
	static char ret[100];
	int bal;
	int input;
	switch(menuChoice)
	{
		case 1:
			bal = viewBalance();
			sprintf(ret, "Balance: $%d", bal);
			break;
		case 2:
			printf("How much would you like to deposit: ");
			scanf("%d", &input);
			fflush(stdin); // clear buffer to avoid bad mermes
			deposit(abs(input));
			stpcpy(ret, "Deposit complete.\n");
			break;
		case 3:
			printf("How much would you like to withdraw: ");
			scanf("%d", &input);
			fflush(stdin); // clear buffer to avoid bad mermes
			if (withdraw(abs(input)) == -1) {
				stpcpy(ret, "Cannot withdraw more than balance.\n");
				break;
			}
			stpcpy(ret, "Withdraw complete.\n");
			break;
		case 4:
			stpcpy(ret, "Goodbye");
			loggedIn = -1;
	}
	return ret;
}
