#include <iostream>
 #include <algorithm>
 
 using namespace std;
 
 bool empty[100][500];
 
 int dx[4] = { -1,0,1,0 };
 int dy[4] = { 0,1,0,-1 };
 
 int W,H;
 
 int dfs(int x,int y,int d) {
   // d = direction comming from: 0=down, 1=left, 2=up, 3=right
   //  cout << "Visit: " << x <<"," << y << " from " << d << endl;
   
   if (x<0 || x>=W || y<0 || y>=H || ! empty[x][y] ) return false;
 
   empty[x][y] = false;
 
   if (y==H-1) return true; // found a flow
 
   for (int i=1; i<=4; i++) {
     int dir = (d+i) % 4;
     if (dfs (x+dx[dir],y+dy[dir],(dir+2)%4 ))
       return true;
   }
   return false;
 };
 
 int main () {
   int T,B;
   
   cin >> T;
   for (int t=1; t<=T; t++) {
     cin >> W >> H >> B;
     for (int x=0; x<W; x++)
       for (int y=0; y<H; y++)
 	empty[x][y] = true;
 
     for (int i=0; i<B; i++) {
       int x0,y0,x1,y1;
       cin >> x0 >> y0 >> x1 >> y1;; 
       for (int x=x0; x<=x1; x++)
 	for (int y=y0; y<=y1; y++)
 	  empty[x][y] = false;
     }
     
     int flow=0;
     for (int x=0; x<W; x++)
       if (dfs(x,0,0)) flow++;
 
     cout << "Case #" << t << ": " << flow << endl;
   };
 };

