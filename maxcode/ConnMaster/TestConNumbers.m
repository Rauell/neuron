function [Errors, ErrorsMean, connStruct] = TestConNumbers(choice)

%{
    This program will test the overall numbers of connections that SHOULD
    be created VS actual connections in a model using various connectivity
    patterns.  

    INPUT

    choice = Which type of connectivity to test over

    OUTPUT

    Errors = matrix of individual differences between expected and actual
    connections
    ErrorsMean = mean difference of Errors
    connStruct = Connectivity structure with several fields determining
    types of connectivity networks

    Max Henderson and Micheal Royster
    Drexel University
    Last updated April 13, 2015
%}


n = [50, 100, 500, 1000];
connStruct = CreateConnectivityStructure();
connStruct.L = 100;
T = 10;
Errors = zeros(T,4);
ErrorsMean = zeros(4,4);
connStruct.CEE = choice;
connStruct.CEI = choice;
connStruct.CIE = choice;
connStruct.CII = choice;

for i = 1 : length(n),
    
        connStruct.N = n(i);
        
        for j = 1 : T,
            j
            data = connStruct.L*rand(connStruct.N,3);
            [ID, NE] = MakeRandomID(connStruct.N);
            connStruct.ID = ID;
            connStruct.NE = NE;
            connStruct.NI = connStruct.N - NE;
            connStruct = CreateDistanceMatrices(connStruct, data); 
            [C, c] = CreateConnectivityMatrix(connStruct, 1);
            Errors(j,1) = abs((sum(sum(C))-c)/c);
            [C, c] = CreateConnectivityMatrix(connStruct, 2);  
            Errors(j,2) = abs((sum(sum(C))-c)/c);
            [C, c] = CreateConnectivityMatrix(connStruct, 3);  
            Errors(j,3) = abs((sum(sum(C))-c)/c);
            [C, c] = CreateConnectivityMatrix(connStruct, 4);
            Errors(j,4) = abs((sum(sum(C))-c)/c);
            
        end
        
        ErrorsMean(i,1) = mean(abs(Errors(:,1)));
        ErrorsMean(i,2) = mean(abs(Errors(:,2)));
        ErrorsMean(i,3) = mean(abs(Errors(:,3)));
        ErrorsMean(i,4) = mean(abs(Errors(:,4)));
        
end 

plot([10 100 500 1000], ErrorsMean(:,1), [10 100 500 1000], ErrorsMean(:,2), [10 100 500 1000], ErrorsMean(:,3), [10 100 500 1000], ErrorsMean(:,4))
ylabel('Error %')
xlabel('N (number of neurons in network')