#include<stdio.h>
 #include<string.h>
 #include<stdlib.h>
 #include<iostream>
 #include<algorithm>
 using namespace std;
 
 int n,s[2000],p[2000],q[2000];
 int cmp(int a, int b){
 	if(p[a] == p[b]){
 		if(s[a] == s[b])
 			return a < b;
 		return s[a] > s[b];
 	}
 	return p[a] > p[b];
 }
 int main(void){
 	int t;
 	scanf("%d",&t);
 	for(int tt=1;tt<=t;tt++){
 		scanf("%d",&n);
 		for(int i=0;i<n;i++)
 			scanf("%d",&s[i]);
 		for(int i=0;i<n;i++)
 			scanf("%d",&p[i]);
 		for(int i=0;i<n;i++)
 			q[i]=i;
 		sort(q,q+n,cmp);
 		printf("Case #%d:", tt);
 		for(int i=0;i<n;i++)
 			printf(" %d", q[i]);
 		puts("");
 	}
 	
 	return 0;
 }

