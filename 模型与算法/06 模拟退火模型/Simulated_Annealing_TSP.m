clear;
% 程 序 参 数 设 定
Coord = ... % 城 市 的 坐 标 Coordinates
 [ 66.83 61.95 40    24.39 17.07 22.93 51.71 87.32 68.78 84.88 50 40 25 ; 
   25.36 26.34 44.39 14.63 22.93 76.1  94.14 65.36 52.19 36.09 30 20 26] ;
t0 = 1 ; % 初 温 t0
iLk = 20 ; % 内 循 环 最 大 迭 代 次 数 iLk
oLk = 50 ; % 外 循 环 最 大 迭 代 次 数 oLk
lam = 0.95 ; % λ lambda
istd = 0.001 ; % 若 内 循 环 函 数 值 方 差 小 于 istd 则 停 止
ostd = 0.001 ; % 若 外 循 环 函 数 值 方 差 小 于 ostd 则 停 止
ilen = 5 ; % 内 循 环 保 存 的 目 标 函 数 值 个 数
olen = 5 ; % 外 循 环 保 存 的 目 标 函 数 值 个 数
% 程 序 主 体
m = length( Coord ) ; % 城 市 的 个 数 m
fare = distance( Coord ) ; % 路 径 费 用 fare
path = 1 : m ; % 初 始 路 径 path
pathfar = pathfare( fare , path ) ; % 路 径 费 用 path fare
ores = zeros( 1 , olen ) ; % 外 循 环 保 存 的 目 标 函 数 值
e0 = pathfar ; % 能 量 初 值 e0
t = t0 ; % 温 度 t
for out = 1 : oLk % 外 循 环 模 拟 退 火 过 程
ires = zeros( 1 , ilen ) ; % 内 循 环 保 存 的 目 标 函 数 值
for in = 1 : iLk % 内 循 环 模 拟 热 平 衡 过 程
[ newpath , v ] = swap( path , 1 ) ; % 产 生 新 状 态
e1 = pathfare( fare , newpath ) ; % 新 状 态 能 量
% Metropolis 抽 样 稳 定 准 则
r = min( 1 , exp( - ( e1 - e0 ) / t ) ) ;
if rand < r
path = newpath ; % 更 新 最 佳 状 态
e0 = e1 ;
end
ires = [ ires( 2 : end ) e0 ] ; % 保 存 新 状 态 能 量
% 内 循 环 终 止 准 则 ：连 续 ilen 个 状 态 能 量 波 动 小 于 istd
if std( ires , 1 ) < istd
break ;
end
end
ores = [ ores( 2 : end ) e0 ] ; % 保 存 新 状 态 能 量
% 外 循 环 终 止 准 则 ：连 续 olen 个 状 态 能 量 波 动 小 于 ostd
if std( ores , 1 ) < ostd
break ;
end
t = lam * t ;
end
pathfar = e0 ;
% 输 入 结 果
fprintf( '近似最优路径为：\n ' )
%disp( char( [ path , path(1) ] + 64 ) ) ;
disp(path)
fprintf( '近似最优路径路程\tpathfare=' ) ;
disp( pathfar ) ;
myplot( path , Coord , pathfar ) ;