/* Tomasz [Tommalla] Zakrzewski, Google Code Jam 2010 /
 /  Qualification Round, Task 'Theme Park' */
 /* Optimized approach, complexicity: O(T*R*NlogN) */
 #include <cstdio>
 #include <algorithm>
 
 #define SIZE 1010
 
 using namespace std;
 
 unsigned int groups[SIZE];
 unsigned int sum[SIZE];
 unsigned int bsum;	//beginning sum
 
 inline bool cmp(const unsigned int &a, const unsigned int &b)
 {
     return a-bsum<=b;
 }
 
 int main()
 {
     unsigned int t,r,n,k,i,j,result,tempk;
     unsigned int* ptr;
     unsigned int* ptrEnd;
     scanf("%u",&t);
     for(i=1,result=0;i<=t;++i,result=0)
     {
 	scanf("%u%u%u",&r,&k,&n);
 	for(j=0;j<n;++j)
 	    scanf("%u",&groups[j]);
 	sum[0]=groups[0];
 	for(j=1;j<n;++j)
 	    sum[j]=sum[j-1]+groups[j];
 	ptr=sum;
 	while(r--)
 	{
 	     bsum=(ptr>sum)?(*(ptr-1)):0;
 	     ptrEnd=lower_bound(ptr,sum+n,k,cmp);
 	     if(ptrEnd==sum+n)
 	     {
 		 result+=*(ptrEnd-1)-bsum;
 		 tempk=k-(*(ptrEnd-1)-bsum);
 		 bsum=0;
 		 ptrEnd=lower_bound(sum,ptr,tempk,cmp);
 	     }
 	     result+=*(ptrEnd-1)-bsum;
 	     ptr=(ptrEnd<sum+n)?ptrEnd:sum;
 	}
 	printf("Case #%u: %u\n",i,result);
     }
     return 0;
 }

