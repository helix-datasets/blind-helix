#include <list>
 #include <map>
 #include <set>
 #include <stack>
 #include <queue>
 #include <algorithm>
 #include <sstream>
 #include <iostream>
 #include <cstdio>
 #include <cmath>
 #include <cstdlib>
 #include <cstring>
 #include <climits>
 #include <cfloat>
 #include <numeric>
 
 using namespace std;
 
 const int oo = 0x3f3f3f3f;
 const double eps = 1e-9;
 
 typedef long long ll;
 typedef unsigned long long ull;
 typedef vector<int> vi;
 typedef vector<string> vs;
 typedef pair<int, int> pii;
 
 #define sz(c) int((c).size())
 #define all(c) (c).begin(), (c).end()
 #define FOR(i,a,b) for (int i = (a); i < (b); i++)
 #define FORD(i,a,b) for (int i = int(b)-1; i >= (a); i--)
 #define FORIT(i,c) for (__typeof__((c).begin()) i = (c).begin(); i != (c).end(); i++)
 
 int T, W, H, B;
 bool mark[110][510];
 
 int dx[4] = {0, 1, 0, -1};
 int dy[4] = {1, 0, -1, 0};
 
 bool dfs(int x, int y, int d) {
   if (x < 0 || x >= W) return false;
   if (y < 0) return false;
   if (y >= H) return true;
   if (mark[x][y]) return false;
   mark[x][y] = true;
   FOR(i, -1, 2) {
     int dd = (d + i + 4) % 4;
     int xx = x + dx[dd], yy = y + dy[dd];
     if (dfs(xx, yy, dd)) return true;
   }
   return false;
 }
 
 int main() {
   cin >> T;
   FOR(cs, 1, T+1) {
     cin >> W >> H >> B;
     memset(mark, 0, sizeof(mark));
     FOR(i, 0, B) {
       int x0, y0, x1, y1;
       cin >> x0 >> y0 >> x1 >> y1;
       FOR(j, x0, x1+1) FOR(k, y0, y1+1) mark[j][k] = true;
     }
     int res = 0;
     FOR(i, 0, W) if (dfs(i, 0, 0)) res++;
     cout << "Case #" << cs << ": " << res << endl;
   }
 	return 0;
 }

