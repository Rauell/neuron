load('SPIKE_EXP_YOUNG.mat')
results = zeros(20,2);
results(:,1) = mean(SPIKE)';
results(:,2) = std(SPIKE)';
hold on
x = linspace(5,100,20)';
errorbar(x,results(:,1), results(:,2), 'k', 'LineWidth',2)

load('SPIKE_EXP_RAND.mat')
results = zeros(20,2);
results(:,1) = mean(SPIKE)';
results(:,2) = std(SPIKE)';
x = linspace(5,100,20)';
errorbar(x,results(:,1), results(:,2), 'r', 'LineWidth',2)

load('SPIKE_CN_YOUNG.mat')
results = zeros(20,2);
results(:,1) = mean(SPIKE)';
results(:,2) = std(SPIKE)';
x = linspace(5,100,20)';
errorbar(x,results(:,1), results(:,2), 'k--', 'LineWidth',2)

load('SPIKE_CN_RAND.mat')
results = zeros(20,2);
results(:,1) = mean(SPIKE)';
results(:,2) = std(SPIKE)';
x = linspace(5,100,20)';
errorbar(x,results(:,1), results(:,2), 'r--', 'LineWidth',2)

%title('SP', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
ylabel('SPIKE distances', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
xlabel('Stimulus interval (ms)', 'FontSize', 14, 'FontWeight', 'bold', 'FontName','Times')
set(gca,'LineWidth',2,'FontSize',14, 'FontWeight', 'bold', 'FontName','Times')
axis([3 102 0.096 0.11])
legend('EXP MICRO', 'EXP RANDOM', 'CN MICRO', 'CN RANDOM')