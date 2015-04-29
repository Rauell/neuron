function [] = MoveNetworkConstants(directory_name, directory_name1)

source_og = sprintf('%s%s/%s',directory_name);
for i = 1 : 100,
    
    directory_name2 = int2str(i);
    destination = sprintf('%s%s/%s/networkConstants.txt',directory_name, directory_name1, directory_name2);
    directory_name2 = int2str(i);
    source = sprintf('%snetworkConstants%s.txt',source_og, directory_name2);
    copyfile(source, destination)
end