#include<iostream>
 #include<stdio.h>
 #include<string>
 #include<string.h>
 #include<algorithm>
 #include<vector>
 #include<map>
 using namespace std;
 
 int l[2000],p[2000];
 int b[2000];
 int main()
 {
     int t;
     cin>>t;
     for(int tt=1;tt<=t;tt++)
     {
         int n;
         cin>>n;
         cout<<"Case #"<<tt<<":";
         for(int i=0;i<n;i++)
             cin>>l[i];
         for(int i=0;i<n;i++)
         {
             cin>>p[i];
             p[i]=100-p[i];
         }
         memset(b,0,sizeof(b));
         for(int i=0;i<n;i++)
         {
             int min=100000,mini;
             for(int j=0;j<n;j++)
             {
                 if(!b[j]&&p[j]<min)
                 {
                     min=p[j];
                     mini=j;
                 }
             }
             cout<<" ";
             cout<<mini;
             b[mini]=1;
         }
         cout<<endl;
 
 
     }
 
     return 0;
 }

