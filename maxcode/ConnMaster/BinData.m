function y = BinData(data, N)

y = zeros(N);
%# Total simulation time
T = 2000;
for i = 1:length(data),
    if rem(i,2) == 1,
        j = (floor(data(i)*N/T));
        y(j) = y(j) + 1;
    end
end