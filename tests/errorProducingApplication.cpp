#include <iostream>
#include <memory>

/*
Errors to detect.

Read/write pre/post bounds of stack array.
Read/write pre/post bounds of dynamically allocated array.
Use after free.
Memory leak.
Used unititialized.
Double free.
Return pointer to stack variable.
*/


bool isValid(double* array) {
  return array != 0;
}

double getElement(double* array, size_t index) {
  if (isValid(array))
    return array[index];
  else
    return 0.0;
}

void setElement(double* array, size_t index, double value) {
  if (isValid(array))
    array[index] = value;
}



double* stackArray;
double* newArray;
double* mallocArray;


void createNewArray() {
  if (!isValid(newArray))
    newArray = new double[10];
}

void createMallocArray() {
  if (!isValid(mallocArray))
    mallocArray = (double*)malloc(10*sizeof(double));
}


void setArray(double* array) {
  double value;
  for (size_t i = 0 ; i <= 11 ; ++i)
    array[0] = value;
}


double* getDouble() {
  double a = 12.0;
  return &a;
}


void axpy(double* lhs, double* rhs) {
  double scalar = *getDouble();
  double* scalarPtr = new double;
  *scalarPtr = scalar;
  delete [] scalarPtr;
  for (size_t i = 0 ; i < 11 ; ++i)
    if (i%2 == 0)
      lhs[i] += lhs[i] + *scalarPtr * rhs[i];
    else
      lhs[i] += lhs[i] + *getDouble() * rhs[i];
}

void printArray(double* array) {
  for (size_t i = 0 ; i < 10 ; ++i)
    std::cout << array[i] << std::endl;
}


int main() {
  double arrayOnStack[10];
  stackArray = arrayOnStack;
  createNewArray();
  createMallocArray();

  setArray(stackArray);
  setArray(newArray - 1);
  setArray(mallocArray - 1);

  printArray(newArray);
  printArray(mallocArray);

  axpy(newArray, stackArray);
  axpy(newArray, mallocArray);

  // delete stackArray;
  stackArray = 0;
  newArray = 0;
  mallocArray = 0;

  return 0;
}


