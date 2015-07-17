function [] = Analysis_PowerSpectrum(file_name)

data = load(file_name);
% Number of samplepoints
N = 5000;
% sample spacing
T = 2.0 / N;
x = linspace(1, N*T, N);
y = BinData(data, N);
yf = fft(y);
xf = linspace(0.0, 1.0/(2.0*T), N/2);
plot(xf, 2.0/N * abs(yf(1:N/2)))
xlabel('Frequency (Hz)')
title('Power Spectrum - Stimulus 1 Hz')
axis([0 100 0 15])