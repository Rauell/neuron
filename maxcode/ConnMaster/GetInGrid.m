function [temp, count] = GetInGrid(geo, gridx, gridy, a, b, c, temp, count, n, inhibIndex)

%{
    This function will determine if a neuron is in a particular node,
    accounting for BC.

    Max Henderson
    7/22/14
    Drexel University
%}

upX = gridx;
lowX = gridx - b;
upY = gridy;
lowY = gridy - b;

if n >= inhibIndex,
    
    return
    
end


if     ((lowX < 0 && lowY < 0) || (upX > a && lowY < 0) || (lowX < 0 && upY > a) || (upX > a && upY > a)),
   
    if (geo(1) < c) && (geo(2) < c),
        temp(count) = n;
        count = count + 1;
    end
    
    if (geo(1) > a-c) && (geo(2) < c),
        temp(count) = n;
        count = count + 1;
    end
    
    if  (geo(1) < c) && (geo(2) > a-c),
        temp(count) = n;
        count = count + 1;
    end
    
    if (geo(1) > a-c) && (geo(2) > a-c),
        temp(count) = n;
        count = count + 1;
    end
    
elseif ((lowX < 0) || (upX > a)),
    
    if ((geo(1) < c) && ((geo(2) > lowY) && (geo(2) < upY))),
        temp(count) = n;
        count = count + 1;
    end
    
    if ((geo(1) > a-c) && ((geo(2) > lowY) && (geo(2) < upY))),
        temp(count) = n;
        count = count + 1;
    end
    
elseif ((lowY < 0) || (upY > a)),
    
    if ((geo(2) < c) && ((geo(1) > lowX) && (geo(1) < upX))),
        temp(count) = n;
        count = count + 1;
    end
    
    if ((geo(2) > a-c) && ((geo(1) > lowX) && (geo(1) < upX))),
        temp(count) = n;
        count = count + 1;
    end
    
else
    
    if ((geo(1) > lowX) && (geo(1) < upX))     && ((geo(2) > lowY) && (geo(2) < upY)),
        temp(count) = n;
        count = count + 1;
    end
    
end