#include <iostream>
#include <boost/multiprecision/cpp_int.hpp>

using namespace std;
using namespace boost::multiprecision;

int main() {
    int n;
    cpp_int factorial = 1;

    cout << "Introduce un numero: ";
    cin >> n;

    for(int i = 1; i <=n; ++i) {
        factorial *= i;
    }

    cout << "Factorial de " << n << " = " << factorial;    
    return 0;
}
