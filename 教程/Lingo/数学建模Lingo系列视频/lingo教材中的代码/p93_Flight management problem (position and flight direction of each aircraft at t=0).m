x=[150,85,150,145,130,0]; %各架飞机的位置初始值横坐标xi0
y=[140,85,155,50,150,0]; %各架飞机的位置初始值横坐标yi0
scatter(x,y,30,'r','filled'); %在坐标轴上设置各架飞机的初始位置
axis([-10,195,-10,170]); %设置坐标轴范围
grid on;
hold on;
plot([0,160,160,0,0],[0,0,160,160,0],'b'); %用黑色方框表示区域
zt=[243,236,220.5,159,230,52];  %各架飞机的飞行方向初始值角（度，与x轴正向的夹角）
zt1=zt*pi/180;  %各架飞机的飞行方向初始值角化为弧度
b=40;
x1=x+b*cos(zt1);
y1=y+b*sin(zt1); %用参数方程表示各架飞机的飞行方向
for n=1:6
    plot([x(n),x1(n)],[y(n),y1(n)],'k');
end  %绘制各架飞机的飞行方向


