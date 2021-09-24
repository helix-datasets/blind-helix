#include <stdio.h>
 #include <algorithm>
 #include <vector>
 #include <map>
 #include <set>
 #include <string>
 
 using namespace std;
 class Lv{
 public:
 	int L, P, num;
 	const bool operator < (const Lv l) const {
 		if (P == 0 && l.P != 0) return false;
 		if (P != 0 && l.P == 0) return true;
 		if (P == 0 && l.P == 0) return num < l.num;
 		// L/P < l.L / l.P
 		return L*l.P < l.L*P;
 	}
 } dat[1010];
 
 int main(){
 	//freopen("input.txt","r",stdin);
 	//freopen("output.txt","w",stdout);
 	
 	freopen("A-small-attempt0.in","r",stdin);
 	freopen("A-small-attempt0.out","w",stdout);
 	int T;
 	scanf("%d",&T);
 	while(T-->0) {
 		//
 		int N;
 		scanf("%d",&N);
 		int i;
 		for(i=0;i<N;i++){
 			scanf("%d",&dat[i].L);
 		}
 		for(i=0;i<N;i++){
 			scanf("%d",&dat[i].P);
 		}
 		for(i=0;i<N;i++) dat[i].num = i;
 		sort(dat, dat+N);
 
 
 		static int cs = 1;
 		printf("Case #%d:", cs ++);
 		for(i=0;i<N;i++){
 			printf(" %d", dat[i].num);
 		}
 		printf("\n");
 	}
 	return 0;
 }
