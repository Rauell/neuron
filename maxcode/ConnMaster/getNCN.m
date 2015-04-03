function cneigh=getNCN(conn)
%this function returns a matrix with the number of cells that connect
%simultaneously, irrespective of direction, the two cells defined by the
%row and column in the result matrix
nc=size(conn,1); %get size of matrix
neigh=double((conn+conn')&1); %make direction irrelevant
cneigh=neigh*neigh.*(1-eye(nc)); %get common neighbors and ignore diagonal
end