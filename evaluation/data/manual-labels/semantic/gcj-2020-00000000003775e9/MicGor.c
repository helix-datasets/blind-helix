#include <bits/stdc++.h>
using namespace std;

typedef long long LL;
typedef pair<int, int> PII;

#define sz(x) (int)(x).size()
#define all(x) (x).begin(), (x).end()

void solve()
{
    LL n, d;
    cin >> n >> d;
    LL x1, y1, x2, y2;
    cin >> x1 >> y1 >> x2 >> y2;
    LL k1 = abs(x1 + y1 - (x2 + y2)), k2 = abs(x1 - y1 - (x2 - y2));
    LL l1 = 2 * d - k1, l2 = 2 * d - k2;
    cerr << k1 << " " << l1 << "\n";
    cerr << k2 << " " << l2 << "\n";
    LL k = abs(x1 - x2) + abs(y1 - y2);
    if(k >= 2 * d)
    {
        cout << 0 << " " << 1 << "\n";
        return;
    }
    if(k >= d)
    {
        LL a = 3 * l1 * l2;
        LL b = 2 * (2 * d) * (2 * d) - l1 * l2;
        LL g = __gcd(a, b);
        cout << a / g << " " << b / g << "\n";
        return;
    }
    LL b = 2 * (2 * d) * (2 * d) - l1 * l2;
    LL a = b - 4 * k1 * k2;
    LL g = __gcd(a, b);
    cout << a / g << " " << b / g << "\n";
}

int main()
{
    ios_base::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);

    int t; cin >> t;
    for(int i = 1; i <= t; i++)
    {
        cout << "Case #" << i << ": ";
        solve();
    }

    return 0;
}
