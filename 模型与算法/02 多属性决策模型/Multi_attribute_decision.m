disp('请输入属性A的属性值（矩阵形式表达）');
% 列为属性，行为决策对象
A=input('A=');
%% 对属性值进行归一化处理
disp('请输入属性A的类型(效益型、成分型、固定型、偏离型、区间型、偏离区间型)');
% 效益型表示属性值越大越好，成分型表示属性值越小越好，固定型表示属性值越接近某一固定值越好，偏离型表示属性值越偏离某一固定值越好，区间型表示属性值越接近某一区间（包括在区间内）越好，偏离区间型表示属性值越偏离某一区间越好。
A_P=input('A_P=');
[A1,A2]=size(A);
if A_P=='效益型'  
    for i=1:A1
        M=max(A(i,:));
        m=min(A(i,:));
        for j=1:A2
            R(i,j)=A(i,j)/M;
%             或者R(i,j)=(A(i,j)-m)/(M-m);
        end
    end
    R
elseif A_P=='成分型'
    for i=1:A1
        M=max(A(i,:));
        m=min(A(i,:));
        for j=1:A2
            R(i,j)=m/A(i,j);
%             或者R(i,j)=(M-A(i,j))/(M-m);
        end
    end
    R
elseif A_P=='固定型'
    disp('请输入固定值a');
    a=input('a=');
    for i=1:A1
        M=max(abs(A(i,:)-a));
        for j=1:A2
            R(i,j)=1-(A(i,j)-a)/M;
        end
    end
    R
elseif A_P=='偏离型'
    disp('请输入偏离值a');
    a=input('a=');
    for i=1:A1
        M=max(abs(A(i,:)-a));
        m=min(abs(A(i,:)-a));
        for j=1:A2
            R(i,j)=abs(A(i,j)-a)-m/(M+m);
        end
    end
    R   
elseif A_P=='区间型'
    disp('请输入区间上限q2');
    q2=input('q2=');
    disp('请输入区间下限q1');
    q1=input('q1=');
    for i=1:A1
        M=max(A(i,:));
        m=min(A(i,:));
        for j=1:A2
            if A(i,j)<q1||A(i,j)>q2
                R(i,j)=1-max(q1-A(i,j),A(i,j)-q2)/max(q1-m,M-q2);
            else
                R(i,j)=1;
            end
        end
    end
    R   
elseif A_P=='偏离区间型'  
    disp('请输入区间上限q2');
    q2=input('q2=');
    disp('请输入区间下限q1');
    q1=input('q1=');
    for i=1:A1
        M=max(A(i,:));
        m=min(A(i,:));
        for j=1:A2
            if A(i,j)<q1||A(i,j)>q2
               R(i,j)=max(q1-A(i,j),A(i,j)-q2)/max(q1-m,M-q2);
            else
                R(i,j)=0;
            end
        end
    end
    R   
end

    
    