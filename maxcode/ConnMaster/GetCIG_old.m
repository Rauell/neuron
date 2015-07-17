function [CIG] = GetCIG(geo, Conn, curL, node, dim)
 
%{
    This program will determine the CIG of a given geometric
    network with regards to spatial organization.  The 3D network will be
    collapsed into a 2D grid, and the grid will have n*n nodes.  The
    neurons will be assigned to nodes respective to their position and the
    dimension in which they are being collapsed.  Each node is then
    evaluated in terms of CIG, which are saved.
 
    INPUT
 
    dim : Dimension (x,y, or z) in which the network will be collapsed
    geo : Geometric positions of each neuron
    a   : Length of the cubic neural block
    n   : Defines the number of grid points/nodes
    data: Firing data for neurons in the network
%}

%% Step 1 - Create grid respect to dim. 
a = curL;
n = node;
b = a/(n-1);  % Length of each node.
c = b/2;      % Useful for speeding up calculations laterCIGz Rand ACN
geo = geo(1:length(Conn),:);
geo = PerturbGeo(geo, a, b);
N = length(geo);

if dim == 1,     % Analyze x-direction
    geo = [geo(:,2) geo(:,3)];
elseif dim == 2, % Analyze y-direction
    geo = [geo(:,1) geo(:,3)];
else             % Analyze z-direction
    geo = [geo(:,1) geo(:,2)];
end

grid = zeros(n, n, 2);
for i = 1 : n,
    for j = 1 : n,
        grid(i,j,2) = (i-1)*b + c;
        
        grid(i,j,1) = (j-1)*b + c;
        
    end
end

%% Step 2 - Assign neurons to node points.
CIG = 0;
NCIG = 0;
total = 0;
for i = 1:n-1, 
    for j = 1:n-1, % Iterate through all nodes
        
        if sum(sum(Conn > 0)),
        
            temp = zeros(1,1); % Temp matrix to store neural indices
            count = 1;

            for k = 1:N, % Iterate through all neurons

                [temp, count] = GetInGrid(geo(k,:), grid(i,j,1), grid(i,j,2), a, b, c, temp, count, k, 100000000000); % inhibIndex normally goes in last spot

            end

            %{
            disp('method 1')
            if length(temp) > 1,

                cig = 0;

                ncig = 0;

                for k = 1:length(temp),

                    ii = temp(k);

                    for jj = 1:length(Conn),

                        if Conn(ii,jj) > 0,

                            if any(temp == jj),

                                cig = cig + 1;

                                CIG = CIG + 1;

                            else

                                ncig = ncig + 1;

                                NCIG = NCIG + 1;

                            end

                            Conn(ii,jj) = 0;

                        end

                        if Conn(jj,ii) > 0,

                            if any(temp == jj),

                                cig = cig + 1;

                                CIG = CIG + 1;

                            else

                                ncig = ncig + 1;

                                NCIG = NCIG + 1;

                            end

                            Conn(jj,ii) = 0;

                        end

                    end

                end

            end

            cig

            ncig

            %}

            if length(temp) > 1,

                cig = sum(sum(Conn(temp,temp)));

                Conn(temp,temp) = 0;

                ncig = sum(sum(Conn(temp,:))) + sum(sum(Conn(:,temp)));

                Conn(temp,:) = 0;

                Conn(:,temp) = 0;

                CIG = CIG + cig;

                NCIG = NCIG + ncig;

            end       

            total = total + length(temp);
            
        end
    end
end
 
CIG = CIG/NCIG;