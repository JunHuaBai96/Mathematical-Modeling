x=[150,85,150,145,130,0]; %各架飞机的位置初始值横坐标xi0
y=[140,85,155,50,150,0]; %各架飞机的位置初始值横坐标yi0
c=[5,4,2,1,6,3]; %指定点的颜色（RGB）
axis([-10,195,-10,170]); %设置坐标轴范围
grid on;
hold on;
plot([0,160,160,0,0],[0,0,160,160,0],'b'); %用黑色方框表示区域
zt=[243,236,220.5,159,230,52];  %各架飞机的飞行方向初始值角（度，与x轴正向的夹角）
zt1=zt*pi/180;  %各架飞机的飞行方向初始值角化为弧度
vt=1;  %这里假设速度为1km/0.1s
dx=vt*cos(zt1);
dy=vt*sin(zt1); %用参数方程表示各架飞机的位置
for n=1:120
    x1=x+dx;
    y1=y+dy;
    scatter(x1,y1,10,c,'filled');  %给每架飞机轨迹设置不同的颜色
    for j=1:5
        for k=2:6
            if k~=j
                tx=x1(j)-x1(k);
                ty=y1(j)-y1(k);
                dl=sqrt(tx*tx+ty*ty);  %计算两架飞机的瞬时距离
                if dl<=8
                    fpromtf('\ni=%d j=%d n=%d',j,k,n);  %储存距离小于8km时的飞机编号和时间
                end  
            end
        end
    end
    x=x1;
    y=y1;
    pause(0.1);
end  