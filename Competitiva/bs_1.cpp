#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

int main() {
    int t;
    cin >> t;
    while (t--) {
        int n, m;
        cin >> n >> m;
        vector<int> a(m);
        for (int i = 0; i < m; i++) {
            cin >> a[i];
        }
        vector<int> cnt(n + 1);
        for (int i = 0; i < m; i++) {
            cnt[a[i]]++;
        }
        int ans = *max_element(cnt.begin(), cnt.end());
        cout << ans << endl;
    }
    return 0;
}