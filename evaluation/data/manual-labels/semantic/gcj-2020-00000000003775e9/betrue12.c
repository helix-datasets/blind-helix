#include <bits/stdc++.h>
using namespace std;

int64_t gcd(int64_t a, int64_t b){
    return b==0 ? a : gcd(b, a%b);
}

void solve(int casenum){
    cout << "Case #" << casenum << ": ";
    int N;
    int64_t D;
    cin >> N >> D;
    vector<int64_t> XX(N), YY(N);
    for(int i=0; i<N; i++){
        int x, y;
        cin >> x >> y;
        XX[i] = x+y, YY[i] = x-y;
    }
    int64_t X = abs(XX[0] - XX[1]), Y = abs(YY[0] - YY[1]);
    if(X > Y) swap(X, Y);
    if(Y >= 2*D){
        cout << "0 1" << endl;
        return;
    }
    int64_t dx = 2*D-X, dy = 2*D-Y;
    int64_t ALL = 8*D*D - dx*dy, active;
    if(dy <= D){
        active = 3*dx*dy;
    }else{
        active = ALL - 4*(X-dx)*(Y-dy);
    }
    int64_t g = gcd(ALL, active);
    ALL /= g;
    active /= g;
    cout << active << " " << ALL << endl;
}

int main() {
    int T;
    cin >> T;
    for(int i=1; i<=T; i++) solve(i);
    return 0;
}
