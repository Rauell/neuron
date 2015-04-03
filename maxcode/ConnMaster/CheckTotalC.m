function avg = CheckTotalC(connStruct)

avg = 0;
for i = 1 : 10000,
    
    avg = avg + sum(sum(Connections_Thresh(connStruct, 1, 7)));
    
end
avg = avg/10000;