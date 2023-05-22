#include <bits/stdc++.h>
using namespace std;

bool cumple(int tiempo, int n, vector<int>& a)
{
    int64_t falta = 0;
    int64_t sobra = 0;
    for(int i = 1; i <= n; i++){
        if(a[i] <= tiempo) sobra += (tiempo - a[i])/2;
        else               falta += a[i] - tiempo; 
    }
    return sobra >= falta;
}

int main() {

    ios::sync_with_stdio(NULL);
    cin.tie(NULL);
    cout.tie(NULL); 

    int t;
    cin >> t;

    while (t--)
    {
        int n, m;
        cin >> n >> m;
        vector<int> a(n + 1);

        for (int i = 0; i < m; i++)
        {
            int x;
            cin >> x;
            a[x]++;
        }

        int mini = 0;
        int64_t max = 1000000000;
        while(max - mini > 1){
            int tmp = mini + ((max - mini) / 2);
            if(cumple(tmp , n , a ))
                max = tmp;
            else    
                mini = tmp;
        }
        cout << max << endl;
    }
    return 0;
}