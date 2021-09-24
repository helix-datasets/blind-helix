#include <bits/stdc++.h>
 
 using namespace std;
 
 int n, m;
 int grid[505][101];
 bool vis[505][101];
 int di[] = {1, 0, 0, -1};
 int dj[] = {0, 1, -1, 0};
 
 int dfs(int i, int j) {
   if(vis[i][j]) return 0;
   if(i == n - 1) return 1;
   vis[i][j] = 1;
   for(int k = 0; k < 4; ++k) {
     int ni = i + di[k];
     int nj = j + dj[k];
     if(ni < 0 || ni >= n || nj < 0 || nj >= m || grid[ni][nj] == -1)
       continue;
     if(dfs(ni, nj))
       return 1;
   }
   return 0;
 }
 
 int main() {
   freopen("C-small-attempt0.in", "rt", stdin);
   freopen("C-small-attempt0.out", "wt", stdout);
   int t; scanf("%d", &t);
   for(int tst = 1; tst <= t; ++tst) {
     int b; scanf("%d %d %d", &m, &n, &b);
     memset(grid, 0, sizeof grid);
     for(int k = 0; k < b; ++k) {
       int i0, j0, i1, j1;
       scanf("%d %d %d %d", &j0, &i0, &j1, &i1);
       for(int i = i0; i <= i1; ++i)
         for(int j = j0; j <= j1; ++j)
           grid[i][j] = -1;
     }
     int ans = 0;
     memset(vis, 0, sizeof vis);
     for(int j = 0; j < m - 1; ++j) if(grid[0][j] != -1 && !vis[0][j]) {
       ans += dfs(0, j);
     }
     printf("Case #%d: %d\n", tst, ans);
   }
   return 0;
 }

