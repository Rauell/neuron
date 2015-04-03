function [] = TestConMicros()


connStruct = CreateConnectivityStructure();
connStruct.L = 100;
connStruct.N = 1000;
totalCon = zeros(100,1);
connStruct.CEE = 8;

for x = 1 : 101,
    
    connStruct.x = (x-1)/100;
    data = connStruct.L*rand(connStruct.N,3);
    [ID, NE] = MakeRandomID(connStruct.N);
    connStruct.ID = ID;
    connStruct.NE = NE;
    connStruct.NI = connStruct.N - NE;
    connStruct = CreateDistanceMatrices(connStruct, data); 
    C = CreateConnectivityMatrix(connStruct, 1);
    totalCon(x,1) = sum(sum(C));
        
end 

plot(linspace(0,1,101), totalCon)
ylabel('Number of connections in 800 exc. neurons')
xlabel('x')