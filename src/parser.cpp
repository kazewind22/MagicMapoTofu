#include<cstdio>
#include<map>
#include<vector>
#include<cassert>
using namespace std;
typedef unsigned long long int unt;
typedef double dou;
typedef pair<dou,int> P;
map<vector<unt> ,P>mp;
int myget(vector<unt>&a,dou&y,int&z){
	for(int i=0;i<30;i++){
		unt x;
		if(scanf("%I64u",&x)==EOF)return 0;
		a.push_back(x);
	}
	if(scanf("%lf %d",&y,&z)==EOF)return 0;
	return 1;
}
char fn[10][100]={
	"count_win.txt",
	"count_win_Yuehs_271_BLACK.txt",
	"count_win_Yuehs_271_WHITE.txt",
	"count_win_anti_271_BLACK.txt",
	"count_win_anti_271_WHITE.txt"
};
int main(){
	for(int k=0;k<5;k++){
		mp.clear();
		freopen(fn[k],"r",stdin);
		dou y;
		int z;
		vector<unt>ID;
		for(;myget(ID,y,z);){
			P t=mp[ID];
			mp[ID]=P((t.first*t.second+y*z)/(t.second+z),t.second+z);
			ID.clear();
		}
		freopen(fn[k],"w",stdout);
		for(auto&it:mp){
			for(auto&jt:it.first){
				printf("%I64u ",jt);
			}
			printf("%+.10f %d\n",it.second.first,it.second.second);
		}	
	}
	return 0;
}

