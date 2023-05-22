#include <bits/stdc++.h>
using namespace std;

void solve(){
    int n; cin >> n;
    int c; cin >> c;
    vector<int>
}

int main() {

    ios::sync_with_stdio(NULL);
    cin.tie(NULL);
    cout.tie(NULL);

    int t;
    cin >> t;

    while (t--)
    {
        int a, b;
        cin >> a >> b;
        vector<int> n;

        for (int i = 0; i < a; i++)
        {
            int x;
            cin >> x;
            n.push_back(x);
        }

        for (int i = 0; i < b; i++)
        {
            int x;
            cin >> x;
            cout << poli(n, x) << endl;

        }

    }
    return 0;
}