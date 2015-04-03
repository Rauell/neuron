function bestThresh = FindBestThresh(D, numCon, N1, N2)

%% Iteratively search matrix and find the best threshold value.
bestThresh = 0;
for i = 1 : N1,
    
    for j = 1 : N2,
        
        currThresh = D(i,j);
        
        c = sum(sum(D < currThresh));
        
        if abs(c - numCon)/numCon < 0.05,
            
            bestThresh = currThresh;
            
            return
        
        end
        
    end
    
end