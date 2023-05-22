#include <iostream>
#include <boost/multiprecision/cpp_int.hpp>
using namespace std;
using namespace boost::multiprecision;

int main() {
    int n;
    cout << "Enter a positive integer: ";
    cin >> n;
    cpp_int factorial = 1;
    for(int i = 1; i <=n; ++i) {
        factorial *= i;
    }
    cout << "Factorial of " << n << " = " << factorial;    
    return 0;
}
