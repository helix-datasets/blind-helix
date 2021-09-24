#include <iostream>
 #include <fstream>
 #include <cstdio>
 #include <algorithm>
 #include <vector>
 #include <queue>
 #include <list>
 #include <map>
 #include <set>
 #include <string>
 #include <cmath>
 #include <stdlib.h>
 #include <string.h>
 #include <iomanip>
 using namespace std;
 
 struct str{
 	int num;
 	int prob;
 	int l;
 	bool operator<(const str& o)const{
 		if(prob!=o.prob) return prob>o.prob;
 		if(l!=o.l) return l>o.l;
 		return num<o.num;
 	}
 };
 str a[1100];
 
 int main(){
 	ifstream cin("input.txt");
 	ofstream cout("output.txt");
 	int ntests;
 	cin>>ntests;
 	for(int testnum=0; testnum<ntests; testnum++){
 		int n;
 		cin>>n;
 		for(int i=0; i<n; i++){
 			a[i].num = i;
 			cin>>a[i].l;
 		}
 		for(int i=0; i<n; i++){
 			cin>>a[i].prob;
 		}
 		sort(&a[0],&a[n]);
 		cout<<"Case #"<<testnum+1<<":";
 		for(int i=0; i<n; i++) cout<<' '<<a[i].num;
 		cout<<endl;
 	}
 	return 0;
 }

