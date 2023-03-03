#ifndef ATMFUNCTIONS_H_INCLUDED
#define ATMFUNCTIONS_H_INCLUDED
#include "account.h"


char* loadAccounts();

int login();

int viewBalance();

char* processSelection(int menuChoice);

int withdraw (int val);

void deposit(int val);
#endif
