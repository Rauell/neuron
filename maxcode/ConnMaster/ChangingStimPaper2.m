load('/home/hendemd/Desktop/MATLAB/bin/Paper 2/test/343/Crystal/1/Nearest neighbors/interval50.txt')
load('/home/hendemd/Desktop/MATLAB/bin/Paper 2/test/343/Crystal/1/Nearest neighbors/interval500.txt')
load('/home/hendemd/Desktop/MATLAB/bin/Paper 2/test/343/Crystal/1/Nearest neighbors/interval1000.txt')

hold on
subplot(3,1,1)
TestPaper2(interval50)
subplot(3,1,2)
TestPaper2(interval500)
subplot(3,1,3)
TestPaper2(interval1000)