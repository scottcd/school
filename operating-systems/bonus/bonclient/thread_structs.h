#include "product_record.h"
#define MAXFILES 30

typedef struct accessFile_struct {
    //Or whatever information that you need
    char* fileName;
    struct product_record records[MAXFILES];
} accessFile_struct;

typedef struct writeSocket_struct {
    //Or whatever information that you need
    char *serverName;
    char *serverPort;
} writeSocket_struct;
