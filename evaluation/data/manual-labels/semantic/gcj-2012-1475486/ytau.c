
 
 
 #include <iostream>
 #include <iomanip>
 #include <fstream>
 
 #include <cmath>
 #include <cstdio>
 #include <cstdlib>
 #include <cstring>
 #include <ctime>
 
 #include <sstream>
 #include <string>
 
 #include <bitset>
 #include <deque>
 #include <list>
 #include <map>
 #include <set>
 #include <queue>
 #include <stack>
 #include <vector>
 
 #include <algorithm>
 
 #include <utility>
 
 using namespace std;
 
 
 
 const int inf = 2000000000;
 const long long linf = 9000000000000000000LL;
 const double finf = 1.0e18;
 const double eps = 1.0e-8;
 
 int T, n, l[1005], p[1005], o[1005];
 
 bool fo(int i, int j) {
 	return p[i]>p[j];
 }
 
 int main() {
 
 	scanf("%d",&T);
 	for (int tt=1; tt<=T; tt++) {
 		scanf("%d",&n);
 		for (int i=0; i<n; i++) {
 			scanf("%d",&l[i]);
 		}
 		for (int i=0; i<n; i++) {
 			scanf("%d",&p[i]);
 		}
 		for (int i=0; i<n; i++) {
 			o[i] = i;
 		}
 		stable_sort(o, o+n, fo);
 		printf("Case #%d:", tt);
 		for (int i=0; i<n; i++) {
 			printf(" %d", o[i]);
 		}
 		printf("\n");
 	}
 	
 	return 0;
 }
 
 

