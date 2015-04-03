function conn2=Reorganize(conn,iter,r,m,p,pr,pnr)

%{
    This program will determine the connectivity between inhibitory neurons
    receiving input from nearby excitory neurons, as shown in Bock et al 2011
    and Hofer et al 2011.

    INPUT
    
    D : Intersomatic distances between neurons in network.
    inhibIndex : Demarker of where neurons flip from exc. to inh.
    N : Number of neurons in the network.
    
    OUTPUT

    CEI : Connections between exc. and inh. neurons in network.

    Max Henderson
    Last updated: Sept. 14, 2014    
    Drexel University
%}

% conn: is the initial binary connectivity matrix (nxn)
% iter: is the number of iterations to perform (scalar)
% ?r? is the power given to the reorganization matric to (scalar)
% ?m? mean weight factor before applying power (scalar)
% ?p? is the probability of connection as a function of distance applied to
%each pair (nxn)
% ?pr? is the reciprocal probability of connection as a function of distance
%applied to each pair (nxn)
% ?pnr? is the non-reciprocal probability of connection as a function of
%distance applied to each pair (nxn)
% ?dist? is the distance between the neurons in each pair (nxn)
n=length(conn); %number of cells
ins=sum(conn); %array of column sums to determine
%number of inputs per cell
conn2=conn; %allocating final connectivity
for i=1:iter,
    conn=double(conn2); %to operate on results of last iteration
    cn=getNCN(conn); %get common neighbors
    for j=1:n,
        cn(:,j)=cn(:,j)/(m*mean(cn(:,j))); %divide common neighbors by
        %the weighted mean
        cn(:,j)=cn(:,j).^r; %apply power
        cn(:,j)=cn(:,j).*p(:,j); %keep distance relations
        cn(:,j)=cn(:,j)./sum(cn(:,j)); %normalize to 1
        cn(:,j)=cn(:,j)*ins(j); %to keep total inputs constant
    end
    pi=(cn+cn')/2; %extract connection probability weight in each pair
    cpnr=pnr./p.*pi; %define non-reciprocal connection probability
    cpr=pr./p.*pi; %define reciprocal connection probability
    clear pi
    clear cn
    %sum(sum(cpr + cpnr/2))
    %sum(sum(pp))
    %adjust for diagonal
    for ii = 1:length(cpr),
        cpnr(ii,ii) = 0;
        cpr(ii,ii) = 0;
    end
    % get pull probability matrix
    cp = cpr + cpnr*0.5;
    rnd=rand(n); %define random matrix
    %rnd=triu(rnd,1)+tril(ones(n)); %make it upper triangular
    %cr=rnd<cpr; %reciprocal connections
    %cnr1=(rnd<(cpr+cpnr)).*(rnd>=(cpr)); %non-reciprocal one way
    %cnr2=(rnd<(cpr+2*cpnr).*(rnd>=(cpr+cpnr))); %non-reciprocal other way
    %conn2=cr+cr'+cnr1+cnr2'; %final connectivity    
    %conn2=conn2>0;
    conn2 = cp>rnd;
end