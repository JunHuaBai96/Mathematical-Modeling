clear;
% �� �� �� �� �� ��
Coord = ... % �� �� �� �� �� Coordinates
 [ 66.83 61.95 40    24.39 17.07 22.93 51.71 87.32 68.78 84.88 50 40 25 ; 
   25.36 26.34 44.39 14.63 22.93 76.1  94.14 65.36 52.19 36.09 30 20 26] ;
t0 = 1 ; % �� �� t0
iLk = 20 ; % �� ѭ �� �� �� �� �� �� �� iLk
oLk = 50 ; % �� ѭ �� �� �� �� �� �� �� oLk
lam = 0.95 ; % �� lambda
istd = 0.001 ; % �� �� ѭ �� �� �� ֵ �� �� С �� istd �� ͣ ֹ
ostd = 0.001 ; % �� �� ѭ �� �� �� ֵ �� �� С �� ostd �� ͣ ֹ
ilen = 5 ; % �� ѭ �� �� �� �� Ŀ �� �� �� ֵ �� ��
olen = 5 ; % �� ѭ �� �� �� �� Ŀ �� �� �� ֵ �� ��
% �� �� �� ��
m = length( Coord ) ; % �� �� �� �� �� m
fare = distance( Coord ) ; % · �� �� �� fare
path = 1 : m ; % �� ʼ · �� path
pathfar = pathfare( fare , path ) ; % · �� �� �� path fare
ores = zeros( 1 , olen ) ; % �� ѭ �� �� �� �� Ŀ �� �� �� ֵ
e0 = pathfar ; % �� �� �� ֵ e0
t = t0 ; % �� �� t
for out = 1 : oLk % �� ѭ �� ģ �� �� �� �� ��
ires = zeros( 1 , ilen ) ; % �� ѭ �� �� �� �� Ŀ �� �� �� ֵ
for in = 1 : iLk % �� ѭ �� ģ �� �� ƽ �� �� ��
[ newpath , v ] = swap( path , 1 ) ; % �� �� �� ״ ̬
e1 = pathfare( fare , newpath ) ; % �� ״ ̬ �� ��
% Metropolis �� �� �� �� ׼ ��
r = min( 1 , exp( - ( e1 - e0 ) / t ) ) ;
if rand < r
path = newpath ; % �� �� �� �� ״ ̬
e0 = e1 ;
end
ires = [ ires( 2 : end ) e0 ] ; % �� �� �� ״ ̬ �� ��
% �� ѭ �� �� ֹ ׼ �� ���� �� ilen �� ״ ̬ �� �� �� �� С �� istd
if std( ires , 1 ) < istd
break ;
end
end
ores = [ ores( 2 : end ) e0 ] ; % �� �� �� ״ ̬ �� ��
% �� ѭ �� �� ֹ ׼ �� ���� �� olen �� ״ ̬ �� �� �� �� С �� ostd
if std( ores , 1 ) < ostd
break ;
end
t = lam * t ;
end
pathfar = e0 ;
% �� �� �� ��
fprintf( '��������·��Ϊ��\n ' )
%disp( char( [ path , path(1) ] + 64 ) ) ;
disp(path)
fprintf( '��������·��·��\tpathfare=' ) ;
disp( pathfar ) ;
myplot( path , Coord , pathfar ) ;