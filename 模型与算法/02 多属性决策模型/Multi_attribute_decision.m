disp('����������A������ֵ��������ʽ��');
% ��Ϊ���ԣ���Ϊ���߶���
A=input('A=');
%% ������ֵ���й�һ������
disp('����������A������(Ч���͡��ɷ��͡��̶��͡�ƫ���͡������͡�ƫ��������)');
% Ч���ͱ�ʾ����ֵԽ��Խ�ã��ɷ��ͱ�ʾ����ֵԽСԽ�ã��̶��ͱ�ʾ����ֵԽ�ӽ�ĳһ�̶�ֵԽ�ã�ƫ���ͱ�ʾ����ֵԽƫ��ĳһ�̶�ֵԽ�ã������ͱ�ʾ����ֵԽ�ӽ�ĳһ���䣨�����������ڣ�Խ�ã�ƫ�������ͱ�ʾ����ֵԽƫ��ĳһ����Խ�á�
A_P=input('A_P=');
[A1,A2]=size(A);
if A_P=='Ч����'  
    for i=1:A1
        M=max(A(i,:));
        m=min(A(i,:));
        for j=1:A2
            R(i,j)=A(i,j)/M;
%             ����R(i,j)=(A(i,j)-m)/(M-m);
        end
    end
    R
elseif A_P=='�ɷ���'
    for i=1:A1
        M=max(A(i,:));
        m=min(A(i,:));
        for j=1:A2
            R(i,j)=m/A(i,j);
%             ����R(i,j)=(M-A(i,j))/(M-m);
        end
    end
    R
elseif A_P=='�̶���'
    disp('������̶�ֵa');
    a=input('a=');
    for i=1:A1
        M=max(abs(A(i,:)-a));
        for j=1:A2
            R(i,j)=1-(A(i,j)-a)/M;
        end
    end
    R
elseif A_P=='ƫ����'
    disp('������ƫ��ֵa');
    a=input('a=');
    for i=1:A1
        M=max(abs(A(i,:)-a));
        m=min(abs(A(i,:)-a));
        for j=1:A2
            R(i,j)=abs(A(i,j)-a)-m/(M+m);
        end
    end
    R   
elseif A_P=='������'
    disp('��������������q2');
    q2=input('q2=');
    disp('��������������q1');
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
elseif A_P=='ƫ��������'  
    disp('��������������q2');
    q2=input('q2=');
    disp('��������������q1');
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

    
    