#include <iostream>
 
 using namespace std;
 long long g[1001],t[1001];
 long long find(long long r,long long k,long long n)
 {
   long long res=0,temp,i,j,ptr,count=0,flag,car;
   while(count < r)
     {
       //cout<<"\n inside start While 1 of FIND with count ="<<count<<" and res ="<<res;
       count++;
       temp = 0;
       ptr = 0;
       flag = 0;
       while(temp <= k && flag == 0)
 	{
 	  //cout<<"\n inside start While 2 of FIND with temp ="<<temp<<" and ptr ="<<ptr ;
 	  if(ptr<n)
 	    temp+=g[ptr++];
 	  else
 	    {
 	      flag = 1;
 	    }
 	  //cout<<"\n inside end   While 2 of FIND with temp ="<<temp<<" and ptr ="<<ptr ;
 	}
       if(flag == 0 && temp > k)
 	{
 	  temp-=g[--ptr];
 	}
       //cout<<"\n tenp before res:"<<temp<<" and res:"<<res;
       res += temp; 
       /*Array Modification*/
       if(flag == 0)
 	{
 	  //cout<<"\n In Array mod with ptr:"<<ptr;
 	  for(i=0;(ptr+i)<n;i++)
 	    {
 	      t[i]= g[ptr+i];
 	    }
 	  car = i;
 	  for(i=car;i<n;i++)
 	    {
 	      t[i]= g[i-car];
 	    }
 	  for(i=0;i<n;i++)
 	    g[i]=t[i];
 	  /* //Array printing
 	  cout<<endl;
 	  for(i=0;i<n;i++)
 	  cout<<" "<<g[i];*/
 	}
       //cout<<"\n inside end  While 1 of FIND with count ="<<count<<" and res ="<<res;
     }
   return res;
 }
 int main()
 {
   long long t,r,n,k,i,cnt,ans,tans;
   cin>>t;
   cnt = 0;
   // tans = find(4,6,4);
   //cout<<"\n"<<tans;
    while(cnt < t)
     {
       cnt++;
       cin>>r>>k>>n;      
       for(i=0;i<n;i++)
 	cin>>g[i];
       ans = find(r,k,n);
       cout<<"\nCase #"<<cnt<<": "<<ans;
     }
   return 0;
 }
   

