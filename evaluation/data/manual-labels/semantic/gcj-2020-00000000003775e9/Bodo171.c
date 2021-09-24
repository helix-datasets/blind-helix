#include <bits/stdc++.h>

using namespace std;
long long oldx[10],oldy[10],x[10],y[10];
long long area(long long X1,long long X2,long long Y1,long long Y2){
    if(X1>X2||Y1>Y2)
        return 0;
    return (X2-X1)*(Y2-Y1);
}
long long gcd(long long A,long long B){
    if((!A)||(!B)) return A+B;
    return gcd(B,A%B);
}
void solve_testcase(int cnt){
    int n;
    long long d;
    cin>>n>>d;
    for(int i=0;i<n;i++){
        cin>>oldx[i]>>oldy[i];
        x[i]=oldx[i]-oldy[i];
        y[i]=oldx[i]+oldy[i];
    }
    long long area1,area2;
    area1=area(x[0]-d,x[0]+d,y[0]-d,y[0]+d);
    area2=area(x[1]-d,x[1]+d,y[1]-d,y[1]+d);
    long long rX=min(x[0]+d,x[1]+d),lX=max(x[0]-d,x[1]-d),rY=min(y[0]+d,y[1]+d),lY=max(y[0]-d,y[1]-d);
    long long common=area(lX,rX,lY,rY);
    long long dX=rX-lX,dY=rY-lY;
    long long autoIntersect=area(2*d-dX,dX,2*d-dY,dY);
    long long d1,d2;
    d1=3*common-2*autoIntersect;
    d2=area1+area2-common;
    long long G=gcd(d1,d2);
    d1/=G,d2/=G;
    cout<<"Case #"<<cnt<<": "<<d1<<' '<<d2;
    cout<<"\n";
}
int main()
{
    //freopen("data.in","r",stdin);
    int t=0;
    cin>>t;
    for(int cnt=1;cnt<=t;cnt++)
        solve_testcase(cnt);
    return 0;
}
