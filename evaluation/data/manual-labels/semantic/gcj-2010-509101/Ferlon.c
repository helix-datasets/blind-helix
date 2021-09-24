#include <cstdio>
 #include <cstring>
 //#include <iostream>
 using namespace std;
 typedef long long ll;
 const int c=1010;
 int g[c];
 ll ans;
 bool b[c];
 int nk[c];
 ll eu[c];
 int n,k,r,t,ii;
 int main() {
 	int i,tmp,p,dp,nj;
 	bool q;
 	scanf("%d",&t);
 	for (ii=1; ii<=t; ++ii) {
 		printf("Case #%d: ",ii);
 		memset(b,0,sizeof(b));
 		scanf("%d%d%d",&r,&k,&n);
 		for (i=0; i<n; ++i) scanf("%d",&g[i]);
 		b[0]=1;
 		nk[1]=0;
 		eu[1]=0;
 		p=0;
 		q=0;
 		ans=0;
 		for (i=1; i<=r; ++i) {
 			tmp=0;
 			nj=0;
 			while (1) {
 				tmp+=g[p];
 				++nj;
 				p=(p+1)%n;
 				if (tmp>k || nj==n) break;
 			}
 			if (tmp>k) {
 				p=(p+n-1)%n;
 				tmp-=g[p];
 			}
 //			cerr << i << ' ' << p << ' ' << tmp << '\n';
 			ans+=tmp;
 			if (b[p] && !q) {
 				dp=(r-i)/(i-nk[p]);
 				ans+=(ans-eu[p])*dp;
 				i+=(i-nk[p])*dp;
 				q=1;
 			} else {
 				b[p]=1;
 				eu[p]=ans;
 				nk[p]=i;
 			}
 		}
 		printf("%I64Ld\n",ans);
 	}
 	return 0;
 }
