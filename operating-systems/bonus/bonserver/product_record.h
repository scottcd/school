#ifndef PROCUCT_RECORD
#define PROCUCT_RECORD


#define PRODUCTSIZE 128
#define MAXSTAGES 5


// Created by: Barrett
// Date: 1/19/2016
//
// product_record
//   models one product at various stages in the system 

struct product_record {
	int idnumber;			    // Unique identification
	char name[PRODUCTSIZE];	 // String description
	double price;			    // Unit cost
	int number;			       // Number ordered
	double tax;			       // Tax on order
	double sANDh;			    // Shipping and handling
	double total;			    // Total order cost
	int stations[MAXSTAGES]; // Stations processed
};

#endif
