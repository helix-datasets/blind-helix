#include <cstdio>
 #include <algorithm>
 #define N 505
 #define M 105
 #define fi(a, b, c) for(int a = (b); a < (c); a++)
 #define fd(a, b, c) for(int a = (b); a > (c); a--)
 #define FI(a, b, c) for(int a = (b); a <= (c); a++)
 #define FD(a, b, c) for(int a = (b); a >= (c); a--)
 #define fe(a, b, c) for(int a = (b); a; a = c[a])
 using namespace std;
 
 int t, n, m, b, dy[] = {1, 0, -1, 0}, dx[] = {0, 1, 0, -1};
 bool map[N][M];
 
 bool dfs(int y, int x, int d){
 	//printf("dfs %d %d %d\n", y, x, d);
 	map[y][x] = 1;
 	if(y == n - 1) return 1;
 	FI(i, -1, 1){
 		int dir = (d + i + 4) % 4, ny = y + dy[dir], nx = x + dx[dir];
 		//printf("dir %d\n", dir);
 		if(ny < 0 || ny >= n || nx < 0 || nx >= m || map[ny][nx]) continue;
 		if(dfs(ny, nx, dir)) return 1;
 	}
 	
 	return 0;
 }
 
 void solve(){
 	scanf("%d %d %d", &m, &n, &b);
 	fi(i, 0, n) fi(j, 0, m) map[i][j] = 0;
 	fi(i, 0, b){
 		int x0, y0, x1, y1;
 		scanf("%d %d %d %d", &x0, &y0, &x1, &y1);
 		FI(j, y0, y1) FI(k, x0, x1) map[j][k] = 1;
 	}
 	
 	int ans = 0;
 	fi(i, 0, m) if(!map[0][i]){
 		//printf("try %d\n", i);
 		ans += dfs(0, i, 0);
 	}
 	printf("%d\n", ans);
 }
 
 int main(){
 	freopen("C-small-attempt0.in", "r", stdin);
 	freopen("C-small-attempt0.out", "w", stdout);
 	scanf("%d", &t);
 	FI(z, 1, t){
 		printf("Case #%d: ", z);
 		solve();
 	}
 	scanf("\n");
 }

