#include <bits/stdc++.h>
using namespace std;

#define pb push_back
#define X first
#define Y second
#define mp make_pair
typedef long long ll;

int n;
ll d;
ll ans;

ll myabs(ll a) { return a > 0 ? a : -a; }
ll mygcd(ll a, ll b) { return a % b ? mygcd(b, a%b) : b; }

void init() {
}

void solve() {
	scanf("%d %d", &n, &d);
	if (n != 2) {
		puts("0 1");
		return;
	}

	ll a = d * d * 4 * 2, b, c;
	ll x1, y1, x2, y2;
	scanf("%d %d %d %d", &x1, &y1, &x2, &y2);
	ll a1 = d * 2 - myabs(x1 + y1 - x2 - y2);
	ll a2 = d * 2 - myabs(x1 - y1 - x2 + y2);
	if (a1 <= 0 || a2 <= 0) {
		puts("0 1");
		return;
	}
	if (a1 > 0 && a2 > 0) b = a - a1 * a2;
	c = a1 * a2 * 3;
	if (a1 > d && a2 > d) c -= (a1 - d)*(a2 - d) * 2;

	ll g = mygcd(c, b);
	c /= g; b /= g;
	printf("%lld %lld\n", c, b);
}

int main() {
	int t;
	scanf("%d", &t);
	for (int tn = 1; tn <= t; tn++) {
		printf("Case #%d: ", tn);
		init();
		solve();
	}
}
