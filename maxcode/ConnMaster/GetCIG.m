function [CIG] = GetCIG(geo, Conn, curL, node, inhib, dim)
 
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
if dim == 1,     % Analyze x-direction
    geo = [geo(:,2) geo(:,3)];
elseif dim == 2, % Analyze y-direction
    geo = [geo(:,1) geo(:,3)];
else             % Analyze z-direction
    geo = [geo(:,1) geo(:,2)];
end
b = a/(n-1);  % Length of each node.
c = b/2;      % Useful for speeding up calculations laterCIGz Rand ACN
grid = zeros(n, n, 2);
for i = 1 : n,
    for j = 1 : n,
        grid(i,j,2) = (i-1)*b + c;
        
        grid(i,j,1) = (j-1)*b + c;
        
    end
end
geo = geo(1:length(Conn),:);
N = length(geo);

%% Step 2 - Assign neurons to node points.
CIG = 0;
total = 0;
for i = 1:n-1, 
    for j = 1:n-1, % Iterate through all nodes
        
        temp = zeros(1,1); % Temp matrix to store neural indices
        count = 1;
        
        for k = 1:N, % Iterate through all neurons
            
            [temp, count] = GetInGrid(geo(k,:), grid(i,j,1), grid(i,j,2), a, b, c, temp, count, k, inhib); % inhibIndex normally goes in last spot

        end
        
        if length(temp) > 1,

            CIG = CIG + sum(sum(Conn(temp, temp) > 0))/(length(temp)^2 -length(temp));  % This is a great ass line of code if I do say so myself
            
        end
        
        total = total + length(temp);
    end
end

CIG = CIG/((n-1)*(n-1));