#include <stdlib.h>
 #include <cstdio>
 
 using namespace std;
 
 typedef long long ll;
 
 #define REP(i, n) for (int i = 0; i < (n); ++i)
 #define FOR(k, a, b) for (typeof(a) k = (a); k < (b); ++k)
 #define SIZE(x) ((int)(x).size())
 #define NEXT_POS(pos, n) ((pos + 1) % n)
 
 int main() {
     int t, r, k, n, pos, nextPos, nextGroup, count;
     ll income = 0;
     int* g = new int[1000];
 
     scanf("%d\n", &t);
     REP(i, t) {
         scanf("%d %d %d\n", &r, &k, &n);
         REP(j, n) scanf("%d", (g + j));
 
         income = 0;
         pos = 0;
         REP(j, r) {
             count = g[pos];
             nextPos = NEXT_POS(pos, n);
             nextGroup = g[nextPos];
 
             while (nextPos != pos && count + nextGroup <= k) {
                 count += nextGroup;
                 nextPos = NEXT_POS(nextPos, n);
                 nextGroup = g[nextPos];
             }
             pos = nextPos;
 
             income += count;
         }
         printf("Case #%d: %lld\n", i+1, income);
     }
 
     return 0;
 }
 

