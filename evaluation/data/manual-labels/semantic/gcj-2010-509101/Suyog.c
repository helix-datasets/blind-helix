#include<iostream>
 
 using namespace std;
 
 int main()
 {
     int T, g[1004], next[1004], nsum[1004];
     cin>>T;
     for(int t = 1; t <= T; t++)
     {
         int R, K, N;
         cin>>R>>K>>N;
 
         long long sum = 0;
 
         for(int i = 0; i < N; i++)
         {
             cin>>g[i];
             sum += g[i];
         }
 
         if(sum <= K)
         {
             cout<<"Case #"<<t<<": "<<(sum * R)<<endl;
             continue;
         }
         
         int j = 0;
         sum = 0;
         for(int i = 0; i < N; i++)
         {
             while(sum + g[j] <= K)
             {
                 sum += g[j];
                 j++;
                 j %= N;
             }
 
             next[i] = j;
             nsum[i] = sum;
             sum -= g[i];
         }
 
         long long res = 0;
         int cur = 0;
         for(int r = 0; r < R; r++)
         {
             res += nsum[cur];
             cur = next[cur];
         }
 
         cout<<"Case #"<<t<<": "<<res<<endl;
     }
 
     return 0;
 }
 

